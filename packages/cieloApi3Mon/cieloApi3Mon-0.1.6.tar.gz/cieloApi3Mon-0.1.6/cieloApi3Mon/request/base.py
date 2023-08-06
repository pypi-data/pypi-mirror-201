import uuid, json

from requests import Request, Session

class Base(object):

    def __init__(self, merchant):

        self.merchant = merchant
        self.last_request = None
        self.last_response = None

    def send_request(self, method, uri, data=None, params=None):

        s = Session()

        body = data

        headers = {
            'User-Agent': "CieloEcommerce/3.0 Python SDK",
            'RequestId': str(uuid.uuid4()),
            'MerchantId': self.merchant.id,
            'MerchantKey': self.merchant.key
        }

        if not body:
            headers['Content-Length'] = '0'
        else:
            headers["Content-Type"] = "application/json"

            if not isinstance(data, dict):
                body = body.toJSON()

        req = Request(method, uri, data=body, headers=headers, params=params)

        self.last_request = req

        prep = s.prepare_request(req)

        response = s.send(prep)

        if 'json' in response.headers['Content-Type'].lower():
            answers = response.json()
        else:
            answers = [{
                'Code': str(response.status_code),
                'Message': response.text
            }]

        if response.status_code >= 400:
            errors = []

            for answer in answers:
                errors.append('\r\n * [%s] %s\r\n' % (answer['Code'], answer['Message']))

            data_send = json.loads(body or 'null')

            raise Exception('\r\n%s\r\nMethod: %s\r\nUri: %s\r\nData: %s' % (''.join(errors), method, response.url, json.dumps(data_send, indent=2)))

        self.last_response = answers
        return answers

    def get_last_request(self, print_out=False):

        if print_out:
            print("------------------------------")
            print("URL:")
            print(self.last_request.url)
            print("------------------------------")
            print("Method:")
            print(self.last_request.method)
            print("------------------------------")
            print("Header:")
            print(json.dumps(self.last_request.headers, indent=4))
            print("------------------------------")
            print("Body:")
            print(json.dumps(json.loads(self.last_request.data), indent=4))
            print("------------------------------")
            print("Response:")
            print(json.dumps(self.last_response, indent=4))
            print("------------------------------")

        return self.last_request