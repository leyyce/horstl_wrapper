from imbox.parser import Struct

from horstl_wrapper.helpers.base import ObjDict


class UMessage(Struct):

    def __init__(self, struct: Struct, uid: int):
        if not Struct:
            super().__init__()
        else:
            self.__dict__.update(struct.__dict__)
        html = self.body["html"]
        plain = self.body["plain"]
        self.uid = uid
        self.body = ObjDict()
        self.body.html = html
        self.body.plain = plain

    def __str__(self):
        msg_str = ("~" * 65 + "\n")
        msg_str += f'Message {self.message_id} from {self.date}\n\n'
        msg_str += UMessage._sent_x_to_str_preview(self.sent_from, "FROM")
        msg_str += UMessage._sent_x_to_str_preview(self.sent_to, "TO")
        msg_str += f'SUBJECT: {self.subject}\n\n'
        for body in self.body.plain:
            msg_str += f'{body}\n'
        msg_str += ("~" * 65)
        return msg_str

    @staticmethod
    def _sent_x_to_str_preview(list_: list, start: str = "", ceil: int = 5) -> str:
        str_ = ''
        min_ = min(len(list_), ceil)
        for index in range(0, min_):
            name = list_[index]["name"]
            email = list_[index]["email"]
            if index == 0:
                str_ += f'{start}:\t{name} <{email}>\n' if name != "" else f'{start}:\t<{email}>\n'
            else:
                str_ += f'\t{name} <{email}>\n' if name != "" else f'\t<{email}>\n'
        if min_ < len(list_):
            str_ += f'\t...\n'
        return str_

    # CAN BE REMOVED?
    #
    # def _get_charsets_(self):
    #     charsets = set({})
    #     for c in self.get_charsets():
    #         if c is not None:
    #             charsets.update([c])
    #         return charsets
    #
    # def _get_body_(self):
    #     msg = deepcopy(self)
    #     while msg.is_multipart():
    #         msg = msg.get_payload()[0]
    #     t = msg.get_payload(decode=True)
    #     for charset in UMessage._get_charsets_(self):
    #         t = t.decode(charset)
    #     if type(t) == bytes:
    #         t = t.decode()
    #     return t
