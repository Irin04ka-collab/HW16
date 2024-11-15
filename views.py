"""
Здесь реализуем представления для API
"""
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from flask import Blueprint, jsonify, request

from model_db import *

# Создаем Blueprint для маршрутов пользователей
user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    result = []
    for user in User.query.all():
        result.append(user.to_dict())

    return jsonify(result), 200


@user_blueprint.route('/users/<int:uid>', methods=['GET'])
def get_one_user(uid):
    user = User.query.get(uid)
    if user is None:
        return jsonify(f"по указанному id={uid} нет данных в базе данных"), 404

    return jsonify(user.to_dict()), 200


@user_blueprint.route('/orders', methods=['GET'])
def get_orders():
    result = []
    for order in Order.query.all():
        result.append(order.to_dict())

    return jsonify(result), 200


@user_blueprint.route('/orders/<int:oid>', methods=['GET'])
def get_one_order(oid):
    order = Order.query.get(oid)
    if order is None:
        return jsonify(f"по указанному id={oid} нет данных в базе данных"), 404

    return jsonify(order.to_dict()), 200


@user_blueprint.route('/offers', methods=['GET'])
def get_offers():
    result = []
    for offer in Offer.query.all():
        result.append(offer.to_dict())

    return jsonify(result), 200


@user_blueprint.route('/offers/<int:ofid>', methods=['GET'])
def get_one_offer(ofid):
    offer = Offer.query.get(ofid)
    if offer is None:
        return jsonify(f"по указанному id={ofid} нет данных в базе данных"), 404

    return jsonify(offer.to_dict()), 200


@user_blueprint.route('/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        user = User(
            id=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            email=data.get('email'),
            role=data.get('role'),
            phone=data.get('phone'),
            role_id=data.get('role_id')
        )
        db.session.add(user)
        db.session.commit()

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)

    return jsonify(user.to_dict()), 200


@user_blueprint.route('/users/<uid>', methods=['DELETE'])
def del_user(uid):
    user = User.query.get(uid)
    if user is None:
        return jsonify(f"по указанному id={uid} нет данных в базе данных"), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(user.to_dict())

@user_blueprint.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    user = User.query.get(uid)
    data = request.json

    try:
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.age = data.get('age')
        user.email = data.get('email')
        user.role = data.get('role')
        user.phone = data.get('phone')
        user.role_id = data.get('role_id')

        db.session.add(user)
        db.session.commit()

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)

    return jsonify(user.to_dict()), 200

@user_blueprint.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    try:
        order = Order(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            address=data.get('address'),
            price=data.get('price'),
            customer_id=data.get('customer_id'),
            executor_id=data.get('executor_id')
        )
        db.session.add(order)
        db.session.commit()

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e), 404

    return jsonify(order.to_dict()), 200


@user_blueprint.route('/orders/<oid>', methods=['DELETE'])
def del_order(oid):
    order = Order.query.get(oid)
    if order is None:
        return jsonify(f"по указанному id={oid} нет данных в базе данных"), 200

    db.session.delete(order)
    db.session.commit()

    return jsonify(order.to_dict())

@user_blueprint.route('/orders/<oid>', methods=['PUT'])
def update_order(oid):
    order = Order.query.get(oid)
    data = request.json
    date_start = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
    date_end = datetime.strptime(data.get('end_date'), "%Y-%m-%d").date()

    try:
        order.name = data.get('name')
        order.description = data.get('description')
        order.start_date = date_start
        order.end_date = date_end
        order.address = data.get('address')
        order.price = data.get('price')
        order.customer_id = data.get('customer_id')
        order.executor_id = data.get('executor_id')

        db.session.add(order)
        db.session.commit()

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)

    return jsonify(order.to_dict()), 200


@user_blueprint.route('/offers', methods=['POST'])
def add_offer():
    data = request.json
    try:
        offer = Offer(
            id=data.get["id"],
            order_id=data.get["order_id"],
            executor_id=data.get["executor_id"]
        )
        db.session.add(offer)
        db.session.commit()

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)

    return jsonify(offer.to_dict()), 200


@user_blueprint.route('/offers/<ofid>', methods=['DELETE'])
def del_offer(ofid):
    offer = Offer.query.get(ofid)
    if offer is None:
        return jsonify(f"по указанному id={ofid} нет данных в базе данных"), 200

    db.session.delete(offer)
    db.session.commit()

    return jsonify(offer.to_dict())

@user_blueprint.route('/offers/<oid>', methods=['PUT'])
def update_offer(oid):
    offer = Offer.query.get(oid)
    data = request.json

    try:
        offer.order_id = data.get('order_id')
        offer.executor_id = data.get('executor_id')

        db.session.add(offer)
        db.session.commit()

    except IntegrityError as e:
        error_message = str(e.orig)
        if "NOT NULL constraint failed" in error_message:
            # Извлекаем имя поля
            field_name = error_message.split(":")[-1].strip()
            return (f"Ошибка: поле '{field_name}' не заполнено. Пожалуйста, заполните это поле.")
        else:
            return("Произошла ошибка целостности данных:", e)

    return jsonify(offer.to_dict()), 200

