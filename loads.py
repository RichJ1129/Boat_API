import os
from google.cloud import datastore
from flask import Flask, request, Blueprint, make_response
import json
from google.oauth2 import id_token
from google.auth.transport import requests
import constants

client = datastore.Client()

bp = Blueprint('loads', __name__, url_prefix='/loads')
client_id = '155864832310-rqqbf4p2d9pjgf2qttitn62h4duun8oh.apps.googleusercontent.com'
client_secret = "xeCqwxUqsKTZa2pmyKfFeTnL"


@bp.route('/', methods=['POST', 'GET'])
def loads_get_post():
    if request.method == 'POST':
        content = request.get_json()
        new_loads = datastore.entity.Entity(key=client.key(constants.loads))
        new_loads.update({'weight': content['weight'],
                          'content': content['content'],
                          'delivery_date': content['delivery_date'],
                          'boat': 'NULL'})

        client.put(new_loads)

        load_result = {"id": str(new_loads.key.id),
                       "weight": content['weight'],
                       "content": content['content'],
                       "delivery_date": content['delivery_date'],
                       "boat": "NULL",
                       "self": request.base_url + str(new_loads.key.id)}

        res = make_response(json.dumps(load_result))
        res.mimetype = 'application/json'
        res.status_code = 201

        return res
    elif request.method == 'GET':
        query = client.query(kind=constants.loads)
        q_limit = int(request.args.get('limit', '40'))
        q_offset = int(request.args.get('offset', '0'))
        l_iterator = query.fetch(limit=q_limit, offset=q_offset)
        pages = l_iterator.pages
        results = list(next(pages))
        if l_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
            e["self"] = request.base_url + str(e.key.id)
        output = {"loads": results}
        if next_url:
            output["next"] = next_url
        return json.dumps(output)
    else:
        return 'Method not recognized'


@bp.route('/<id>', methods = ['PUT', 'DELETE', 'GET'])
def loads_put_delete_get(id):
    if request.method == 'PUT':
        content = request.get_json()
        loads_key = client.key(constants.loads, int(id))
        loads = client.get(key=loads_key)
        loads.update({'weight': content['weight']})
        client.put(loads)
        return '', 200
    elif request.method == 'DELETE':
        key = client.key(constants.loads, int(id))
        client.delete(key)
        return '', 200
    elif request.method == 'GET':
        loads_key = client.key(constants.loads, int(id))
        loads = client.get(key=loads_key)
        return json.dumps(loads)
    else:
        return 'Method not recognized'







