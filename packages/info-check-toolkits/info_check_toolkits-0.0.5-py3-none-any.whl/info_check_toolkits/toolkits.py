class Problem:
    def __init__(self, problem_type, column, msg):
        # 0 is empty and 1 is invalid
        self.problem_type = problem_type

        # Which colum do the problem occur in
        self.column = column

        # error info
        self.msg = msg


# Limits for columns
class Limit:
    def __init__(self, **parameters):
        """
        Available limit options

        1. num_limit(int): the limited length of the value
        2. no_space(bool): if space can be used
        3. is_date(bool): if the value has a format of YYYYMMDD
        4. value_range(List): which values are valid

        Default values for options(no limit)

        1. num_limit: 0
        2. no_space: True
        3. is_date: False
        4. value_range: []
        """
        self.default_option_values = {
            'num_limit': 0,
            'no_space': True,
            'is_date': False,
            'value_range': []
        }

        # set the default value of parameters
        for option in self.default_option_values.keys():
            if option not in parameters.keys():
                parameters[option] = self.default_option_values[option]

        # store the parameters
        self.parameters = parameters


class Processor:
    def __init__(self, columns, limits):
        # store the columns
        self.columns = columns

        # combine the columns and limits with a hash map
        self.limits = {}
        for i in range(len(self.columns)):
            self.limits[self.columns[i]] = limits[i]

    @staticmethod
    def check_date(date):
        # check the length
        if len(date) != 8:
            return False

        # check if there are only numbers
        for ch in date:
            if ch not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return False

        # get the year, month and day
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])

        # check if this date is valid
        if month in [1, 3, 5, 7, 8, 10, 12]:
            if day > 31:
                return False
        elif month in [4, 6, 9, 11]:
            if day > 30:
                return False
        elif month == 2:
            # leap year
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                if day > 29:
                    return False
            else:
                if day > 28:
                    return False
        else:
            return False

        return True

    def check_row(self, row):
        problems = []
        for column in self.columns:
            current_value = str(row[column])

            # check if the value is not empty
            if current_value == 'nan':
                new_problem = Problem(0, column, column + " is empty")
                problems.append(new_problem)

            # if value is not empty, check if it is valid
            else:
                current_limit = self.limits[column]

                # 1.check the length limit
                if current_limit.parameters['num_limit'] != 0:
                    num_limit = current_limit.parameters['num_limit']
                    if len(current_value) < num_limit:
                        new_problem = Problem(1, column, column + " is less than " + str(num_limit))
                        problems.append(new_problem)

                    elif len(current_value) > num_limit:
                        new_problem = Problem(1, column, column + " is more than " + str(num_limit))
                        problems.append(new_problem)

                # 2.check the space limit
                if current_limit.parameters['no_space']:
                    new_problem = None
                    for i in range(len(current_value)):
                        if current_value[i] == " ":
                            if i == 0:
                                new_problem = Problem(1, column, column + " has space in front of it")
                                break
                            else:
                                new_problem = Problem(1, column, column + " has space in the middle")
                                break
                    if new_problem is not None:
                        problems.append(new_problem)

                # 3.check the date limit
                if current_limit.parameters['is_date']:
                    if not self.check_date(current_value):
                        new_problem = Problem(1, column, column + " has wrong format")
                        problems.append(new_problem)

                # 4.check if the value is in range
                if len(current_limit.parameters['value_range']) != 0:
                    value_range = current_limit.parameters['value_range']
                    if current_value not in value_range:
                        new_problem = Problem(1, column, column + " is out of range")
                        problems.append(new_problem)

        # no problem
        if len(problems) > 0:
            res = problems
        elif len(problems) == 0:
            res = None
        return res
