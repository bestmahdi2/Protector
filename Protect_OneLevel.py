from os import walk, rename, path, sep, chdir, listdir
from random import randint, choice

class Private:
    def __init__(self, dest):
        self.charList = ["[", "]", "{", "}", "@", "#", "$", "%", "^", "&", "!", ";"]
        self.forbidden = ["alaki.py", "zzz.py", "Protect.py"]

        chdir(dest)

        self.hidder()

    def hidder(self):
        lister = listdir('.')

        special = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"
        seps = "." + sep

        if "zzz" in lister:
            rename(seps + "zzz", seps + special)
            chdir(special)
            self.lock()

        elif "sd" in lister:
            rename(seps + "sd", seps + special)
            chdir(special)
            self.lock()

        elif special in lister:
            rename(seps + special, seps + "sd")
            chdir("sd")
            self.unlock()

    def lock(self):
        for (dirpath, dirname, filenames) in walk("."):
            for filename in filenames:
                if filename not in self.forbidden:
                    absulpathR = path.abspath(sep.join([dirpath, filename]))

                    nameList = list(filename)

                    x = 0

                    while len(filename)*1.5 > x:
                        character = choice(self.charList)
                        number = randint(0, len(nameList) - 1)

                        nameList.insert(number, character)

                        x += 1

                    name = "".join(nameList)

                    rename(absulpathR, absulpathR.replace(filename, name))

    def unlock(self):
        for (dirpath, dirname, filenames) in walk("."):
            for filename in filenames:
                if filename not in self.forbidden:
                    absulpathR = path.abspath(sep.join([dirpath, filename]))

                    nameList = []

                    fileList = list(filename)

                    for file in fileList:
                        if file not in self.charList:
                            nameList.append(file)

                    name = "".join(nameList)

                    rename(absulpathR, absulpathR.replace(filename, name))


P = Private("D:\\MY Projects\\Python\\Protect\\")
