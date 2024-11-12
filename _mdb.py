import os
import json

class Database:
    def __init__(self):
        self.images = self.load_images()
        self.movies = self.load_movies()
        self.users = self.load_users()
        self.ratings = self.load_ratings()
        #self.images = self.load_images()
        self.avg_ratings = self.compute_avg_ratings()


    # pre-load ratings
    def compute_avg_ratings(self):
        rating_sums = {}
        rating_counts = {}
        for rating in self.ratings:
            movie_id = rating["movie_id"]
            rating_sums[movie_id] = rating_sums.get(movie_id, 0) + rating["rating"]
            rating_counts[movie_id] = rating_counts.get(movie_id, 0) + 1

        avg_ratings = {movie_id: rating_sums[movie_id] / rating_counts[movie_id] for movie_id in rating_sums}
        return avg_ratings

    # read in movies
    def load_movies(self, filename="data/movies.dat"):
        movies = {}
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split("::")
                    movie_id = int(parts[0])
                    title = parts[1]
                    genres = parts[2]#.split('|')
                    movies[movie_id] = {"title": title, "genres": genres, "img": self.images.get(movie_id, "blank.png")}
            print(f"DEBUG: Loaded {len(movies)} movies.")
        else:
            print("DEBUG: movies.dat file not found.")
        return movies
    
    # read in images
    def load_images(self, filename="data/images.dat"):
        images = {}
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split("::")
                    movie_id = int(parts[0])
                    image_filename = parts[2]
                    images[movie_id] = image_filename
        return images

    # read in users
    def load_users(self, filename="data/users.dat"):
        users = {}
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split("::")
                    user_id = int(parts[0])
                    gender = parts[1]
                    age = int(parts[2])
                    occupation = int(parts[3])
                    zipcode = parts[4]
                    users[user_id] = {
                        "gender": gender,
                        "age": age,
                        "occupation": occupation,
                        "zipcode": zipcode
                    }
        return users

    # read in ratings
    def load_ratings(self, filename="data/ratings.dat"):
        ratings = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split("::")
                    user_id = int(parts[0])
                    movie_id = int(parts[1])
                    rating = int(parts[2])
                    ratings.append({"user_id": user_id, "movie_id": movie_id, "rating": rating})
        return ratings

