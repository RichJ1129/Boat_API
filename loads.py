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
                          'boat': 'NULL'
                          })

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

        res = make_response(json.dumps(output))
        res.mimetype = 'application/json'
        res.status_code = 200

        return res

    else:
        res = make_response('Method Not Allowed')
        res.mimetype = 'application/json'
        res.status_code = 405
        return res


@bp.route('/<id>', methods=['PUT', 'PATCH', 'GET'])
def loads_put_patch(id):
    if request.method == 'PUT':
        if 'application/json' in request.accept_mimetypes:
            content = request.get_json()
            load_key = client.key(constants.loads, int(id))
            load = client.get(key=load_key)

            load.update({"weight": content["weight"],
                         "content": content["content"],
                         "delivery_date": content["delivery_date"]
                         })

            client.put(load)

            res = make_response('')
            res.mimetype = 'application/json'
            res.status_code = 200
            return res
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
            elif "content" in content_keys:
                load.update({"content": content["content"]})
            elif "delivery_date" in content_keys:
                load.update({"delivery_date": content["delivery_date"]})
            else:
                res = make_response('')
                res.mimetype = 'application/json'
                res.status_code = 400
                return res

            client.put(load)

            res = make_response('')
            res.mimetype = 'application/json'
            res.status_code = 200
            return res

    elif request.method == 'GET':
        if 'application/json' in request.accept_mimetypes:
            loads_key = client.key(constants.loads, int(id))
            loads = client.get(key=loads_key)

            if loads == None:
                res = make_response('Not Found')
                res.mimetype = 'application/json'
                res.status_code = 404
                return res

            load_result = {"id": str(loads.key.id),
                           "weight": loads['weight'],
                           "content": loads['content'],
                           "delivery_date": loads['delivery_date'],
                           "boats": loads['boat'],
                           "self": request.base_url + str(loads.key.id)
                           }

            res = make_response(json.dumps(load_result))
            res.mimetype = 'application/json'
            res.status_code = 200
            return res

        else:
            res = make_response("Not Acceptable")
            res.mimetype = 'application/json'
            res.status_code = 406
            return res


@bp.route('/<id>', methods=['DELETE'])
def loads_delete(id):
    if request.method == 'DELETE' and 'application/json' in request.accept_mimetypes:
        load_key = client.key(constants.loads, int(id))
        load = client.get(load_key)
        client.delete(load_key)

        query = client.query(kind=constants.boats)
        query_iter = query.fetch()

        for entity in query_iter:
            if str(load.key.id) in entity["loads"]:
                loads_list = entity["loads"]
                loads_list.remove(str(load.key.id))
                if not loads_list:
                    loads_list = "NULL"
                    entity.update({"loads": loads_list})
                else:
                    entity.update({"loads": loads_list})
                client.put(entity)

        res = make_response('No Content')
        res.mimetype = 'application/json'
        res.status_code = 204
        return res
    else:
        res = make_response('Forbidden')
        res.mimetype = 'application/json'
        res.status_code = 403
        return res
