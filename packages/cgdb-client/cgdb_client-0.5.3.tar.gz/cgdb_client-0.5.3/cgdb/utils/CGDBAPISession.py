from requests import Response, Session


class CGDBAPISession(Session):
    def __init__(self, host, api_key, *args, **kwargs):
        self.host = host
        self.api_key = api_key
        super(CGDBAPISession, self).__init__(*args, **kwargs)

        self.headers.update({
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent': 'cgdb-python-client/{}'.format(0.1)
        })

   # def request(self, method, url: str | bytes | Text, *args, **kwargs) -> Response:
    def request(self, method, url, *args, **kwargs) -> Response:

        if '?' in url:
            url += "&"
        else:
            url += "?"
        url += "token={0}".format(self.api_key)

        return super().request(method, self.host + url, verify=False, *args, **kwargs)