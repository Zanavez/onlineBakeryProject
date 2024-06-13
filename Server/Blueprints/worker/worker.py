from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import OrderService
from Server.Forms import SearchOrderWorkerForm

from Server.database import TypeOrder, StatusOrder

from Server.Models import state_order, type_order


worker_router = Blueprint("worker", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "worker_blueprint.order", "title": "Заказы"},
]


@worker_router.before_request
def is_worker():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "worker" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@worker_router.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", menu=menu, user=current_user)


@worker_router.route("/orders", methods=["GET", "POST"])
@login_required
def order():

    args = request.args
    form = SearchOrderWorkerForm()

    state_user = args.get("state_user")
    type_user = args.get("type_user")

    if state_user is None:
        state_user = StatusOrder.confirmed.name

    service = OrderService()
    if request.method == "GET":
        orders_entity = service.get_list_order_by_state_order(state_user)
        return render_template("order_worker.html",
                               menu=menu,
                               user=current_user,
                               orders=orders_entity,
                               type_order=type_order,
                               state_order=state_order,
                               form=form)
    elif request.method == "POST":
        return redirect(url_for("worker_blueprint.order", state_user=form.state_order.data))


@worker_router.route("/order/<uuid>", methods=["GET"])
@login_required
def order_info(uuid: str):

    service = OrderService()
    orders_entity = service.get_order(uuid)

    return render_template("info_order_worker.html",
                           menu=menu,
                           user=current_user,
                           order=orders_entity,
                           type_order=type_order,
                           state_order=state_order)


@worker_router.route("/order/update_state/<uuid>", methods=["GET"])
@login_required
def order_update_state(uuid: str):
    service = OrderService()
    orders_entity = service.get_order(uuid)

    order = service.order_update_status(uuid)
    return redirect(url_for("worker_blueprint.order",  state_user=order.status_order.name))

