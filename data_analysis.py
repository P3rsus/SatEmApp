""" This Script is used to get the data, remove outliers, analyse it
and separate it into lists """


class DataAnalysis():
    """ This class does what was mentioned above """

    def __init__(self, file_name):
        self.file_name = file_name
        ofile = open(self.file_name, "r")
        self.data = ofile.read()
        ofile.close()
        self.lines = len(self.data.split('\n'))
        self.cleaned_lines = 0
        self.amount_variables = self.detect_amount_variables()
        self.cleaned = False
        self.naming = ["" for _ in range(self.amount_variables)]

    def detect_amount_variables(self, upper_limit=100, match=0.95):
        l = []
        with open(self.file_name, "r") as f:
            temp_data = f.read()
        lines_over = self.lines * match
        i = 1
        while upper_limit != i:
            self.amount_variables = i
            self.clean()
            lines = len(self.data.split("\n"))
            if lines > lines_over:
                return i
            l.append(lines)
            self.data = temp_data
            i += 1
        return l.index(max(l))+1

    def change_amount_variables(self, amount):
        self.amount_variables = amount
        if len(self.naming) > self.amount_variables:
            self.naming = self.naming[:self.amount_variables]
        else:
            self.naming += ["" for _ in range(self.amount_variables-len(self.naming))]

    def update(self, clean=False):
        """ Updates the data from the file """
        ofile = open(self.file_name, "r")
        self.data = ofile.read()
        ofile.close()
        self.lines = len(self.data.split('\n'))
        if clean:
            self.clean()
        else:
            self.cleaned = False

    def clean(self):
        """ Removes corrupted data """
        self.cleaned = True
        res = []
        prev_time = -1
        for i in self.data.split("\n"):
            temp = i.split(" ")
            try:
                int(temp[0])
                for i in temp:
                    float(i)
                if len(temp) == self.amount_variables and prev_time < float(temp[0]):
                    prev_time = float(temp[0])
                    res.append(temp)
            except TypeError:
                continue
            except ValueError:
                continue
        self.data = "\n".join([" ".join(i) for i in res])
        self.cleaned_lines = len(self.data.split('\n'))

    def line_read(self, am):
        """ Splits the data by lines into a list and returns it """
        return self.data.split("\n")[-am:]

    def val_read(self):
        """ Splits the data by lines and then by values into a list
        of lists and returns it """
        if not self.cleaned:
            self.clean()
        return list(zip(*[i.split(" ") for i in self.data.split("\n")]))

    def read_data(self):
        """ Returns the data from the file """
        return self.data