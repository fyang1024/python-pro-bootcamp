class ArgsValidator:

    def __init__(self, args):
        self.args = args

    def validate(self):
        if len(self.args) != 3:
            return False
        elif self.__is_blank_str(self.args[1]):
            return False
        elif not self.__is_positive_int(self.args[2]):
            return False
        return True

    @staticmethod
    def __is_positive_int(arg):
        try:
            num = int(arg)
            return num > 0
        except ValueError:
            return False

    @staticmethod
    def __is_blank_str(arg):
        return len(arg.strip()) == 0
