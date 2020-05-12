import csv
from pprint import pprint

class Clasifier:
    def __init__(self, filename):
        self.filename = filename
        self.header = []
    
    def unique_vals(self,column, rows):
        return set([row[column] for row in rows])

    def count_vals(self, rows):
        columns = {}

        for row in rows:
            key = row[0]
            if key not in columns:
                columns[key] = 0
            columns[key] += 1
                
        return columns

    def partition(self, question, rows):
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

    def ask(self):
        with open(self.filename, newline="") as csvfile:
            csvread = csv.reader(csvfile)
            self.header = csvread.__next__()
            rows = []
            for row in csvread:
                # print(row)
                rows.append(list(row))
        
        # self.gini_histo = self.gini(rows)
        print(self.find_split(rows))


    def gini_index(self, rows):
        
        rows_histo = self.count_vals(rows)
        gini = 1

        for key in rows_histo:
            probability = rows_histo[key] / len(rows)
            gini -= probability**2
        
        return gini

    def find_split(self, rows):
        max_gain = int(0)
        uncertainty = self.gini_index(rows)
        optimal_question = None

        for column in range(len(rows[1])):
            if column == 0:
                continue
            uniques = self.unique_vals(column, rows)
            
            for val in uniques:
                question = Question(self.header, column, val)
                true_rows, false_rows = self.partition(question, rows)

                if len(true_rows) == 0 or len(false_rows) == 0:
                    continue

                gain = self.information_gain(true_rows, false_rows, uncertainty )

                if gain > max_gain:
                    max_gain = gain
                    optimal_question = question
                
        return max_gain, optimal_question
    
    def information_gain(self, true, false, uncertainty):
        prob = len(true) / (len(true) + len(false))
        gain = uncertainty - (prob * self.gini_index(true)) - ((1-prob) * self.gini_index(false))
        return gain


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
    # q = Question(classify.header, 3, "1")
    # pprint(classify.gini_histo)
    # print(q)
    # print(len(classify.partition(q)[0]), len(classify.partition(q)[1]))
    # classify.gini(classify.partition(q)[0])
    classify.ask()
