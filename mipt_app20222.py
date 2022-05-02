import sqlite3
import os
from flask import Flask, render_template, request, url_for, g, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = '/tmp/mipt_app20222.db'
DEBUG = True
SECRET_KEY = 'jbghgaiwgbbherlg'

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(DATABASE=os.path.join(app.root_path, 'mipt_app20222.db')))

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'], timeout = 10)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]

@app.route("/contact", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByName(request.form['name'])

        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)

            return redirect(request.args.get("next") or url_for("index"))
        flash("Неверная пара логин/пароль", "error")

    return render_template("contact.html", menu=dbase.getMenu(), title="Автори    зация")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['name']) >= 4 and len(request.form['psw']) >= 4\
            and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], hash, "", "", "")

            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
    else:
        flash("Неверно заполнены поля", "error")

    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")

@app.route("/index")
def index():
    return render_template('index.html', title="Главная страница сайта", menu=dbase.getMenu())

@app.route("/find", methods=['POST', 'GET'])
def find():
    if request.method == 'POST':
        res = dbase.getUserByName(request.form['name'])
        if res:
            return redirect('/nick/' + request.form['name'])
        else:
            pass
    return render_template("find.html", menu=dbase.getMenu(), title="Поиск пользователей")

@app.route("/nick/<user>")
def nick(user):

    return render_template("nick.html", menu=dbase.getMenu(), title="Результат поиска", user = user)


@app.route("/added/<user>")
def added(user):

    res = dbase.getUser(current_user.get_id())
    res2 = dbase.addFriend(res['handle'], user)


    return render_template("added.html", menu=dbase.getMenu(), title="Пользователь добавлен!", user = user)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/about")
def about():
    return "<h1>О сайте</h1>"

@app.route("/friends")
@login_required
def friends():
    res = dbase.getUser(current_user.get_id())
    f = list(res['friends'].split())

    return render_template("friends.html", menu=dbase.getMenu(), title="Список друзей", fmenu = f)

@app.route("/dialogue", methods=['POST', 'GET'])
@login_required
def dialogue():
    if request.method == "POST":
        res = dbase.getUser(current_user.get_id())
        f = list(res['friends'].split())
        #f1 = list(res['to_friend'].split())
        #f2 = list(res['from_friend'].split())

        #res5 = dbase.toMessage(res['handle'], request.form['msg'], request.form['name'])
    return render_template("dialogue.html", menu=dbase.getMenu(), title="Отправить сообщение")


if __name__ == "__main__":
    app.run(debug=True)

