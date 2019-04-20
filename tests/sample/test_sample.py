import sample


def test_sample():
    event = {
        'resource': '/hello',
        'path': '/hello',
        'httpMethod': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': {'greeting': 'Hi'},
        'requestContext': {},
        'body': "{\r\n\t\"name\": \"Tom\"\r\n}",
        'isBase64Encoded': False
    }
    context = None
    response = sample.handler(event, context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"result": "Hi, Tom"}'
