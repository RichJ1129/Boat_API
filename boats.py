import os
from google.cloud import datastore
from flask import Flask, request, Blueprint, make_response
import json
from google.oauth2 import id_token
from google.auth.transport import requests
import constants

client = datastore.Client()

bp = Blueprint('boats', __name__, url_prefix='/boats')
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


@bp.route('/', methods=['POST', 'GET'])
def boats_post_get():
    if request.method == 'POST' and 'application/json' in request.accept_mimetypes:
        user_sub = str(verify_jwt())
        if user_sub == "Unauthorized Error":
            res = make_response("Unauthorized Error")
            res.mimetype = 'application/json'
            res.status_code = 401
            return res
        else:
            content = request.get_json()
            new_boats = datastore.entity.Entity(key=client.key(constants.boats))

            new_boats.update({"name": content["name"],
                              "type": content["type"],
                              "length": content["length"],
                              "loads": 'NULL',
                              "owner": user_sub,
                              "self": request.base_url + str(new_boats.key.id)})

            client.put(new_boats)

            boat_result = {"id": str(new_boats.key.id),
                           "name": new_boats['name'],
                           "type": new_boats['type'],
                           "length": new_boats['length'],
                           "owner": user_sub,
                           "loads": "NULL",
                           "self": new_boats["self"]}

            res = make_response(json.dumps(boat_result))
            res.mimetype = 'application/json'
            res.status_code = 201

            return res

    elif request.method == 'GET' and 'application/json' in request.accept_mimetypes:
        query = client.query(kind=constants.boats)
        q_limit = int(request.args.get('limit', '5'))  # change to 5
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
        output = {"boats": results}
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


@bp.route('/<id>', methods=['PUT', 'PATCH'])
def boats_put_patch(id):
    if request.method == 'PUT':
        if 'application/json' in request.accept_mimetypes:
            user_sub = str(verify_jwt())
            if user_sub == "Unauthorized Error":
                res = make_response("Unauthorized Error")
                res.mimetype = 'application/json'
                res.status_code = 401
                return res
            else:
                content = request.get_json()
                boats_key = client.key(constants.boats, int(id))
                boats = client.get(key=boats_key)

                boats.update({"name": content["name"],
                              "type": content["type"],
                              "length": content["length"],
                              "self": request.base_url + str(boats.key.id)})

                client.put(boats)

                res = make_response('See Other')
                res.mimetype = 'application/json'
                res.headers.set('Location', 'http://127.0.0.1/boats/' + str(boats.id))
                res.status_code = 303
        else:
            res = make_response("Not Acceptable")
            res.mimetype = 'application/json'
            res.status_code = 406
            return res

    elif request.method == 'PATCH':
        if 'application/json' in request.accept_mimetypes:
            user_sub = str(verify_jwt())
            if user_sub == "Unauthorized Error":
                res = make_response("Unauthorized Error")
                res.mimetype = 'application/json'
                res.status_code = 401
                return res
            else:
                content = request.get_json()
                boats_key = client.key(constants.boats, int(id))
                boats = client.get(key=boats_key)

                content_keys = content.keys()

                if 'name' in content_keys:
                    boats.update({"name": content["name"]})
                elif 'type' in content_keys:
                    boats.update({"type": content["type"]})
                elif 'length' in content_keys:
                    boats.update({"length": content["length"]})
                else:
                    res = make_response('')
                    res.mimetype = 'application/json'
                    res.status_code = 400
                    return res

                client.put(boats)

                res = make_response('See Other')
                res.mimetype = 'application/json'
                res.headers.set('Location', request.base_url + str(boats.id))
                res.status_code = 303
                return res

        else:
            res = make_response("Not Acceptable")
            res.mimetype = 'application/json'
            res.status_code = 406
            return res


