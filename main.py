import csv
from pprint import pprint

class Clasifier:
    """Decision tree that goes through a csv file and makes predictions based on the set of attributes."""
    def __init__(self, filename):
        # takes in a csv file name as a parameter and stores it.
        self.filename = filename
        #  instantiate the header as an empty list. the header is the first row in the file.
        self.header = []
    
    def unique_vals(self,column, rows):
        """Returns a set of all the unique values in each column, most are binary ( 1, 0)
            This is used to check the gain on every value in the data set.
            Time Complexity:
                O(n) - where n is the number of rows in the dataset
            Space Complexity:
                O(k) - where k is the number of unique elements in each row
            Args:
                column - int; the index of the column to check for unique values
                rows    - array; the array of all the rows in the data set.
            Return:
                set - set; python set object that is storing all the unique values for a particular column"""
        return set([row[column] for row in rows])

    def count_vals(self, rows):
        """Creates a histogram of all the occurances in the data set for a particular outcome. 
            i.e. if looking for an animal { 'aardvark': 1, 'lion':1, ...} 
            this is used to help calculate the impurity, using the gini index, of the data set.
            Time Complexity:
                O(n) - where n is the number of different rows in the dataset
            Space Complexity:
                O(k) - where k is the number of unique elements inside the dataset.
            Args:
                rows - [array]; an array of arrays denoting all the different rows in the data set.
            Return:
                columns - dict; python dict object that is storing a histogram of all the unique rows. """
        columns = {}

        for row in rows:
            key = row[0]
            if key not in columns:
                columns[key] = 0
            columns[key] += 1
                
        return columns

    def partition(self, question, rows):
        """Helper method that splits the data set into two lists, one for all the questions that were answered correctly,
        another for all the false answers.
        Time Complexity:
            O(n) - where n is the number of different questions that can be asked.
        Space Complexity:
            O(n) - creates two lists that are equal in size to the original list
                        (n - true_rows) + (n - false_rows) where true_rows + false_rows = n
        Args:
            question  - Question object; the question to be asked
            rows        - the rows to be searched for all the correct answers
        Return:
            tuple(true_rows, false_rows) - tuple([], []); a tuple of two arrays. tuple[0] being all the rows that
                                                            were true, tuple[1] all rows that are false."""
        true_rows = []
        false_rows = []

        for row in rows:
            if question.answer(row) is True:
                true_rows.append(row)
            else:
                false_rows.append(row)
        return true_rows, false_rows

    def ask(self):
        """Method that asks the questions"""
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
        """Calculates the gini index of all of the rows in the dataset.
            Time Complexity:
                O(n) - where n is the number of rows inside the dataset
            Space Complexity:
                O(k) - creates a histogram of all the unique occurrances in the data set.
            Args:
                rows - [array]; list of lists that holds all of the data from the CSV file
                                        that we would like to get the gini index for
            Return:
                gini - float; the gini index of the values"""
        rows_histo = self.count_vals(rows)
        gini = 1

        for key in rows_histo:
            probability = rows_histo[key] / len(rows)
            gini -= probability**2
        
        return gini

    def find_split(self, rows):
        """Finds the question with the highest information gain in order to ask the most optimal question.
            Time Complexity:
                O(n^2) - where n is the number of rows and the number of attributes in the data set.
            Space Complexity:
                O(n) - creaets new data structures to store various information.
            Args:
                rows - [array]; all of the data that you would like to find a split in.
            Return:
                tuple(max_gain, optimal_question) - tuple(); a tuple holding the highest gain and
                                                                        the most optimal question to ask next, 
                                                                        stored as tuple()[0]: Gain, tuple()[1]: question """
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
        """Method to calculate the Information gain of a question in order to decide the most optimal to use.
            Time Complexity:
                O(n) - where n is the number of items in the data set.
            Space Complexity:
                O(n) - creates histograms for many different sets of data.
            Args:
                true            - [array]; an array of all the true rows in the dataset.
                false           - [array]; an array of all the false rows in the dataset.
                uncertainty - float; the current uncertainty of all the questions
            Return:
                gain - float; the information gain of the questions in the true/false lists. """
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
