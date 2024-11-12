import cherrypy
import json

class RecommendationsController:
    def __init__(self, mdb):
        self.mdb = mdb

    def DELETE(self):
        self.mdb.ratings.clear()
        return json.dumps({"result": "success"})

    def GET_ITEM(self, user_id):
        #print("DEBUG: starting GET_ITEM for user_id:", user_id)
        user_id = int(user_id)
        user_rated_movies = {rating["movie_id"] for rating in self.mdb.ratings if rating["user_id"] == user_id}

        recommended_movie = None
        highest_rating = -1

        for movie_id, avg_rating in sorted(self.mdb.avg_ratings.items(), key=lambda x: (-x[1], x[0])):
            if movie_id not in user_rated_movies:
                highest_rating = avg_rating
                recommended_movie = {"movie_id": movie_id, "title": self.mdb.movies[movie_id]["title"], "rating": avg_rating}
                break


        #print("DEBUG: Ending GET_ITEM")

        if recommended_movie:
            result = {"result": "success", "movie_id": recommended_movie["movie_id"]}
            #print("DEBUG: recommendation result:", result)
        else:
            result = {"result": "error", "message": "No recommendation found"}
            #print("DEBUG: no recommendation found")

        return json.dumps(result)

    def PUT_ITEM(self, user_id):
        user_id = int(user_id)
        ret = {"result": "success"}

        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))
            movie_id = int(data.get("movie_id"))
            rating = data.get("rating")

            if movie_id not in self.mdb.movies or user_id not in self.mdb.users:
                return json.dumps({"result": "error", "message": "invalid user_id or movie_id"})

            found = False
            for r in self.mdb.ratings:
                if r["user_id"] == user_id and r["movie_id"] == movie_id:
                    r["rating"] = rating
                    found = True
                    break
            
            if not found:
                self.mdb.ratings.append({
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "rating": rating
                })

        except Exception as ex:
            ret = {"result": "failure", "message": str(ex)}

        return json.dumps(ret) 
