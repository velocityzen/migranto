import datetime

class Printer:
    def __init__(self, out, format):
        self.out = out
        self.format = format

    def formatCell(self, data):
        if type(data) is datetime.datetime:
            return data.strftime('%Y-%m-%d %H:%M')
        else:
            return str(data)

    def printRow(self, row):

        print >> self.out, row[0].ljust(self.format[0] + 1),
        print >> self.out, self.formatCell(row[1]).rjust(self.format[1]) + '   ',
        print >> self.out, self.formatCell(row[2]).ljust(self.format[2]),
        print >> self.out