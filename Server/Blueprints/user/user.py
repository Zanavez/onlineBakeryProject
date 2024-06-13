from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import ShopService, RegistrateTableService
from Server.Forms import CreateOrderForm, OrderSweetUpdateForm

from Server.database import TypeOrder, RegistrateTable

from Server.Models import state_order, type_order

user_router = Blueprint("user", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "index", "title": "Главная"},
    {"url": "shop", "title": "Магазин"},
]


@user_router.before_request
def is_user():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "user" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@user_router.route("/car/add/<uuid>")
@login_required
def add_car(uuid: str):
    cart = session.get("car")
    if uuid not in session["car"]:
        cart[uuid] = 0
    cart[uuid] += 1
    session["car"] = cart
    return redirect(f"/shop")


@user_router.route("/car")
@login_required
def car():
    cart: dict = session.get("car")
    service = ShopService()
    order_sweet_product = service.get_list_product_by_uuid(list(cart.keys()), cart)
    sum_cart = 0
    for prod in order_sweet_product:
        sum_cart += prod.count * prod.price
    return render_template("car.html", menu=menu, user=current_user, products=order_sweet_product, sum_cart=sum_cart)


@user_router.route("/car/delete/<uuid>")
@login_required
def delete_car(uuid: str):
    cart: dict = session.get("car")
    if cart[uuid] == 1:
        cart.pop(uuid)
    else:
        cart[uuid] -= 1
    session["car"] = cart
    return redirect(url_for("user_blueprint.car"))


@user_router.route("/list_order", methods=["GET"])
@login_required
def list_order():
    service = ShopService()
    list_order_json = service.get_list_order_by_user_id(current_user.user.id)
    return render_template("list_order.html", menu=menu, user=current_user, orders=list_order_json, state_order=state_order)


@user_router.route("/info_order/<uuid>", methods=["GET"])
@login_required
def info_order(uuid: str):
    service = ShopService()
    order = service.get_order_by_uuid(uuid)
    return render_template("info_order.html", menu=menu, user=current_user, order=order, type_order=type_order, state_order=state_order)


@user_router.route("/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    form = CreateOrderForm()
    service = ShopService()
    service_reg = RegistrateTableService()
    bakery = service.get_list_bakery()
    form.bakeries.choices = [(g.trace_id, g.name) for g in bakery]
    if request.method == "GET":
        cart = session.get("car")
        form.type_order.data = 1
        order_sweet_product = service.get_list_product_by_uuid(list(cart.keys()), cart)
        sum_cart = 0
        for prod in order_sweet_product:
            sum_cart += prod.count * prod.price

        return render_template("create_order.html",
                               menu=menu,
                               user=current_user,
                               form=form,
                               sum_cart=sum_cart,
                               products=order_sweet_product)
    elif request.method == "POST":
            address = ""
            type_order = TypeOrder.in_hall
            if int(form.type_order.data) == TypeOrder.in_hall.value:
                address = service.get_address_by_bakery_uuid(form.bakeries.data)
                print("Тип заказа: в зале")
            else:
                type_order = TypeOrder.with_myself
                address = service.get_address_by_bakery_uuid(form.bakeries.data)
                print("Тип заказа: Бронирование")
            cart = session.get("car")
            order = service.create_order(type_order, address, form.description.data, cart, current_user.user.id)
            if order is not None:
                session["car"] = {}
                service_reg.add_registrate_table(RegistrateTable(
                    name=current_user.user.name,
                    surname=current_user.user.surname,
                    patronymics=current_user.user.patronymics,
                    phone=current_user.user.phone,
                    bakery_id=service.get_bakery_uuid(form.bakeries.data).id,
                    data_registrate=form.date_reg.data,
                    order_id=order.id
                ))
                return redirect(url_for('user_blueprint.info_order',  uuid=order.trace_id))
            else:
                return redirect(url_for("user_blueprint.create_order"))


@user_router.route("/car/update/<uuid>", methods=["GET", "POST"])
@login_required
def update_car(uuid: str):
    form = OrderSweetUpdateForm()
    if request.method == "GET":
        cart: dict = session.get("car")

        form.count.data = cart[uuid]
        return render_template("update_item_order.html",
                               menu=menu,
                               user=current_user,
                               form=form,
                               uuid_item=uuid)
    elif request.method == "POST":
        count = form.count.data
        cart: dict = session.get("car")
        if count <= 0:
            return redirect(url_for("user_blueprint.delete_car", uuid=uuid))
        else:
            cart[uuid] = count
        session["car"] = cart
        print(url_for("user_blueprint.car"))
        return redirect(url_for("user_blueprint.car"))