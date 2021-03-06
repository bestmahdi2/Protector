from platform import system as syst
from os import walk, rename, path, sep, chdir, listdir, popen, getcwd
from getpass import getpass
from random import choice
from sys import argv

from progressbar import ProgressBar, Percentage, Bar, ETA


class Enigma:
    def __init__(self, text):
        self.plain = text

    def __call__(self, text):
        self.plain = text

    def __str__(self):
        return self.main()

    def main(self):

        self.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.+-=_@#$%&[]{},;!~123456789"
        self.r1 = ";%5=lmOQnLd@$W8v3R7qx!~bKp#+gC]hIeVJ{zow-_,U}tFiX491asYPGNA2r[.M6yDjuHkBfEZ&TcS"
        self.r2 = "%c5rSnDv9f+_#-1lGMiRae7tH[jYJ2&~6@g,Os4UI$ypVQk=uEFhZbLXoN{K.8wPqxm]3B}zT;WC!Ad"
        self.r3 = "z%EGq_+aAl~jVKU7nt6$u.HWsfLdi=eSy!RT2]C@,xJgo[cB-YZv}PF39O4;Qw#5pbk1m8MXD{h&NIr"

        forbiden = "آابپتثجچحخدذرزژسشصضظطغعفقکگلمنوهئی"
        forbiden_additional = "战魔獸界王之地世"

        cipher = ""
        self.state = 0

        for char in self.plain:

            if char in forbiden:
                cipher += char
            elif char in forbiden_additional:
                cipher += char
            else:
                self.state += 1
                cipher += self.enigma_one_char(char)
                self.rotate_rotors()


        return cipher

    def reflector(self, char):
        return self.alphabet[len(self.alphabet) - self.alphabet.rfind(char) - 1]

    def enigma_one_char(self, char):
        if char == " ":
            return "^"

        elif char == "^":
            return " "

        else:

            c1 = self.r1[self.alphabet.rfind(char)]
            c2 = self.r2[self.alphabet.rfind(c1)]
            c3 = self.r3[self.alphabet.rfind(c2)]
            reflected = self.reflector(c3)
            c3 = self.alphabet[self.r3.rfind(reflected)]
            c2 = self.alphabet[self.r2.rfind(c3)]
            c1 = self.alphabet[self.r1.rfind(c2)]

            return c1

    def rotate_rotors(self):
        self.r1 = self.r1[1:] + self.r1[0]

        if self.state % 80:
            self.r2 = self.r2[1:] + self.r2[0]
        if self.state % (80 * 80):
            self.r3 = self.r3[1:] + self.r3[0]


