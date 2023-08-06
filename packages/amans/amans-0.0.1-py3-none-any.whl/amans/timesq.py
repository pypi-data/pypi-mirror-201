from datetime import datetime

class Test:
    def time(self):
        return datetime.now()
    

test = Test()
print(test.time())