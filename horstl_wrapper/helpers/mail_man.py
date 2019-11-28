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
            _, self.folders = self.folders()
            self.logged_in = True
        except IMAP4_SSL.error:
            self.logged_in = False
        self._fd_number = fd_number

    def print_all_messages(self) -> None:
        all_messages = self.messages()
        for uid, message in all_messages:
            message = UMessage(message)
            print(str(message))
        # for num in data[0].split():
        #     typ, data = self.mail_box.fetch(num, '(RFC822)')
        #     message = UMessage(data[0][1])
        #     print(str(message))
        # print(self.mail_box.lsub())

    def __del__(self) -> None:
        if self.logged_in:
            self.logout()
