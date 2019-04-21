import json

from api_gateway_lambda_proxy.response import JsonProxyResponse


def test_json_proxy_response():
    resp_sans_body = JsonProxyResponse(204)
    assert resp_sans_body.to_raw() == {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json'
        },
        'multiValueHeaders': {},
        'isBase64Encoded': False
    }

    body = {
        'name': 'Tom',
        'age': 10
    }
    resp_with_body = JsonProxyResponse(200, body)
    assert resp_with_body.to_raw() == {
        'statusCode': 200,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        },
        'multiValueHeaders': {},
        'isBase64Encoded': False
    }
