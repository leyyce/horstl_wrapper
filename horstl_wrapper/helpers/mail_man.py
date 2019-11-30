from imaplib import IMAP4_SSL

from imbox import Imbox
from ssl import create_default_context

from horstl_wrapper.models import UMessage


class MailMan(Imbox):

    def __init__(self, fd_number: str, password: str):
        try:
            super().__init__('mail.hs-fulda.de',
                             username=fd_number,
                             password=password,
                             ssl=False,
                             ssl_context=create_default_context(),
                             starttls=True)
            self.logged_in = True
        except IMAP4_SSL.error:
            self.logged_in = False
        self.fd_number = fd_number

    def get_all_messages(self) -> list:
        self._refresh()
        return [UMessage(message, uid) for uid, message in self.messages()]

    def get_unread_messages(self) -> list:
        self._refresh()
        return [UMessage(message, uid) for uid, message in self.messages(unread=True)]

    def search_for_subject(self, subject: str) -> list:
        self._refresh()
        return [UMessage(message, uid) for uid, message in self.messages(subject=subject)]

    def search_for_sender(self, sender: str) -> list:
        self._refresh()
        return [UMessage(message, uid) for uid, message in self.messages(sent_from=sender)]

    def logout(self):
        super().logout()
        self.fd_number = None
        self.password = None
        self.username = None
        self.logged_in = False

    def connection_active(self) -> bool:
        try:
            status, message = self.connection.check()
            if status == "OK":
                return True
            return False
        except IMAP4_SSL.error:
            return False

    def reauthenticate(self, fd_number: str, password: str):
        self.__init__(fd_number, password)

    def _refresh(self):
        if not self.connection_active():
            self.reauthenticate(self.fd_number, self.password)

    def __del__(self) -> None:
        if self.logged_in:
            self.logout()
