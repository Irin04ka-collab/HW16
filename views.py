"""
Здесь реализуем представления для API
"""

from flask import Blueprint, jsonify
from model_db import *

# Создаем Blueprint для маршрутов пользователей
user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    result = []
    for user in User.query.all():
        result.append(user.to_dict())

    return jsonify(result), 200


@user_blueprint.route('/users/<int:uid>')
def get_one_user(uid):
    return f"User {uid}"


@user_blueprint.route('/orders')
def get_orders():
    return "orders"


@user_blueprint.route('/orders/<int:oid>')
def get_one_order(oid):
    return f"order {oid}"


@user_blueprint.route('/offers')
def get_offers():
    return "offers"


@user_blueprint.route('/offers/<int:ofid>')
def get_one_offer(ofid):
    return f"offer {ofid}"




