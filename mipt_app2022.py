from flask import Flask, render_template

app = Flask(__name__)

menu = ["Установка", "Первое приложение", "Обратная связь"]

@app.route("/")
def index():
    return render_template('index.html', title="Главная страница сайта", menu=menu)

@app.route("/about")
def about():
    return "<h1>О сайте</h1>"

if __name__ == "__main__":
    app.run(debug=True)