class Private:
    def __init__(self, dest="."):
        self.forbidden = ["alaki.py", "zzz.py", "Protect.py"]
        pwd = getcwd()
        chdir(dest)

        self.main()
        chdir(pwd)

        if ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" in listdir("."):
            p = popen('attrib +h ' + ".\\.Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}")
            p.close()

        elif "sd" in listdir("."):
            p = popen('attrib -h ' + ".\\sd")
            p.close()

    @staticmethod
    def getpw() -> bool:
        pw = getpass(prompt="\nEnter Password > ")
        if pw == "badass 2":
            return True
        else:
            return False

    def main(self):
        lister = listdir('.')

        special = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"
        seps = "." + sep

        if "zzz" in lister:
            rename(seps + "zzz", seps + special)
            chdir(special)
            self.locker("hide", getcwd())

        elif "sd" in lister:
            rename(seps + "sd", seps + special)
            chdir(special)
            self.locker("hide", getcwd())

        elif special in lister:
            if self.getpw():
                rename(seps + special, seps + "sd")
                chdir("sd")
                self.locker("unhide", getcwd())

    @staticmethod
    def Additional_char(name):
        additional_char = ["战", "魔", "獸", "界", "王", "之", "地", "世"]
        namelist = list(name)
        if len([i for i in additional_char if i in name]) > 0:
            for i in additional_char:
                if i in namelist:
                    namelist.remove(i)
        else:
            selected = additional_char[choice(range(0, len(additional_char) - 1))]
            namelist.insert(choice(range(0, len(name) - 1)), selected)

        name = "".join(namelist)
        return name

    @staticmethod
    def File_rename_hide(dirpath, nameF, mode):
        pwd = getcwd()
        absulpath = path.abspath(dirpath)
        absulpathR = path.abspath(sep.join([dirpath, nameF]))
        # print("ok")

        if mode == "+":
            chdir(absulpath)
            p = popen('attrib +h \"{}\"'.format(nameF))
            p.close()

            name = str(Enigma(nameF))
            name = Private.Additional_char(name)
            rename(absulpathR, absulpathR.replace(nameF, name))

        else:
            name = str(Enigma(nameF))
            name = Private.Additional_char(name)
            rename(absulpathR, absulpathR.replace(nameF, name))

            chdir(absulpath)
            p = popen('attrib -h \"{}\"'.format(name))
            p.close()

        # back to Original folder and not broke the last : for_file_in_walk()
        chdir(pwd)

    @staticmethod
    def Folder_hide(dirpath, name, mode):
        pwd = getcwd()

        absulpath = path.abspath(dirpath)
        absulpathR = path.abspath(sep.join([dirpath, name]))

        if mode == "+":
            chdir(absulpath)
            p = popen('attrib +h \"{}\"'.format(name))
            p.close()

        else:
            chdir(absulpath)
            p = popen('attrib -h \"{}\"'.format(name))
            p.close()

        # back to Original folder and not broke the last : for_folder_in_walk()
        chdir(pwd)

    def locker(self, Hide_Unhide, source):
        mode = "+" if Hide_Unhide == "hide" else "-"

        # region ProgressBar
        fileCount = 0
        for (dirpath, dirnames, filenames) in walk("."):
            fileCount += len(filenames)
            fileCount += len(dirnames)

        print()
        widgets = ['Processing: ', Percentage(), ' ', Bar(marker='#', left='[', right=']'), ',  ', ETA(),
                   ',  Files\\Folders: ', str(fileCount)]
        bar = ProgressBar(widgets=widgets, maxval=fileCount)
        x = 1
        bar.start()
        # endregion

        for (dirpath, dirnames, filenames) in walk("."):
            for filename in filenames:
                if filename not in self.forbidden:
                    self.File_rename_hide(dirpath, filename, mode)
                    bar.update(x)
                    x += 1

        for (dirpath, dirnames, filenames) in walk("."):
            for dirname in dirnames:
                self.Folder_hide(dirpath, dirname, mode)
                bar.update(x)
                x += 1

        self.Find_folders(source)
        bar.finish()

    def Find_folders(self, loc):
        chdir(loc)
        dirs = [fol for fol in listdir(".") if path.isdir(fol)]
        if dirs:
            x = 0
            while x < len(dirs):
                name = str(Enigma(dirs[x]))
                name = Private.Additional_char(name)
                rename(dirs[x], name)
                dirs[x] = name
                x += 1

            for fol in dirs:
                self.Find_folders(fol)
                chdir("..")

class Repair:
    def __init__(self):
        print("Start Fixing ...")

        additional_char = ["战", "魔", "獸", "界", "王", "之", "地", "世"]
        # unhide files and folders
        mode = "-"

        for (dirpath, dirnames, filenames) in walk("."):
            for filename in filenames:
                if len([i for i in additional_char if i in filename]) > 0:
                    for i in additional_char:
                        if i in filename:
                            Private.File_rename_hide(dirpath, filename, mode)

        for (dirpath, dirnames, filenames) in walk("."):
            for dirname in dirnames:
                if len([i for i in additional_char if i in dirname]) > 0:
                    for i in additional_char:
                        if i in dirname:
                            Private.Folder_hide(dirpath, dirname, mode)

        print("Fixing finished. Files are unlocked.")


if __name__ == "__main__":
    if len(argv) == 1:
        if syst() == "Windows":
            try:
                P = Private(".")  # D:\\MY Projects\\Python\\Protect\\")
            except Exception as ex:
                input(ex)
        if syst() == "Linux":
            pass

    if len(argv) == 2:
        if argv[1] == "-fix":
            R = Repair()
        else:
            input("INPUT LIKE THIS:   Protector.exe -fix")

    if len(argv) > 2:
        input("INPUT LIKE THIS:   Protector.exe -fix")
