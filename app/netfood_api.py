import mongo
import flask
import json
from flask_cors import CORS, cross_origin
import os


app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

# appelle de la base de donnée



def get_collection():
    my_client = pymongo.MongoClient('mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"] + '/')
    db = my_client.list_database_names()
    hives = db.hives
    return hives


@app.route('/hives', methods=['GET'])  
@cross_origin() 
# 打印所有蜂巢信息
def page_query():
    args = flask.request.args
    page_size = args.get("limit")
    page_on = args.get("page")
    skip = page_size * (page_on - 1)
    coll = get_collection()
    page_record = coll.find().limit(page_size).skip(skip)
    
    return flask.Response(json.dumps(page_record), mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
