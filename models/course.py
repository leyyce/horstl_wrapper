class Course:

    def __init__(self, ident: str, name: str, kind: str, group: str, time: str, frequency: str, time_period: str,
                 room_info: str, docent: str, status: str, warning: str):
        self.id = ident
        self.name = name
        self.kind = kind
        self.group = group
        self.time = time
        self.frequency = frequency
        self.time_period = time_period
        self.room_info = room_info
        self.docent = docent
        self.status = status
        self.warning = warning

    def to_string(self):
        course_str = f"\tID: {self.id}\n\tName: {self.name}\n\tTyp: {self.kind}\n\t" \
                     f"Parralelgruppe: {self.group}\n\tZeit: {self.time}\n\t" \
                     f"Frequenz: {self.frequency}\n\tZeitraum: {self.time_period}\n\t" \
                     f"Rauminfo: {self.room_info}\n\tDozent/in: {self.docent}\n\t" \
                     f"Status: {self.status}"
        if self.warning is not "None":
            course_str += f"\n\tWarnung: {self.warning}"
        return course_str
