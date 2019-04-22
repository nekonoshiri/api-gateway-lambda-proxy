import sample


def test_sample():
    event = {
        'resource': '/hello',
        'path': '/hello',
        'httpMethod': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'multiValueHeaders': {'Content-Type': ['application/json']},
        'queryStringParameters': {'greeting': 'Hi'},
        'multiValueQueryStringParameters': {'greeting': ['Hi']},
        'pathParameters': None,
        'stageVariables': None,
        'requestContext': {},
        'body': "{\r\n\t\"name\": \"Tom\"\r\n}",
        'isBase64Encoded': False
    }
    context = None
    response = sample.handler(event, context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"result": "Hi, Tom"}'
