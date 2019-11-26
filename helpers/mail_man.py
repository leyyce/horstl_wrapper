import imaplib
import email


class MailMan:

    def __init__(self, fd_number: str, password: str):
        self.mail_box = imaplib.IMAP4_SSL("mail.hs-fulda.de")
        self.mail_box.login(fd_number, password)
        self._ai_number = fd_number
        self._password = password

    def log_out(self):
        self.mail_box.close()
        self.mail_box.logout()

    def print_all_messages(self):
        self.mail_box.select()
        typ, data = self.mail_box.search(None, 'ALL')
        for num in data[0].split():
            typ, data = self.mail_box.fetch(num, '(RFC822)')
            mail = email.message_from_bytes(data[0][1])
            body = MailMan._get_body(mail)
            subject = mail["Subject"]
            if type(body) == bytes:
                print(f'Message {num.decode()}\n{subject}\n\n{body.decode()}\n')
            else:
                print(f'Message {num.decode()}\n{subject}\n\n{body}\n')
            print("-" * 25)
        # print(self.mail_box.lsub())
        self.log_out()

    @staticmethod
    def _get_charsets_(mail_):
        charsets = set({})
        for c in mail_.get_charsets():
            if c is not None:
                charsets.update([c])
            return charsets

    @staticmethod
    def _get_body(mail_):
        while mail_.is_multipart():
            mail_ = mail_.get_payload()[0]
        t = mail_.get_payload(decode=True)
        for charset in MailMan._get_charsets_(mail_):
            t = t.decode(charset)
        return t
