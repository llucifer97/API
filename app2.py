#get data of keypoints from mongodb
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

# reading json file
pose_doc = []
for i in range(5,10):

    with open('./wga_json/' + str(i) + '.json') as f:
        l = json.load(f)
        pose_doc.append(l)


cluster = MongoClient("mongodb+srv://ayush:1234@cluster0-iyhwx.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]

for i in range(5):
    try:
        w = natsorted(list(natsorted(list(l.items()))[0][1][0].items()))[7][1]
    except IndexError as e:
        print("no pose detected!")
        pass
    post1 = {
        "pose": pose_doc[i],
        "_id": str(i),
        "user": "leo"
    }
    try:
        collection.insert_one(post1)
    except pymongo.errors.DuplicateKeyError:
        pass


class keypoints(Resource):
    def get(self):

        results = collection.find({})
        db_results = []
        for result in results:
            db_results.append(result)
        return db_results

api.add_resource(keypoints,'/poses')
#if __name__ == '__main__':
app.run(port = 8000)


















