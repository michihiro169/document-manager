class Schedule():
    def __init__(self, name, tickets) -> None:
        self.name = name
        self.tickets = tickets

    def getName(self) -> str:
        return self.name

    def getTickets(self) -> list:
        return self.tickets
