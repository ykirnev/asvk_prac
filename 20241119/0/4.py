class Sender:
    flag = True

    @classmethod
    def report(self):
        if self.flag:
            print('Greetings')
            self.flag = False
        else:
            print('Get away')

class Asker:
    @staticmethod
    def askall(lst):
        for i in lst:
            i.report()


b = Asker()
lst = [Sender() for i in range(10)]
b.askall(lst)