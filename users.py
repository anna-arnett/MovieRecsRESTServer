import cherrypy
import json

class UserController(object):
    def __init__(self, mdb):
        self.mdb = mdb

    def GET_ALL(self):
        users_list = []
        for user_id, user_data in self.mdb.users.items():
            users_list.append({
                "id": user_id,
                "gender": user_data.get("gender"),
                "age": user_data.get("age"),
                "occupation": user_data.get("occupation"),
                "zipcode": user_data.get("zipcode")
            })
        response = {"result": "success", "users": users_list}
        return json.dumps(response)

    def POST(self):
        ret = dict()
        ret['result'] = 'success'

        try:
            dat = cherrypy.request.body.read().decode('utf-8')
            dat = json.loads(dat)

            if self.mdb.users:
                new_id = max(self.mdb.users.keys()) + 1

            self.mdb.users[new_id] = {"gender": dat.get("gender", "Unknown gender"),
                                      "age": dat.get("age", "age unknown"),
                                      "occupation": dat.get("occupation", "unknown occupation"),
                                      "zipcode": dat.get("zipcode", "unknown zipcode")
                                      }
            ret["id"] = new_id
        except Exception as ex:
            ret["result"] = "failure"
            ret["message"] = str(ex)
            print(str(ex))
        return json.dumps(ret)

    def DELETE_ALL(self):
        self.mdb.users.clear()
        return json.dumps({"result": "success"})

    def GET_ITEM(self, user_id):
        ret = dict()
        user_id = int(user_id)
        if user_id in self.mdb.users:
            user = self.mdb.users[user_id]
            ret['id'] = user_id
            ret['gender'] = user.get("gender")
            ret['age'] = user.get("age")
            ret['occupation'] = user.get("occupation")
            ret['zipcode'] = user.get("zipcode")
        else:
            ret["result"] = "error"
            ret["message"] = "Movie not found"
        return json.dumps(ret)

    def PUT_ITEM(self, user_id):
        ret = dict()
        ret['result'] = 'success'
        
        try:
            dat = cherrypy.request.body.read().decode('utf-8')
            dat = json.loads(dat)
            user_id = int(user_id)
            self.mdb.users[user_id] = {"gender": dat.get("gender", "unknown gender"),
                                       "age": dat.get("age", "age unknown"),
                                       "occupation": dat.get("occupation", "unknown occupation"),
                                       "zipcode": dat.get("zipcode", "unknown zipcode")
                                      }
        except Exception as ex:
            ret['result'] = 'failure'
            ret['message'] = str(ex)
            print(str(ex))
        return json.dumps(ret)

    def DELETE_ITEM(self, user_id):
        ret = dict()
        user_id = int(user_id)
        ret['result'] = 'success'

        if user_id in self.mdb.users:
            del self.mdb.users[user_id]
        else:
            ret['result'] = 'error'
            ret['message'] = 'Movie not found'
        return json.dumps(ret)