@bp.route('/<bid>/loads/<lid>', methods=['PUT', 'DELETE'])
def add_remove_load(bid, lid):
    if request.method == 'PUT':
        user_sub = str(verify_jwt())
        if user_sub == "Unauthorized Error":
            res = make_response("Unauthorized Error")
            res.mimetype = 'application/json'
            res.status_code = 401
            return res
        else:
            boats_key = client.key(constants.boats, int(bid))
            loads_key = client.key(constants.loads, int(lid))
            boats = client.get(key=boats_key)
            loads = client.get(key=loads_key)

            if boats is None:
                res = make_response('Boats Not Found')
                res.mimetype = 'application/json'
                res.status_code = 404
                return res
            elif loads is None:
                res = make_response('Loads Not Found')
                res.mimetype = 'application/json'
                res.status_code = 404
                return res

            if loads['boat'] == "NULL":
                loads.update({"boat": str(boats.key.id)})
                print(loads["boat"])
            else:
                res = make_response('Load is already on a boat')
                res.mimetype = 'application/json'
                res.status_code = 404
                return res


            if boats['loads'] == "NULL":
                loads_list = []
                loads_list.append(str(loads.key.id))
                boats.update({"loads": loads_list})
            else:
                loads_list = boats['loads']
                loads_list.append(str(loads.key.id))
                boats.update({"loads": loads_list})

            boat_result = {"id": str(boats.key.id),
                           "name": boats['name'],
                           "type": boats['type'],
                           "length": boats['length'],
                           "owner": boats['owner'],
                           "loads": boats['loads'],
                           "self": request.base_url + str(boats.key.id)}

            client.put(boats)
            client.put(loads)

            res = make_response(json.dumps(boat_result))
            res.mimetype = 'application/json'
            res.status_code = 200
            return res

    elif request.method == 'DELETE':
        user_sub = str(verify_jwt())
        if user_sub == "Unauthorized Error":
            res = make_response("Unauthorized Error")
            res.mimetype = 'application/json'
            res.status_code = 401
            return res
        else:
            boats_key = client.key(constants.boats, int(bid))
            loads_key = client.key(constants.loads, int(lid))
            boats = client.get(key=boats_key)
            loads = client.get(key=loads_key)

            if boats is None:
                res = make_response('Boat Not Found')
                res.mimetype = 'application/json'
                res.status_code = 404
                return res
            elif loads is None:
                res = make_response('Load Not Found')
                res.mimetype = 'application/json'
                res.status_code = 404
                return res

            loads_list = boats["loads"]

            loads_list.remove(str(loads.key.id))

            if not loads_list:
                loads_list = "NULL"
                boats.update({"loads": loads_list})
            else:
                boats.update({"loads": loads_list})

            loads.update({"boat": "NULL"})

            client.put(boats)
            client.put(loads)

            boat_result = {"id": str(boats.key.id),
                           "name": boats['name'],
                           "type": boats['type'],
                           "length": boats['length'],
                           "owner": boats['owner'],
                           "loads": boats['loads'],
                           "self": boats['self']}

            res = make_response(json.dumps(boat_result))
            res.mimetype = 'application/json'
            res.status_code = 200
            return res


@bp.route('/<id>', methods=['DELETE'])
def boats_delete(id):
    if request.method == 'DELETE':
        user_sub = str(verify_jwt())
        if user_sub == "Unauthorized Error":
            res = make_response("Unauthorized Error")
            res.mimetype = 'application/json'
            res.status_code = 401
            return res
        else:
            try:
                boats_key = client.key(constants.boats, int(id))
                boat_entity = client.get(boats_key)
                if boat_entity['owner'] == user_sub:
                    client.delete(boats_key)

                    query = client.query(kind=constants.loads)
                    query_iter = query.fetch()

                    for entity in query_iter:
                        if entity["boat"] == str(boat_entity.key.id):
                            entity.update({"boat": "NULL"})
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
            except:
                res = make_response('Forbidden')
                res.mimetype = 'application/json'
                res.status_code = 403
                return res




