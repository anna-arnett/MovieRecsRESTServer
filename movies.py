import cherrypy
import json

class MovieController(object):
    def __init__(self, mdb):
        self.mdb = mdb

    def GET_ALL(self):
        movies_list = []
        for movie_id, movie_data in self.mdb.movies.items():
            movies_list.append({
                "id": movie_id,
                "title": movie_data.get("title"),
                "genres": movie_data.get("genres", []),
                "img": movie_data.get("img", "poster.jpg")
            }) 
        response = {"movies": movies_list, "result" : "success"}
        return json.dumps(response)
    
    def GET_ITEM(self, movie_id):
        ret = dict()
        movie_id = int(movie_id)
        #print(self.movies)
        if movie_id in self.mdb.movies:
            movie = self.mdb.movies[movie_id]
            ret['title'] = movie.get("title")
            ret['genres'] = movie.get("genres", "Unknown Genre")
            ret['result'] = "success"
            ret['id'] = movie_id
            ret['img'] = movie.get("img")
        else:
            ret["result"] = "error"
            ret["message"] = "Movie not found"
        return json.dumps(ret)

    def PUT_ITEM(self, movie_id):
        ret = dict()
        ret['result'] = 'success'
        
        try:
            dat = cherrypy.request.body.read().decode('utf-8')
            print("DEBUG: Data received in PUT_ITEM:", dat)
            dat = json.loads(dat)
            movie_id = int(movie_id)
            self.mdb.movies[movie_id] = {"title": dat.get("title", "Unknown Title"),
                                     "genres": dat.get("genres", "Unknown Genre"),
                                     "img": dat.get("img", "blank.png") }
        except Exception as ex:
            ret['result'] = 'failure'
            ret['message'] = str(ex)
            print("DEBUG: Exception in PUT_ITEM:", str(ex))
        return json.dumps(ret)

    def POST(self):
        ret = dict()
        ret['result'] = 'success'

        try:
            dat = cherrypy.request.body.read().decode('utf-8')
            dat = json.loads(dat)
            
            if self.mdb.movies:
                new_id = max(self.mdb.movies.keys()) + 1

            self.mdb.movies[new_id] = {"title": dat.get("title", "Unknown Title"),
                                   "genres": dat.get("genres", "Unknown Genre"),'''.split("|")'''
                                   "img": dat.get("img", "blank.png")
                                  }
            ret["id"] = new_id
        except Exception as ex:
            ret["result"] = "failure"
            ret["message"] = str(ex)
            print(str(ex))
        return json.dumps(ret)

    def DELETE_ALL(self):
        self.mdb.movies.clear()
        return json.dumps({"result": "success"})

    def DELETE_ITEM(self, movie_id): 
        movie_id = int(movie_id)
        ret = dict()
        ret["result"] = "success"

        if movie_id in self.mdb.movies:
            del self.mdb.movies[movie_id]
        else:
            ret["result"] = "error"
            ret["message"] = "Movie not found"
        return json.dumps(ret)
        
