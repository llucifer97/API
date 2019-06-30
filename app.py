#
import json
import pymongo
from flask import Flask,request
from flask_restful import Resource, Api
from flask_restful import reqparse
from pymongo import MongoClient
from natsort import natsorted, ns
import sys


# reading json file
with open('wga_json/34.json') as f:
    l = json.load(f)
print(l)

app = Flask(__name__)
api = Api(app)

cluster = MongoClient("mongodb+srv://ayush:1234@cluster0-iyhwx.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]
try:
    w = natsorted(list(natsorted(list(l.items()))[0][1][0].items()))[7][1]
except IndexError as e:
    print("no pose detected!")
    exit(1)
#results_int = [int(i) for i in w]

post1 = {
    "pose": w,
    "_id": 120965,
}
try:
    collection.insert_one(post1)
except pymongo.errors.DuplicateKeyError:
    pass

results = collection.find({"_id":120965})
db_results = []
for result in results:
    db_results.append(result)
    print(result)

items =[]

class URL(Resource):
    def get(self,name):
        for item in items:
            if item['name'] == name:
                return item
 #       return {'item': None}, 404action='append'

    def post(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument('url',action='append')
        parser.add_argument('_id', type=str)
 #       parser.add_argument()
        data = parser.parse_args()
        item = {'name': name,'url': data['url'],'_id': data['_id']}
        items.append(item)
        return items,201







api.add_resource(URL,'/<path:name>/url')
#api.add_resource(URL,'/<path:name>')
#api.add_resource(url_list,'/urls')


#if __name__ == '__main__':
app.run(port = 8080)


















