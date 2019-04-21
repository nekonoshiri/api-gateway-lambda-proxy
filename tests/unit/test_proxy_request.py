import json

from api_gateway_lambda_proxy.request import ProxyRequest


def test_proxy_request():
    resource = '/{proxy+}'
    path = '/hello/world'
    httpMethod = 'POST'
    headers = {'Content-Type': 'application/json'}
    multiValueHeaders = {'Content-Type': ['application/json']}
    queryStringParameters = {'name': 'me'}
    multiValueQueryStringParameters = {'name': ['me']}
    pathParameters = {'proxy': 'hello/world'}
    stageVariables = {'name': 'value'}
    requestContext = {
        'accountId': '12345678912',
        'resourceId': 'roq9wj',
        'stage': 'testStage',
        'requestId': 'deef4878-7910-11e6-8f14-25afc3e9ae33',
        'identity': {
          'cognitoIdentityPoolId': None,
          'accountId': None,
          'cognitoIdentityId': None,
          'caller': None,
          'apiKey': None,
          'sourceIp': '192.168.196.186',
          'cognitoAuthenticationType': None,
          'cognitoAuthenticationProvider': None,
          'userArn': None,
          'userAgent': 'PostmanRuntime/2.4.5',
          'user': None
        },
        'resourcePath': '/{proxy+}',
        'httpMethod': 'POST',
        'apiId': 'gy415nuibc'
    }
    body = "{\r\n\t\"a\": 1\r\n}"
    body_dict = {'a': 1}
    isBase64Encoded = False

    event = {
        'resource': resource,
        'path': path,
        'httpMethod': httpMethod,
        'isBase64Encoded': isBase64Encoded
    }

    req = ProxyRequest.from_event(event)
    assert req.resource == resource
    assert req.path == path
    assert req.httpMethod == 'POST'
    assert req.headers == {}
    assert req.multiValueHeaders == {}
    assert req.queryStringParameters == {}
    assert req.multiValueQueryStringParameters == {}
    assert req.pathParameters == {}
    assert req.stageVariables == {}
    assert req.requestContext == {}
    assert req.body == None
    assert req.isBase64Encoded == isBase64Encoded

    event['body'] = body
    event['headers'] = headers
    event['multiValueHeaders'] = multiValueHeaders
    event['queryStringParameters'] = queryStringParameters
    event['multiValueQueryStringParameters'] = multiValueQueryStringParameters
    event['pathParameters'] = pathParameters
    event['stageVariables'] = stageVariables
    event['requestContext'] = requestContext

    req = ProxyRequest.from_event(event)
    assert req.headers == headers
    assert req.multiValueHeaders == multiValueHeaders
    assert req.queryStringParameters == queryStringParameters
    assert req.multiValueQueryStringParameters == \
        multiValueQueryStringParameters
    assert req.pathParameters == pathParameters
    assert req.stageVariables == stageVariables
    assert req.requestContext == requestContext
    assert req.body.get() == body
    assert req.body.load_as_json() == body_dict
