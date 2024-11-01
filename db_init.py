from model_db import db, User, Order, Offer
from data import users, orders, offers
import datetime

"""
В этом файле функции для инициализации базы данных и заполнения её данными
"""

def init_db(app):
    """
    инциализация БД
    """
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        fill_out_db()


def fill_out_db():
    """
    заполнение данными таблиц
    """

    for user_data in users:
        db.session.add(User(
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone']
            # так же это эквивалентно записи db.session.add(User(**user_data))
        ))

    for order_data in orders:
        month_start, day_start, year_start = order_data['start_date'].split("/")
        month_end, day_end, year_end = order_data['end_date'].split("/")
        db.session.add(Order(
            id=order_data['id'],
            name=order_data['name'],
            description=order_data['description'],
            start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order_data['address'],
            price=order_data['price'],
            customer_id=order_data['customer_id'],
            executor_id=order_data['executor_id']
        ))

    for offer_data in offers:
        db.session.add(Offer(
            id=offer_data['id'],
            order_id=offer_data['order_id'],
            executor_id=offer_data['executor_id']
        ))

    db.session.commit()
