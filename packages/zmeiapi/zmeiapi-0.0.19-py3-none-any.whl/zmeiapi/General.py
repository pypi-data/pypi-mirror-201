__version__ = "0.0.1"
__author__ = "Vlad Romanenko"


from Logger import logger


class General:
    def __init__(self):
        self.title = "None"
        self.acelib = "None"
        self.nfylib = "None"
        self.declib = "None"
        self.ures = 1
        self.include = None
        self.gcu = [0]
        self.bc = 1
        self.pop = [10000, 100, 20]
        self.src = "n"
        self.repro = 0
        self.shbuf = [0, 0]
        self.poi = None
        self.cmm = 1

        pass

    def _compile_title(self, file):
        file.write(f'set title \"{self.acelib}\" \n')

    def _compile_acelib(self, file):
        file.write(f'set acelib \"{self.acelib}\" \n')

    def _compile_nfylib(self, file):
        file.write(f'set nfylib \"{self.nfylib}\" \n')

    def _compile_declib(self, file):
        file.write(f'set declib \"{self.declib}\" \n')

    def _compile_ures(self, file):
        file.write(f'set ures {int(self.ures)} \n')

    def _compile_include(self, file):
        if self.include is None:
            pass
        elif type(self.include) is list:
            for f in self.include:
                file.write(f'include \"{f}\" \n')
        else:
            logger.error(f'Include attribute must have a list type')
            raise AttributeError(f'Include attribute must have a list type')

    def _compile_gcu(self, file):
        if self.gcu is None:
            pass
        elif (type(self.gcu) is list) or (type(self.gcu) is int):
            _line = 'set gcu '
            for f in self.gcu:
                _line += f'{f} '
            file.write(f'{_line} \n')
        else:
            logger.error(f'Gcu attribute must have a list type {type(self.gcu)}')
            raise AttributeError(f'Gcu attribute must have a list type')

    def _compile_bc(self, file):
        if self.bc is None:
            pass
        elif (self.bc == 0) or (self.bc == 1):
            file.write(f'set bc {self.bc} \n')
        else:
            logger.error(f'Bc attribute possible values must be 0 or 1')
            raise AttributeError(f'Bc attribute possible values must be 0 or 1')

    def _compile_pop(self, file):
        if self.pop is None:
            pass
        elif type(self.pop) is list:
            _line = 'set pop '
            for f in self.pop:
                if type(f) == int:
                    _line += f'{f} '
                else:
                    logger.error(f'Pop attribute must contain integer numbers')
                    raise AttributeError(f'Pop attribute must contain integer numbers')
            file.write(f'{_line} \n')
        else:
            logger.error(f'Pop attribute must have a list type')
            raise AttributeError(f'Pop attribute must have a list type')

    def _compile_src(self, file):
        if self.src is None:
            pass
        elif self.src == "n":
            file.write(f'set src {self.src} \n')
        else:
            logger.error(f'Src attribute possible values must be "n" or None')
            raise AttributeError(f'Src attribute possible values must be "n" or None')

    def compile(self, filename):
        with open(filename, 'w') as file:
            self._compile_title(file)
            file.write('\n')
            self._compile_acelib(file)
            self._compile_nfylib(file)
            self._compile_declib(file)
            file.write('\n')
            self._compile_ures(file)
            file.write('\n')
            self._compile_include(file)
            file.write('\n')
            self._compile_gcu(file)
            file.write('\n')
            self._compile_bc(file)
            file.write('\n')
            self._compile_pop(file)
            file.write('\n')
            self._compile_src(file)
            file.write('\n')


if __name__ == '__main__':
    general = General()

    general.compile('input')
