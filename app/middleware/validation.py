class RequestValidation(object):

    def process_resource(self, req, res, resource):
        if hasattr(resource, 'validate'):
            resource.validate(req.context['data'])
