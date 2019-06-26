class FIFO_Queue():
    def __init__(self):
        self.items = []

    def Push(self, newItem):
        self.items.append(newItem)

    def Pop(self):
        return self.items.pop(0)

    def Print(self):
        for item in self.items:
            print(item)

    def Contains(self, checkItem):
        return checkItem in self.items

    def IsEmpty(self):
        return len(self.items) == 0