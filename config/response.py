from os import abort
from flask import make_response

def response(rescode, message, data):
    try:
        res = make_response({'status': rescode, 'message': message, 'data': data})
        res.mimetype = "application/json"
        return res
    except:
        abort(401)

