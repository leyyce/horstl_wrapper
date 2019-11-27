from copy import deepcopy
from email.message import EmailMessage
from email import message_from_bytes


class UniMail(EmailMessage):

    def __init__(self, bytes_: bytes = None):
        if bytes_ is None:
            super().__init__()
        else:
            msg = message_from_bytes(bytes_)
            self.__dict__ = msg.__dict__.copy()
        self.subject = self["Subject"]
        self.body = self._get_body_()

    def _get_charsets_(self):
        charsets = set({})
        for c in self.get_charsets():
            if c is not None:
                charsets.update([c])
            return charsets

    def _get_body_(self):
        msg = deepcopy(self)
        while msg.is_multipart():
            msg = msg.get_payload()[0]
        t = msg.get_payload(decode=True)
        for charset in UniMail._get_charsets_(self):
            t = t.decode(charset)
        if type(t) == bytes:
            t = t.decode().replace("\n", "\n\t")
        else:
            t = t.replace("\n", "\n\t")
        return t
