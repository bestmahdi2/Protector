from platform import system as syst
from os import walk, rename, path, sep, chdir, listdir, popen, getcwd
from getpass import getpass


class Enigma:
    def main(self, text):

        self.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.+-=_@#$%&[]{},;!~123456789"
        self.r1 = ";%5=lmOQnLd@$W8v3R7qx!~bKp#+gC]hIeVJ{zow-_,U}tFiX491asYPGNA2r[.M6yDjuHkBfEZ&TcS"
        self.r2 = "%c5rSnDv9f+_#-1lGMiRae7tH[jYJ2&~6@g,Os4UI$ypVQk=uEFhZbLXoN{K.8wPqxm]3B}zT;WC!Ad"
        self.r3 = "z%EGq_+aAl~jVKU7nt6$u.HWsfLdi=eSy!RT2]C@,xJgo[cB-YZv}PF39O4;Qw#5pbk1m8MXD{h&NIr"

        forbiden = "آابپتثجچحخدذرزژسشصضظطغعفقکگلمنوهئی"

        plain = text
        cipher = ""
        self.state = 0

        for char in plain:
            if char not in forbiden:
                self.state += 1
                cipher += self.enigma_one_char(char)
                self.rotate_rotors()
            else:
                cipher += char

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
        self.E = Enigma()
        chdir(dest)

        self.main()
        chdir(pwd)

        if ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" in listdir("."):
            p = popen('attrib +h ' + ".\\.Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}")
            p.close()

        elif "sd" in listdir("."):
            p = popen('attrib -h ' + ".\\sd")
            p.close()

    def getpw(self) -> bool:
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

    def File_rename_hide(self, dirpath, nameF, mode):
        pwd = getcwd()

        absulpath = path.abspath(dirpath)
        absulpathR = path.abspath(sep.join([dirpath, nameF]))
        # print(absulpath, absulpathR, nameF , mode)

        if mode == "+":
            chdir(absulpath)
            p = popen('attrib +h \"{}\"'.format(nameF))
            p.close()

            name = self.E.main(nameF)
            rename(absulpathR, absulpathR.replace(nameF, name))

        else:
            name = self.E.main(nameF)
            rename(absulpathR, absulpathR.replace(nameF, name))

            chdir(absulpath)
            p = popen('attrib -h \"{}\"'.format(name))
            p.close()

        # back to Original folder and not broke the last : for_file_in_walk()
        chdir(pwd)

    def Folder_hide(self, dirpath, name, mode):
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

        for (dirpath, dirnames, filenames) in walk("."):
            for filename in filenames:
                if filename not in self.forbidden:
                    self.File_rename_hide(dirpath, filename, mode)

        for (dirpath, dirnames, filenames) in walk("."):
            for dirname in dirnames:
                self.Folder_hide(dirpath, dirname, mode)

        self.Find_folders(source)

    def Find_folders(self, loc):
        chdir(loc)
        dirs = [fol for fol in listdir(".") if path.isdir(fol)]
        if dirs:
            x = 0
            while x < len(dirs):
                name = self.E.main(dirs[x])
                rename(dirs[x], name)
                dirs[x] = name
                x += 1

            for fol in dirs:
                self.Find_folders(fol)
                chdir("..")


if __name__ == "__main__":
    if syst() == "Windows":
        try:
            P = Private(".")  # D:\\MY Projects\\Python\\Protect\\")
        except Exception as ex:
            input(ex)
    if syst() == "Linux":
        pass
