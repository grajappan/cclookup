from flask import Flask
from flask_restful import Api, Resource
from flask_api import status
from lookup import apiConvert, apiDiag, health
app = Flask(__name__)
api = Api(app)

class CCLHealth(Resource):
    def get(self):
        ret = health()
        if ret == 200:
            return "Ok", status.HTTP_200_OK
        else:
            return "Unhealthy", status.HTTP_404_NOT_FOUND
class CCLConvert(Resource):
    def post(self, cc):
        ret = apiConvert(cc)
        if ret == 'Country code not valid':
            return "Failed to retrieve Country", status.HTTP_406_NOT_ACCEPTABLE
        else: 
            return ret, status.HTTP_200_OK
class CCLDiag(Resource):
    def get(self):
        ret = apiDiag()
        if (ret == 'Unable to get diagnostics'):
            return "Failed to get diagnostics", status.HTTP_408_REQUEST_TIMEOUT
        else: 
            return ret, status.HTTP_200_OK

api.add_resource(CCLHealth, "/health")
api.add_resource(CCLConvert, "/convert/<string:cc>")
api.add_resource(CCLDiag, "/diag")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4080')
