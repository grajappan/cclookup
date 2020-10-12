from flask import Response, Flask
from flask_restful import Api, Resource
from flask_api import status
from lookup import apiConvert, apiDiag, health
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Counter, Histogram
import time
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
        start = time.time()
        gdict['CCRequests'].inc()
        ret = apiConvert(cc)
        if ret == 'Country code not valid':
            return "Failed to retrieve Country", status.HTTP_406_NOT_ACCEPTABLE
        else: 
            end = time.time()
            gdict['CCRequests_hist'].observe(end - start)
            return ret, status.HTTP_200_OK
class CCLDiag(Resource):
    def get(self):
        ret = apiDiag()
        if (ret == 'Unable to get diagnostics'):
            return "Failed to get diagnostics", status.HTTP_408_REQUEST_TIMEOUT
        else: 
            return ret, status.HTTP_200_OK

class CCLMetrics(Resource):
    def get(self):
        res = []
        for k,v in gdict.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res,mimetype="text/plain")

gdict = {}
gdict['CCRequests'] = Counter('convert_requests_total','The total number of Country Code Convert requests')
gdict['CCRequests_hist'] = Histogram('convert_request_duration_seconds','Historgram for the duration in seconds', buckets=(1,2,3,4,5,float('inf')))


api.add_resource(CCLHealth, "/health")
api.add_resource(CCLConvert, "/convert/<string:cc>")
api.add_resource(CCLDiag, "/diag")
api.add_resource(CCLMetrics, "/metrics")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4080')
