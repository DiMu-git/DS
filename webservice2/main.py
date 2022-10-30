from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
CORS(app)

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("movie")
task_post_args.add_argument("actor")
task_post_args.add_argument("country")
imageURL = "https://image.tmdb.org/t/p/original"

languageDic = {"German": "de", "French": "fr", "Irish": "ga", "Indonesian": "id", "Italian": "it", "Japanese": "ja",
               "Korean": "ko", "Latin": "la", "Spanish": "es", "Thai": "th", "Mandarin": "zh", "English": "en",
               "Cantonese": "cn", "Greek": "el"}


class Movie(Resource):

    ###############################################################
    # Function for getting data from TMDB for movie
    ###############################################################
    def connectTMDB(self, result):
        title = result[0]['title']
        overview = result[0]['overview']
        imagePath = f"{imageURL}{result[0]['backdrop_path']}"
        # popularity = result[0]['popularity']
        voteAverage = result[0]['vote_average']
        voteCount = result[0]['vote_count']
        genreID = result[0]['genre_ids']
        genreArray = self.getGenre(genreID)
        id = result[0]['id']
        homePage = self.getHomePage(id)
        return {"Title": title, "Overview": overview, "ImagePath": imagePath,
                "VoteAverage": voteAverage, "VoteCount": voteCount,
                "GenreArray": genreArray, "HomePage": homePage
                }

    ###############################################################
    # Function for getting home page url
    ###############################################################
    def getHomePage(self, id):
        url = f"http://api.themoviedb.org/3/movie/{id}"
        query_params = {"api_key": "0f5467ecb5bb6c537173a518a293eb62"}
        data = requests.get(url, params=query_params).json()
        return data["homepage"]

    ###############################################################
    # Function for getting genre of a specific movie
    ###############################################################
    def getGenre(self, genreID):
        endpoint = "http://api.themoviedb.org/3/genre/movie/list"
        query_params = {"api_key": "0f5467ecb5bb6c537173a518a293eb62"}
        genres = requests.get(endpoint, params=query_params).json()["genres"]
        returnArray = []
        for id in genreID:
            for genre in genres:
                if id == genre["id"]:
                    returnArray.append(genre["name"])
        return returnArray

    ###############################################################
    # Function for determining search type
    ###############################################################
    def getResult(self, movieName, actor, region):
        if movieName and not region:
            endpoint = "http://api.themoviedb.org/3/search/movie"
            query_params = {"api_key": "0f5467ecb5bb6c537173a518a293eb62", "query": movieName}
            data = requests.get(endpoint, params=query_params).json()
            if len(data['results']) == 0:
                return None
            result = data['results']
            return self.connectTMDB(result)
        elif movieName and region:
            endpoint = "http://api.themoviedb.org/3/search/movie"
            query_params = {"api_key": "0f5467ecb5bb6c537173a518a293eb62", "query": movieName,
                            "language": languageDic[region]}
            data = requests.get(endpoint, params=query_params).json()
            if len(data['results']) == 0:
                return None
            result = data['results']
            return self.connectTMDB(result)
        else:
            endpoint = "http://api.themoviedb.org/3/search/person"
            query_params = {"api_key": "0f5467ecb5bb6c537173a518a293eb62", "query": actor}
            data = requests.get(endpoint, params=query_params).json()
            if len(data['results']) == 0:
                return None
            result = data['results'][0]['known_for']
            return self.connectTMDB(result)

    ###############################################################
    # Post
    ###############################################################
    def post(self):
        args = task_post_args.parse_args()
        movieName, actor, region = args["movie"], args["actor"], args["country"]
        result = self.getResult(movieName, actor, region)
        return result


api.add_resource(Movie, '/movies/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port="5001", debug=True)
