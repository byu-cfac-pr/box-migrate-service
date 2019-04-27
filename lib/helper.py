class RunningTotal:
    def __init__(self, msg):
        self.count = -1
        self.msg = msg
        self.next()

    def next(self):
        self.count += 1
        print(self.msg, self.count, end='\r')