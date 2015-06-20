import json
import falcon


class JSONBodyParser(object):

    def process_request(self, req, res):
        if req.content_type == 'application/json':
            data = req.stream.read()
            if data:
                try:
                    req.context['data'] = json.loads(data)
                except ValueError:
                    message = "Request body is not valid 'application/json'"
                    raise falcon.HTTPBadRequest('Bad request', message)
