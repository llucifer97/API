#get links of image and send to remote server

import json
import pymongo
from flask import Flask,request
from flask_restful import Resource, Api
from flask_restful import reqparse
from pymongo import MongoClient
from natsort import natsorted, ns
import sys



app = Flask(__name__)
api = Api(app)

cluster = MongoClient("mongodb+srv://ayush:1234@cluster0-iyhwx.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["url"]
print("app is running................")


class URL(Resource):
    def get(self,user):
        parser = reqparse.RequestParser()

        parser.add_argument('user')
        data = parser.parse_args()
        results = collection.find({"user": user})
        db_results = []
        for result in results:
            db_results.append(result)
        return db_results

 #       return {'item': None}, 404action='append'

    def post(self,user):
        parser = reqparse.RequestParser()
        parser.add_argument('url',action='append')
        parser.add_argument('_id',type=str)

 #       parser.add_argument()
        data = parser.parse_args()
        item = {'user': user,'url': data['url'],'_id': data['_id']}
        try:
            collection.insert_one(item)
        except pymongo.errors.DuplicateKeyError:
            pass

        return item,201




api.add_resource(URL,'/<path:user>/url')
#api.add_resource(URL,'/<path:name>')
#api.add_resource(URL,'/urls')



#if __name__ == '__main__':
app.run()


















