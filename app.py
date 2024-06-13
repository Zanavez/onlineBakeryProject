from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_uuid import FlaskUUID
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from Server.database import db, Role, User, SweetProduct, Ingredient, Bakery, Type, Table, RegistrateTable
from Server.Models import UserSession

from Server.Repository import UserRepository
from Server.Models import GetUser
from Server.Service import LoginService, UserService, ShopService, RegistrateTableService
from Server.AdminView import *
from Server.Forms import LoginForm, RegistrationForm, SearchSweetProduct, RegTableFrom

from Server.Blueprints.user.user import user_router
from Server.Blueprints.manager.manager import manager_router
from Server.Blueprints.worker.worker import worker_router

from settings import settings
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '2wae3tgv'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = '/Files'


app.register_blueprint(manager_router, name="manager_blueprint", url_prefix="/manager")
app.register_blueprint(user_router, name="user_blueprint", url_prefix="/user")
app.register_blueprint(worker_router, name="worker_blueprint", url_prefix="/worker")

flask_uuid = FlaskUUID()

db.init_app(app)
flask_uuid.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)


route = {
    "worker": "/worker",
    "manager": "manager_blueprint.index",
    "admin": "/admin",
    "user": "/"
}

menu = [
    {"url": "index", "title": "Главная"},
    {"url": "shop", "title": "Товары"},
    {"url": "reg_table", "title": "Бронирование столика"}
]


@login_manager.user_loader
def load_user(id_user) -> UserSession:
    repo = UserRepository(db.session)
    try:
        return UserSession(GetUser.model_validate(repo.get_user(int(id_user)), from_attributes=True))
    except:
        return UserSession(None)


@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "worker" in user_roles:
            return redirect(route["worker"])
        elif "manager" in user_roles:
            return redirect(url_for(route["manager"]))
        elif "admin" in user_roles:
            return redirect(route["admin"])
        else:
            return render_template("index.html", exception="", menu=menu, user=current_user)

    else:
        return render_template("index.html", exception="", menu=menu, user=current_user)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Авторизация", form=form, menu=menu, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            login_service = LoginService()

            user = login_service.login_user(form.email.data, form.password.data)
            if user is None:
                return redirect("login")
            login_user(UserSession(user))
            session["car"] = {}
            return redirect("/")
        return redirect("login")


@app.route("/reg_table",  methods=["POST", "GET"])
def reg_table():
    form = RegTableFrom()
    is_user = False
    service_shop = ShopService()
    bakery = service_shop.get_list_bakery()
    form.bakeries.choices = [(g.trace_id, g.name) for g in bakery]
    message = None
    if current_user.is_authenticated:
        is_user = True
    if request.method == "GET":
        message = None
    if request.method == "POST":
        service = RegistrateTableService()
        entity = RegistrateTable()
        if current_user.is_authenticated:
            entity.name = current_user.user.name
            entity.surname = current_user.user.surname
            entity.patronymics = current_user.user.patronymics
            entity.phone = current_user.user.phone
        else:
            entity.name = form.name.data
            entity.surname = form.surname.data
            entity.patronymics = form.patronymics.data
            entity.phone = form.phone.data
        bakery = service_shop.get_bakery_uuid(form.bakeries.data)
        entity.bakery_id = bakery.id
        entity.data_registrate = form.date_reg.data
        service.add_registrate_table(entity)
        message = "Спасибо за заявку, менеджер скоро с вами свяжется"
    return render_template("reg_table.html", title="Бронирование", form=form, menu=menu, user=current_user,
                           is_user=is_user, message=message)


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("registration.html", title="Авторизация", form=form, menu=menu, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            user_service = UserService()
            user = user_service.registration(
                form.name.data,
                form.surname.data,
                form.patronymics.data,
                form.phone.data,
                form.email.data,
                form.password.data
            )
            print(1)
            login_user(UserSession(user))
            session["car"] = {}
            return redirect(url_for('index'))
        return render_template("registration.html", title="Авторизация", form=form, menu=menu, user=current_user)


@app.route("/shop", methods=["GET", "POST"])
def shop():
    form = SearchSweetProduct()
    shop_service = ShopService()
    args = request.args
    tag = args.get("type")

    form.tag.choices = [(i.id, i.name) for i in shop_service.get_list_tag()]
    form.tag.choices.append((0, "все"))
    if request.method == "GET":
        if tag is None or int(tag) == 0:
            sweet_products = shop_service.get_sweet_product()
        else:
            sweet_products = shop_service.get_sweet_product_by_tag(int(tag))

        return render_template("shop.html",
                               title="Магазин",
                               menu=menu,
                               user=current_user,
                               sweet_products=sweet_products,
                               form=form)
    elif request.method == "POST":
        return redirect(url_for("shop", type=form.tag.data))


@app.route("/product/<uuid>/", methods=["GET"])
def product(uuid: str):
    if request.method == "GET":
        service = ShopService()
        sweet_product = service.get_product(uuid)
        return render_template("product_information.html",
                               title=sweet_product.name,
                               menu=menu,
                               user=current_user,
                               product=sweet_product)


@app.route("/init_app/<password>", methods=["GET"])
def create_user_admin(password):
    if request.method == "GET":
        if password == "AdminPassword1":
            roles = [
                Role(
                    name="worker",
                    description="worker"
                ),
                Role(
                    name="manager",
                    description="manager"
                ),
                Role(
                    name="admin",
                    description="admin"
                ),
                Role(
                    name="user",
                    description="user"
                ),
            ]

            db.session.add_all(roles)
            db.session.commit()

            admin_user = User(
                name="Александр",
                surname="Абрамов",
                patronymics="Александрович",

                phone="9023500725",
                email="admin@admin.ru",

                role=roles[2],
                passport_series="0000",
                passport_number="123456"
            )
            admin_user.password = "admin"

            db.session.add(admin_user)
            db.session.commit()

            return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


admin = Admin(app, name="Панель Админ", template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(UserAdminView(User, db.session, name="Пользователь"))
admin.add_view(ModelView(Role, db.session, name="Роли"))
admin.add_view(SweetProductAdminView(SweetProduct, db.session, name="Кондитерские изделия"))
admin.add_view(ModelView(Ingredient, db.session, name="Ингредиенты"))
admin.add_view(ModelView(Type, db.session, name="Тип изделия"))
admin.add_view(BakeryAdminView(Bakery, db.session, name="Пекарня"))
admin.add_view(ModelView(Table, db.session, name="Места"))

admin.add_link(LogoutMenuLink(name="Выход", category="", url="/logout"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
