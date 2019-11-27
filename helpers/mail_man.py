import imaplib
from models.uni_mail import UniMail


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
            mail = UniMail(data[0][1])
            body = mail.body
            subject = mail.subject
            print(f'Message {num.decode()}\n{subject}\n\n\t{body}\n')
            print("~" * 65)
        # print(self.mail_box.lsub())
