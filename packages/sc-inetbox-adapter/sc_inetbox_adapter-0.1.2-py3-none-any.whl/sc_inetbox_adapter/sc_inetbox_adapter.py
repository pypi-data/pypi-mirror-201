import json
import requests
import urllib3
import http
from .const import DEFAULT_HOST, DEFAULT_SSL, DEFAULT_VERIFY_SSL
from .errors import NoActiveSessionException


class InternetboxAdapter:

    def __init__(
            self,
            admin_password: str,
            ssl: bool = DEFAULT_SSL,
            host: str = DEFAULT_HOST,
            verify_ssl: bool = DEFAULT_VERIFY_SSL
        ) -> None:
        self._admin_password = admin_password
        self._host = host
        self._auth_token = None
        self._session = requests.Session()
        self._verify_ssl = verify_ssl

        if ssl:
            self._protocol = "https"
        else:
            self._protocol = "http"

    def create_session(self) -> http.HTTPStatus:
        payload = json.dumps({"service": "sah.Device.Information", "method": "createContext", "parameters": {
                             "applicationName": "webui", "username": "admin", "password": self._admin_password}})
        headers = {
            'Authorization': 'X-Sah-Login'
        }
        response = self._send_ws_request(payload, headers)
        if response.status_code == http.HTTPStatus.OK:
            self._auth_token = response.json()['data']['contextID']
        return response.status_code

    def logout_session(self) -> http.HTTPStatus:

        payload = json.dumps({"service": "sah.Device.Information",
                             "method": "releaseContext", "parameters": {"applicationName": "webui"}})
        headers = {
            'Authorization': 'X-Sah-Logout %s' % (self._auth_token)
        }
        response = self._send_auth_ws_request(payload, headers)
        return response.status_code

    def get_software_version(self) -> str:
        payload = json.dumps(
            {"service": "APController", "method": "getSoftWareVersion", "parameters": {}})
        response = self._send_ws_request(payload)
        if response.status_code == http.HTTPStatus.OK:
            return response.json()["data"]["version"]
        else:
            return "HTTP status code %d, check authentication" % (response.status_code)

    def get_device_info(self) -> json:
        headers = self._add_auth_header()
        payload = json.dumps({"parameters":{}})
        response = self._send_request("/sysbus/DeviceInfo:get", payload, headers)
        return response.json()["status"]

    def get_devices(self) -> json:

        payload = json.dumps({
            "service": "Devices",
            "method": "get",
            "parameters": {
                "expression": "lan and not self",
                "flags": "no_actions"
            }
        })

        response = self._send_auth_ws_request(payload)
        if response.status_code == http.HTTPStatus.OK:
            return response.json()["status"]
        else:
            return {"error": "Got HTTP status code %d, check authentication" % (response.status_code)}

    def _send_ws_request(self, payload: str, headers={}) -> requests.Response:
        path = "/ws"
        return self._send_request(path, payload, headers)

    def _send_auth_ws_request(self, payload: str, headers={}) -> requests.Response:
        headers = self._add_auth_header(headers)
        return self._send_ws_request(payload, headers)

    def _add_auth_header(self, headers={}):
        if not self._auth_token:
            raise NoActiveSessionException
        headers['X-Context'] = self._auth_token
        return headers

    def _send_request(self, path, payload, headers):
        url = "%s://%s%s" % (self._protocol, self._host, path)
        headers['Content-Type'] = 'application/x-sah-ws-4-call+json'
        if not self._verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # TODO exception handling
        response = self._session.post(
            url, headers=headers, data=payload, verify=self._verify_ssl)
        return response
