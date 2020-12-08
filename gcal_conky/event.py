from datetime import datetime


class Event:

    def __init__(self, name: str, start: datetime, end: datetime):
        self.name = name
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start

    def __str__(self):
        return f"{self.start}\t-\t{self.end}\t-\t{self.name}"
