
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

with app.app_context():

    class User(db.Model):
        __tablename__ = "user"
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(40), nullable=False)
        last_name = db.Column(db.String(40), nullable=False)
        age = db.Column(db.Integer, db.CheckConstraint("age>0"))
        email = db.Column(db.String(100), nullable=False)
        role = db.Column(db.String(40), nullable=False)
        phone = db.Column(db.String(40), nullable=False)

        orders = relationship("Order")
        offers = relationship("Offer")

    class Offer(db.Model):
        __tablename__ = "offer"
        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
        executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

        order = relationship("Order")
        user = relationship("User")

    class Order(db.Model):
        __tablename__ = "order"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(255), nullable=False)
        start_date = db.Column(db.Date, nullable=False)
        end_date = db.Column(db.Date, nullable=False)
        addresses = db.Column(db.String(255), nullable=False)
        price = db.Column(db.Integer)
        costumer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

        user = relationship("User")
        offers = relationship("Offer")


    db.create_all()

#читаем данные из файла
list_of_users = utils.load_data("data/user.json")
list_of_orders = utils.load_data("data/orders.json")
list_of_offers = utils.load_data("data/offers.json")



@app.route('/users')
def get_users():
    return "Users"


@app.route('/users/<int:uid>')
def get_one_user(uid):
    return f"User {uid}"


@app.route('/orders')
def get_orders():
    return "orders"


@app.route('/orders/<int:oid>')
def get_one_order(oid):
    return f"order {oid}"


@app.route('/offers')
def get_offers():
    return "offers"


@app.route('/offers/<int:ofid>')
def get_one_offer(ofid):
    return f"offer {ofid}"




if __name__ == "__main__":
    app.run(port=5000)

