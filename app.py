from flask import Flask
from model_db import db
from db_init import init_db
from views import user_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False

# Инициализируем базу данных и добавляем Blueprint
init_db(app)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

