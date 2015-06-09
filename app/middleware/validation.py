class RequestValidation(object):

    def process_resource(self, req, res, resource):
        if req.method == 'POST':
            resource.validate_create(req.context['data'])
        if req.method == 'PUT':
            resource.validate_update(req.context['data'])
