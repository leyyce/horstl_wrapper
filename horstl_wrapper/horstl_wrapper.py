from horstl_wrapper.helpers import HorstlScrapper, MailMan


class HorstlWrapper:

    def __init__(self, fd_number: str, password: str):
        self.fd_number = fd_number
        self.password = password
        if self._verify_login():
            self.horstl = HorstlScrapper(fd_number, password)
            self.mailbox = MailMan(fd_number, password)
        else:
            raise ValueError("Username or password are incorrect.")

    def logout(self):
        self.fd_number = None
        self.password = None
        self.horstl = None
        self.mailbox = None

    def reauthenticate(self, fd_number: str, password: str):
        self.__init__(fd_number, password)

    def _verify_login(self) -> bool:
        return MailMan(self.fd_number, self.password).logged_in
