
class Middleware:

    def __init__(self, get_response):
        self.get_response= get_response

    def __call__(self, request):
        response= self.get_response(request)  
        api_request = {
            "Request": {
                "Scheme": request.scheme,
                "Path": request.path,
                "Path_Information" : request.path_info,
                "Method": request.method,
                "Encoding": request.encoding,
                "Content_Type": request.content_type,
                "Content_Params": request.content_params,
                "Host": request.get_host(),
                "Meta" : request.META,
                "Headers": request.headers,
                "Body": request.body,
            },
            "Response":{
                "Headers": response.headers,
                "Content": response.content
            }
        } 
        print(api_request)
        return response
