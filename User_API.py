# /user Endpoint created for User Authentications

import falcon, json
from waitress import serve
import base64
import redis


r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


class User:
    output = {}

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        self.output["username"] = r.hkeys('Auth_data')
        resp.body = json.dumps(self.output)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        data = {k.lower(): v for k, v in data.items()}

        if r.hexists('Auth_data', data['username']):
            resp.body = json.dumps("Ah - User already exists, choose a different username or "
                                   "contact system administrator :( ")
        else:
            r.hset('Auth_data', key=data['username'], value=data['password'])
            resp.body = json.dumps("Congratulations - New User Added to our system :) ")

    def on_put(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        data = {k.lower(): v for k, v in data.items()}
        if r.hexists('Auth_data', data['username']):
            r.hset('Auth_data', data['username'], data['password'])
            resp.body = json.dumps("Username updated in our system :) ")
        else:
            resp.body = json.dumps("User does not exists in our system :( ")


    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        data = {k.lower(): v for k, v in data.items()}
        if r.hexists('Auth_data', data['username']):
            r.hdel('Auth_data', data['username'])
            resp.body = json.dumps("User deleted from our system :) ")
        else:
            resp.body = json.dumps("User does not exists in our system :( ")


api = application = falcon.API()
api.add_route('/user', User())

serve(api, host='127.0.0.1', port=5555)
