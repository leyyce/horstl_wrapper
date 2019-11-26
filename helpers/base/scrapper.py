from requests import Session


class Scrapper:

    def __init__(self, fd_number: str, fd_password: str, base_url: str):
        self.fd_number = fd_number
        self.fd_password = fd_password
        self._BASE_URL = base_url
        self._SESSION = None

    def _set_session(self, s: Session):
        self._SESSION = s
