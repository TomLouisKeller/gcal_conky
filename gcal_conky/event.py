from datetime import datetime


class Event:

    def __init__(self, name: str, start: datetime, end: datetime):
        self.name = name
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start
