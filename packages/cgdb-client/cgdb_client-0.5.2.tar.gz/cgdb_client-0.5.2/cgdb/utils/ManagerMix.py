import json

from cgdb.exceptions.EntityNotFound import EntityNotFoundException
import cgdb.config


class ManagerMix:
    def __init__(self, client):
        self._client = client

    def get(self, url=""):
        if cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB:
            print("GET: " + url)
        raw_content = self._client._session.get(url)

        if raw_content.status_code != 200:
            if raw_content.status_code == 404:
                content = json.loads(raw_content.content)
                raise EntityNotFoundException(content["code"], content["message"] + "\n Entity url: " + url)

        if cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB:
            print("GET finished: " + str(raw_content.status_code) + ", json parse start")

        content = json.loads(raw_content.content)

        if cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB:
            print("Json parse finished")

        return content

    def post(self, url="", data=""):
        if cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB:
            print("POST: " + url)
        raw_content = self._client._session.post(url, data)
        if cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB:
            print("POST finished, status code:" + str(raw_content.status_code))

        if raw_content.status_code != 200:
            if raw_content.status_code == 404:
                content = json.loads(raw_content.content)
                raise EntityNotFoundException(content["code"], content["message"] + "\n Entity url: " + url)

        return raw_content

    def delete(self, url=""):
        raw_content = self._client._session.delete(url)
        print(raw_content.status_code)
        if raw_content.status_code != 200:
            if raw_content.status_code == 404:
                content = json.loads(raw_content.content)
                raise EntityNotFoundException(content["code"], content["message"] + "\n Entity url: " + url)

        return raw_content
