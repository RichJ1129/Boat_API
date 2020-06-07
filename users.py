from google.cloud import datastore
from flask import Flask, request, Blueprint, make_response
from google.oauth2 import id_token
from google.auth.transport import requests
import constants
import os
import json

client = datastore.Client()

bp = Blueprint('users', __name__, url_prefix='/users')
client_id = '155864832310-rqqbf4p2d9pjgf2qttitn62h4duun8oh.apps.googleusercontent.com'
client_secret = "xeCqwxUqsKTZa2pmyKfFeTnL"


def verify_jwt():
    user_header = str(request.headers['Authorization'])
    user_header = user_header[7::]

    try:
        req = requests.Request()

        id_info = id_token.verify_oauth2_token(
            user_header, req, client_id)

        return id_info['sub']
    except:
        return "Unauthorized Error"


@bp.route('', methods=['GET'])
def get_all_users():
    if request.method == "GET":
        query = client.query(kind=constants.users)
        q_limit = int(request.args.get('limit', '40'))  # change to 3
        q_offset = int(request.args.get('offset', '0'))
        l_iterator = query.fetch(limit=q_limit, offset=q_offset)
        pages = l_iterator.pages
        results = list(next(pages))
        if l_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        output = {"users": results}
        if next_url:
            output["next"] = next_url
        return json.dumps(output)

    else:
        res = make_response('Method Not Allowed')
        res.mimetype = 'application/json'
        res.status_code = 405
        return res


@bp.route('/<id>/boats', methods=['GET'])
def get_users(id):
    if request.method == "GET":
        user_sub = str(verify_jwt())
        if user_sub == "Unauthorized Error":
            res = make_response("Unauthorized Error")
            res.mimetype = 'application/json'
            res.status_code = 401
            return res
        else:
            query = client.query(kind=constants.boats)
            query_iter = query.fetch()

            user_boats = []

            for entity in query_iter:
                if entity['user'] == str(user_sub):
                    entity["id"] = entity.key.id
                    user_boats.append(entity)

            output = {"boats": user_boats}

            return output
