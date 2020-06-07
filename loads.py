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
        q_limit = int(request.args.get('limit', '5'))
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


@bp.route('/<id>', methods=['PUT', 'PATCH'])
def loads_put_patch(id):
    if request.method == 'PUT':
        if 'application/json' in request.accept_mimetypes:
            content = request.get_json()
            load_key = client.key(constants.loads, int(id))
            load = client.get(key=load_key)

            load.update({"weight": content["weight"],
                         "content": content["content"],
                         "delivery_date": content["delivery_date"],
                         "self": request.base_url + str(load.key.id)})

            client.put(load)

            res = make_response('See Other')
            res.mimetype = 'application/json'
            res.headers.set('Location', 'http://127.0.0.1/loads/' + str(load.id))
            res.status_code = 303
        else:
            res = make_response("Not Acceptable")
            res.mimetype = 'application/json'
            res.status_code = 406
            return res

    elif request.method == 'PATCH':
        if 'application/json' in request.accept_mimetypes:
            content = request.get_json()
            load_key = client.key(constants.loads, int(id))
            load = client.get(key=load_key)

            content_keys = content.keys()

            if 'weight' in content_keys:
                load.update({"weight": content["weight"]})
            elif 'content' in content_keys:
                load.update({"content": content["content"]})
            elif 'delivery_date' in content_keys:
                load.update({"delivery_date": content["delivery_date"]})
            else:
                res = make_response('')
                res.mimetype = 'application/json'
                res.status_code = 400
                return res

            client.put(load)

            res = make_response('See Other')
            res.mimetype = 'application/json'
            res.headers.set('Location', request.base_url + str(load.id))
            res.status_code = 303
            return res

        else:
            res = make_response("Not Acceptable")
            res.mimetype = 'application/json'
            res.status_code = 406
            return res
