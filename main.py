import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

# читаем данные из файла
list_of_users = utils.load_data("data/user.json")
list_of_orders = utils.load_data("data/orders.json")
list_of_offers = utils.load_data("data/offers.json")



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
        role_id = db.Column(db.Integer)

        # get_order = relationship("Order", foreign_keys=[Order.costumer_id])
        # offers = relationship("Offer")

    class Offer(db.Model):
        __tablename__ = "offer"
        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
        executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

        # order = relationship("Order")
        # give_order = relationship("User")

    class Order(db.Model):
        __tablename__ = "order"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(255), nullable=False)
        start_date = db.Column(db.Date, nullable=False)
        end_date = db.Column(db.Date, nullable=False)
        address = db.Column(db.String(255), nullable=False)
        price = db.Column(db.Integer)
        customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

        # user_costumer = relationship("User", foreign_keys=[costumer_id], back_populates='get_order')
        # user_executor = relationship("User", foreign_keys=[executor_id], back_populates='give_order')
        # offers = relationship("Offer")

    db.drop_all()
    db.create_all()

    for user in list_of_users:

        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone'],
            role_id=user['role_id']
        ))

    for order in list_of_orders:
        month_start, day_start, year_start = order['start_date'].split("/")
        month_end, day_end, year_end = order['end_date'].split("/")
        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))

    for offer in list_of_offers:
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))

    db.session.commit()

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


#
# if __name__ == "__main__":
#     app.run(port=5000)

