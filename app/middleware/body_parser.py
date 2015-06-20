import ujson as json
import falcon


class JSONBody(object):

    def process_request(self, req, res):
        if req.content_type != 'application/json':
            message = "Content-Type must be 'application/json'"
            raise falcon.HTTPBadRequest('Bad request', message)

        if req.method in ['POST', 'PUT']:
            try:
                req.context['data'] = json.loads(req.stream.read())
            except ValueError:
                message = "Request body is not valid 'application/json'"
                raise falcon.HTTPBadRequest('Bad request', message)

    def process_response(self, req, res, resource):
        if 'result' not in req.context:
            return
        res.body = json.dumps(req.context['result'])
