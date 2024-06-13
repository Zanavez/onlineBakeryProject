from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import UserService, OrderService, ShopService, RegistrateTableService
from Server.Forms import UserForm, OrderUpdateForm, OrderSweetUpdateForm, SearchRegTableForm, RegTableUpdateFrom

from Server.database import TypeOrder, StatusOrder

from Server.Models import state_order, type_order

manager_router = Blueprint("manager", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "manager_blueprint.user", "title": "Клиенты"},
    {"url": "manager_blueprint.order", "title": "Заказы"},
    {"url": "manager_blueprint.registrate_table", "title": "Бронирование"}
]


@manager_router.before_request
def is_manager():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "manager" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@manager_router.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", menu=menu, user=current_user)


@manager_router.route("/user", methods=["GET"])
@login_required
def user():
    service = UserService()
    users_entity = service.get_list_by_user()
    return render_template("user.html", menu=menu, user=current_user, users=users_entity)


@manager_router.route("/user/update/<uuid>", methods=["POST", "GET"])
@login_required
def user_update(uuid: str):
    form = UserForm()
    service = UserService()
    user = service.get_user_by_uuid(uuid)
    if request.method == "GET":

        form.name.data = user.name
        form.surname.data = user.surname
        form.patronymics.data = user.patronymics
        form.phone.data = user.phone
        form.email.data = user.email

        return render_template("user_update.html", menu=menu, user=current_user, user_target=user, form=form)
    else:
        if form.validate_on_submit():
            service.update_user(uuid,
                                form.name.data,
                                form.surname.data,
                                form.patronymics.data,
                                form.phone.data,
                                form.email.data)

        return redirect(url_for("manager_blueprint.user"))


@manager_router.route("/order", methods=["GET"])
@login_required
def order():
    service = OrderService()
    order_entity = service.get_list_order()
    return render_template("order.html", menu=menu, user=current_user, orders=order_entity, state_order=state_order,
                           type_order=type_order)


@manager_router.route("/order/update/<uuid>", methods=["POST", "GET"])
@login_required
def order_update(uuid: str):
    form = OrderUpdateForm()
    service_order = OrderService()
    service_shop = ShopService()
    bakery = service_shop.get_list_bakery()
    form.bakeries.choices = [(g.trace_id, g.name) for g in bakery]

    form.state_order.choices = [(g.name, state_order[g.value]) for g in StatusOrder]

    if request.method == "GET":
        order = service_order.get_order(uuid)

        if order.type_order == TypeOrder.in_hall:
            bakery = service_order.get_bakery_by_address(order.address)
            form.bakeries.data = bakery.trace_id
        else:
            form.address.data = order.address

        form.state_order.data = order.status_order.name

        return render_template("order_update.html", menu=menu,
                               user=current_user,
                               order=order,
                               form=form,
                               type_order=type_order)

    elif request.method == "POST":
        order = service_order.get_order(uuid)

        if order.type_order == TypeOrder.in_hall:
            address = service_shop.get_address_by_bakery_uuid(form.bakeries.data)
        else:
            address = form.address.data

        service_order.update(uuid, address, form.state_order.data)
        return redirect(url_for("manager_blueprint.order"))


@manager_router.route("/order_cart/delete/<int:id_order>/<int:id_sweet_product>", methods=["GET"])
@login_required
def delete_order_sweet_product(id_order: int, id_sweet_product: int):
    if request.method == "GET":
        service = OrderService()
        service.delete_order_sweet_product(id_order, id_sweet_product)
        order = service.get_order_by_id(id_order)
        return redirect(url_for('manager_blueprint.order_update', uuid=order.trace_id))


@manager_router.route("/order/back/<int:id_order>", methods=["GET"])
@login_required
def back_order(id_order: int):
    if request.method == "GET":
        service = OrderService()
        order = service.get_order_by_id(id_order)
        return redirect(url_for("manager_blueprint.order_update", uuid=order.trace_id))


@manager_router.route("/order_cart/update/<int:id_order>/<int:id_sweet_product>", methods=["POST", "GET"])
@login_required
def order_car_update(id_order: int, id_sweet_product: int):
    service = OrderService()
    form = OrderSweetUpdateForm()
    if request.method == "GET":
        sweet_product_order = service.get_order_sweet_product(id_order, id_sweet_product)
        form.count.data = sweet_product_order.count
        return render_template("order_sweet_product_update.html",
                               menu=menu,
                               user=current_user,
                               product=sweet_product_order,
                               form=form,
                               type_order=type_order)
    elif request.method == "POST":
        if form.validate_on_submit():
            service.update_order_sweet_product(id_order, id_sweet_product, form.count.data)
            return redirect(url_for("manager_blueprint.back_order", id_order=id_order))


@manager_router.route("/registrate_table", methods=["POST", "GET"])
@login_required
def registrate_table():
    args = request.args
    form = SearchRegTableForm()

    state_reg_table = args.get("state_reg_table")

    if state_reg_table is None:
        state_reg_table = StatusOrder.waiting_for_confirmation.name
    service = RegistrateTableService()
    if request.method == "GET":
        reg_entity = service.get_list_reg_by_status_registrate(state_reg_table)

        return render_template("registrate_table.html",
                               menu=menu,
                               user=current_user,
                               regs=reg_entity,
                               state_order=state_order,
                               form=form)
    elif request.method == "POST":
        return redirect(url_for("manager_blueprint.registrate_table", state_reg_table=form.state_order.data))


@manager_router.route("/info_reg_table/<uuid>", methods=["POST", "GET"])
@login_required
def info_reg_table(uuid: str):
    service = RegistrateTableService()
    if request.method == "GET":
        entity = service.get_reg_by_uuid(uuid)
        start_time = 0
        end_time = 0
        if entity.start_time > 0:
            start_time = service.converter_min_to_time(entity.start_time)

        if entity.end_time > 0:
            end_time = service.converter_min_to_time(entity.end_time)

        return render_template("info_registrate_table.html",
                               menu=menu,
                               user=current_user,
                               reg=entity,
                               state_order=state_order,
                               start_time=start_time,
                               end_time=end_time)


@manager_router.route("/update_reg_table/<uuid>", methods=["POST", "GET"])
@login_required
def update_reg_table(uuid: str):
    form = RegTableUpdateFrom()
    service_table = RegistrateTableService()

    entity = service_table.get_reg_by_uuid(uuid)

    tables = service_table.get_tables_list(entity.bakery_id)
    form.table.choices = [(g.id, g.name) for g in tables]
    time = [(g, service_table.converter_min_to_time(g)) for g in range(9 * 60, 17 * 60, 30)]
    form.start_time.choices = time
    form.end_time.choices = time
    form.date_reg.data = entity.data_registrate
    tables_info = service_table.get_dict_map_table(entity.bakery_id, entity.data_registrate)
    if request.method == "GET":
        return render_template("update_reg_table.html",
                               menu=menu,
                               user=current_user,
                               reg=entity,
                               form=form,
                               uuid=uuid,
                               tables_info=tables_info)
    elif request.method == "POST":
        entity.table_id = form.table.data
        entity.data_registrate = form.date_reg.data
        entity.status_registrate = form.state_reg.data
        entity.start_time = form.start_time.data
        entity.end_time = form.end_time.data
        service_table.update(entity)
        order_service = OrderService()

        if entity.order_id is not None:
            order = order_service.get_order_by_id(entity.order_id)
            order_service.update(order.trace_id, order.address, StatusOrder.confirmed.name)

        return redirect(url_for('manager_blueprint.info_reg_table',  uuid=entity.trace_id))


