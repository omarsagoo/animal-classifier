import csv

class Clasifier:
    def __init__(self, filename):
        self.csvfile = open(filename, "r", newline="")
        self.csvread = csv.reader(self.csvfile)
        self.header = self.csvread.__next__()
        # self.columns_histo = self.count_vals()
    
    def unique_vals(self,column):
        return set([row[column] for row in self.csvread])

    def count_vals(self):
        counts = {}
        columns = {}

        for row in self.csvread:
            for index, column in enumerate(row):
                if self.header[index] not in columns:
                    columns[self.header[index]] = dict()
                if column not in columns[self.header[index]]:
                    columns[self.header[index]][column] = 0
                columns[self.header[index]][column] += 1
                
        return columns

    def partition(self, question):
        true_rows = []
        false_rows = []

        for row in self.csvread:
            if question.answer(row) is True:
                true_rows.append(row)
            else:
                false_rows.append(row)
            
        print(len(true_rows))


class Question:
    def __init__(self, header, column, value):
        self.column = column
        self.value = value        
        self.header = header

    def __repr__(self):
        return f"is {self.header[self.column]} true? "

    def answer(self, response):
        val = response[self.column]
        print(val,"==",  self.value, val == self.value)
        if val == self.value:
            return True
        return False
    

if __name__ == "__main__":
    classify = Clasifier("zoo.csv")
    q = Question(classify.header, 3, "1")
    print(q)
    print(classify.partition(q))
