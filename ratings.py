import cherrypy
import json

class RatingsController:
    def __init__(self, mdb):
        self.mdb = mdb

    def GET_ITEM(self, movie_id):
        movie_id = int(movie_id)

        movie_ratings = [rating["rating"] for rating in self.mdb.ratings if rating["movie_id"] == movie_id]
        
        if movie_ratings:
            avg_rating = sum(movie_ratings) / len(movie_ratings)
            response = {
                "result": "success",
                "movie_id": movie_id,
                "rating": avg_rating
            }
        else:
            response = {"result": "error", "message": "No ratings found for this movie"}

        return json.dumps(response)
