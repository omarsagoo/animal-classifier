import csv
from pprint import pprint

class Clasifier:
    def __init__(self, filename):
        self.filename = filename
        self.header = []
        self.columns_histo = self.count_vals()
    
    def unique_vals(self,column):
        return set([row[column] for row in self.csvread])

    def count_vals(self):
        counts = {}
        columns = {}
        
        with open(self.filename, newline="") as csvfile:
            csvread = csv.reader(csvfile)
            self.header = csvread.__next__()

            for row in csvread:
                for index, column in enumerate(row):
                    if index == 0:
                        continue
                    if self.header[index] not in columns:
                        columns[self.header[index]] = dict()
                    if column not in columns[self.header[index]]:
                        columns[self.header[index]][column] = 0
                    columns[self.header[index]][column] += 1
                
        return columns

    def partition(self, question):
        true_rows = []
        false_rows = []
        with open(self.filename, newline="") as csvfile:
            csvread = csv.reader(csvfile)
            self.header = csvread.__next__()

            for row in csvread:
                if question.answer(row) is True:
                    true_rows.append(row)
                else:
                    false_rows.append(row)
        return true_rows, false_rows


class Question:
    def __init__(self, header, column, value):
        self.column = column
        self.value = value        
        self.header = header

    def __repr__(self):
        return f"is {self.header[self.column]} {bool(self.value)}? "

    def answer(self, response):
        val = response[self.column]
        # print(val,"==",  self.value, val == self.value)
        if val == self.value:
            return True
        return False
    

if __name__ == "__main__":
    classify = Clasifier("zoo.csv")
    q = Question(classify.header, 3, "1")
    print(q)
    print(len(classify.partition(q)[0]), len(classify.partition(q)[1]))
    # pprint(classify.columns_histo)