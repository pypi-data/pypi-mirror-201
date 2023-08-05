class GPerror(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Ошибка в модуле graphical_password: {0} '.format(self.message)
        else:
            return 'Была вызвана ошибка в модуле graphical_password.'