import cherrypy
import json

class ResetController():
    def __init__(self, mdb):
        self.mdb = mdb

    def PUT(self):
        self.mdb.__init__()
        print(f"DEBUG: Database reset complete")

        return json.dumps({"result": "success"})

    def PUT_MOVIE(self, movie_id):
        movie_id = int(movie_id)
        filename = "data/movies.dat"
        movie_found = False

        if filename:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split("::")
                    if int(parts[0]) == movie_id:
                        title = parts[1]
                        genres = parts[2].split('|')
                        img = self.mdb.images.get(movie_id, "poster.jpg")

                        self.mdb.movies[movie_id] = {"title": title, "genres": genres, "img": img}
                        movie_found = True
                        break
        
        if movie_found:
            return json.dumps({"result": "success"})
        else:
            print(f"DEBUG: Movie with ID {movie_id} not found in movies.dat")
            return json.dumps({"result": "error", "message": "Movie not found"})
