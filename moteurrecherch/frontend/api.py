import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from elasticsearch import Elasticsearch

app = Flask(__name__)
api = Api(app)

NODE_NAME = 'si'
es = Elasticsearch(hosts="http://esmedias24.cloud.atlashoster.net:9200/", http_auth=("elastic", "Zo501nQV7AKxxxxxx"))

class ObjectApiResponse:
    def __init__(self, response):
        self.response = response

class ObjectApiResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectApiResponse):
            return obj.response
        return super().default(obj)

class Controller(Resource):
    def get(self):
        query = request.args.get("query", None)
        if query is None:
            return {"message": "Missing 'query' parameter"}, 400

        baseQuery = {
            "_source": [],
            "min_score": 0.5,
            "query": {
                "bool": {
                    "must": [
                        {
                            "wildcard": {
                                "post_title.keyword": {
                                    "value": "{}*".format(query),
                                    "case_insensitive": True
                                }
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "post_title.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }

        res = es.search(index=NODE_NAME, body=baseQuery)
        response_data = res['aggregations'] # Extraction des résultats de la recherche Elasticsearch
        return jsonify(response_data)


api.add_resource(Controller, '/autocomplete')

if __name__ == '__main__':
    app.run(debug=True, port=4000)

    