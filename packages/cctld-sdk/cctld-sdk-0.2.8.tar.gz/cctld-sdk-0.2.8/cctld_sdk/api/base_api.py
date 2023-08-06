from cctld_sdk.api.decorator import auth_required
from cctld_sdk.common.types import CCTLDActions
from cctld_sdk.common.exceptions import (
    NginxForbiddenResponseError,
    CCTLDResponseError,
    NotAuthorizedError,
)

import requests
import xmltodict
from dicttoxml import dicttoxml


class Client(object):
    API_ENDPOINT = "/api/api_2_1.php"

    def __init__(
        self,
        url: str,
        login: str,
        password: str,
        verify_certs: bool = False,
        debug: bool = False,
    ) -> None:
        """Function summary
        Args:
            url (str): URL of the target cctld instance
            login (str): login
            password (str): password
            verify_certs (bool): True (default) to verify SSL certificates, False otherwise
            debug (bool): set to True to print debugging messages to stdout, defaults to False:

        Examples:

            >>> cctld = CCTLD("http://example.uz/", "login", "password")
            >>> print(cctld)
        """

        if not url.endswith("/"):
            url += "/"

        self.url = url + self.API_ENDPOINT
        self.login = login
        self.password = password
        self._session = None
        self._debug = debug
        self._verify_certs = verify_certs

    @auth_required
    def send_command(
        self, action: CCTLDActions, data: dict, root: str = "data"
    ) -> dict:
        payload = {
            "action": action.value,
            "data": dicttoxml({root: data}, root=False, attr_type=False),
        }
        if self._session is None:
            raise NotAuthorizedError()
        resp = self._session.post(self.url, data=payload)
        if resp.status_code == 403:
            raise NginxForbiddenResponseError(resp.content)

        content = self.get_successful_response_content(resp.content)
        return content

    def get_successful_response_content(self, content: str) -> bool:
        content = xmltodict.parse(content)
        if content["data"].get("msg", None) == "Вы не авторизированы":
            raise NotAuthorizedError()
        if not bool(int(content["data"].get("rcode", 1))):
            raise CCTLDResponseError(content)
        return content

    def auth(self) -> dict:
        data = {"sLogin": self.login, "sPass": self.password}
        self._session = requests.session()
        self._session.verify = self._verify_certs
        return self.send_command(action=CCTLDActions.AUTH, data=data)
