from api_gateway_lambda_proxy import ProxyLambdaHandler
from api_gateway_lambda_proxy.proxy_response import JsonProxyResponse

handler = ProxyLambdaHandler(log_level = 'DEBUG')

@handler.error_handler
def error_handler(e):
    handler.logger.exception('Some error occured')
    return JsonProxyResponse(500, {
        'message': 'Some error'
    })

@handler.pre_handler
def pre_handler(request):
    print(request)
    return request

@handler.post('/hello')
def hello(request, context):
    greeting = request.queryStringParameters['greeting']
    name = request.body.load_as_json()['name']
    return JsonProxyResponse(200, {
        'result': f'{greeting}, {name}'
    })
