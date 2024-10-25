from main import db

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

