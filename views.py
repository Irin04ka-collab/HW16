"""
Здесь реализуем представления для API
"""
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request

from data import orders, offers
from model_db import *
from schema import OfferSchema, OrderSchema, UserSchema

# Создаем Blueprint для маршрутов пользователей
user_blueprint = Blueprint('user_blueprint', __name__)

# Создаём экземпляры схем
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify(users_schema.dump(users)), 200


@user_blueprint.route('/users/<int:uid>', methods=['GET'])
def get_one_user(uid):
    user = User.query.get(uid)
    if user is None:
        return jsonify(f"по указанному id={uid} нет данных в базе данных"), 404

    return jsonify(user_schema.dump(user)), 200


@user_blueprint.route('/users', methods=['POST'])
def add_user():
    try:
        # Десериализация данных
        data = user_schema.load(request.json)
        user=User(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201

    except IntegrityError as e:
        db.session.rollback()
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)



@user_blueprint.route('/users/<uid>', methods=['DELETE'])
def del_user(uid):
    user = User.query.get(uid)
    if user is None:
        return jsonify(f"по указанному id={uid} нет данных в базе данных"), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(f"Пользователь с id={uid} удален."), 200

@user_blueprint.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    user = User.query.get(uid)
    if not user:
        return jsonify(f"по указанному id={uid} нет данных в базе данных"), 404

    try:
        data = user_schema.load(request.json)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return jsonify(f"Пользователь обновлен"), 200

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле."), 400
        else:
            return("Произошла ошибка целостности данных:", e), 400



@user_blueprint.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()

    return jsonify(orders_schema.dump(orders)), 200


@user_blueprint.route('/orders/<int:oid>', methods=['GET'])
def get_one_order(oid):
    order = Order.query.get(oid)
    if order is None:
        return jsonify(f"по указанному id={oid} нет данных в базе данных"), 404

    return jsonify(order_schema.dump(order)), 200

@user_blueprint.route('/orders', methods=['POST'])
def add_order():
    try:
        data = order_schema.load(request.json)
        order = Order(**data)

        db.session.add(order)
        db.session.commit()
        return jsonify(order_schema.dump(order)), 200

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e), 404


@user_blueprint.route('/orders/<oid>', methods=['DELETE'])
def del_order(oid):
    order = Order.query.get(oid)
    if order is None:
        return jsonify(f"по указанному id={oid} нет данных в базе данных"), 200

    db.session.delete(order)
    db.session.commit()

    return jsonify(f"Заказ {oid} удален"), 200

@user_blueprint.route('/orders/<oid>', methods=['PUT'])
def update_order(oid):
    order = Order.query.get(oid)
    if not order:
        return jsonify(f"по указанному id={oid} нет данных в базе данных"), 200


    try:
        data = order_schema.load(request.json)
        for key, value in data.items():
            setattr(order, key, value)

        db.session.add(order)
        db.session.commit()
        return jsonify(f"Заказ {oid} обновлен"), 200

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле."), 400
        else:
            return("Произошла ошибка целостности данных:", e)



@user_blueprint.route('/offers', methods=['GET'])
def get_offers():
    offers = Offer.query.all()

    return jsonify(offers_schema.dump(offers)), 200


@user_blueprint.route('/offers/<int:ofid>', methods=['GET'])
def get_one_offer(ofid):
    offer = Offer.query.get(ofid)
    if offer is None:
        return jsonify(f"по указанному id={ofid} нет данных в базе данных"), 404

    return jsonify(offer_schema.dump(offer)), 200


@user_blueprint.route('/offers', methods=['POST'])
def add_offer():
    data = offer_schema.load(request.json)
    try:
        offer = Offer(**data)
        db.session.add(offer)
        db.session.commit()
        return jsonify(offer_schema.dump(offer)), 200

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)



@user_blueprint.route('/offers/<ofid>', methods=['DELETE'])
def del_offer(ofid):
    offer = Offer.query.get(ofid)
    if offer is None:
        return jsonify(f"по указанному id={ofid} нет данных в базе данных"), 200

    db.session.delete(offer)
    db.session.commit()

    return jsonify(f"Предложение id={ofid} удалено"), 200

@user_blueprint.route('/offers/<ofid>', methods=['PUT'])
def update_offer(ofid):
    offer = Offer.query.get(ofid)
    if not offer:
        jsonify(f"по указанному id={ofid} нет данных в базе данных"), 200

    try:
        data = offer_schema.load(request.json)
        for key, value in data.items():
            setattr(offer, key, value)

        db.session.add(offer)
        db.session.commit()
        return jsonify(f"Обновлено предложение id={ofid}"), 200

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)



