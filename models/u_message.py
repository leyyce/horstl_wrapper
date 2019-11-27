from copy import deepcopy
from email.message import EmailMessage
from email import message_from_bytes


class UMessage(EmailMessage):

    def __init__(self, bytes_: bytes = None):
        if bytes_ is None:
            super().__init__()
        else:
            msg = message_from_bytes(bytes_)
            self.__dict__ = msg.__dict__.copy()
        self.from_ = self["From"]
        self.to = self["To"]
        self.reply_to = self["Reply-To"]
        self.message_id = self["Message-ID"]
        self.date = self["Date"]
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
        for charset in UMessage._get_charsets_(self):
            t = t.decode(charset)
        if type(t) == bytes:
            t = t.decode()
        return t

    def __str__(self):
        msg_str = ("~" * 65 + "\n")
        msg_str += f'Message {self.message_id} from {self.date}\n\n' \
                   f'FROM: {self.from_}\n' \
                   f'TO: {self.to}\n'
        msg_str += f'REPLY TO: {self.reply_to}\n' if self.reply_to is not None else f''
        msg_str += f'SUBJECT: {self.subject}\n\n' \
                   f'{self.body}\n'
        msg_str += ("~" * 65)
        return msg_str
