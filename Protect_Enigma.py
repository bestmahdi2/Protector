from os import walk, rename, path, sep, chdir, listdir


class Enigma:
    def main(self, text):

        self.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.+-=_@#$%&[]{},;!~123456789"
        self.r1 = ";%5=lmOQnLd@$W8v3R7qx!~bKp#+gC]hIeVJ{zow-_,U}tFiX491asYPGNA2r[.M6yDjuHkBfEZ&TcS"
        self.r2 = "%c5rSnDv9f+_#-1lGMiRae7tH[jYJ2&~6@g,Os4UI$ypVQk=uEFhZbLXoN{K.8wPqxm]3B}zT;WC!Ad"
        self.r3 = "z%EGq_+aAl~jVKU7nt6$u.HWsfLdi=eSy!RT2]C@,xJgo[cB-YZv}PF39O4;Qw#5pbk1m8MXD{h&NIr"

        plain = text
        cipher = ""
        self.state = 0

        for char in plain:
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
    def __init__(self, dest):
        self.forbidden = ["alaki.py", "zzz.py", "Protect.py"]

        self.E = Enigma()

        chdir(dest)

        self.hidder()

    def hidder(self):
        lister = listdir('.')

        special = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"
        seps = "." + sep

        if "zzz" in lister:
            rename(seps + "zzz", seps + special)
            chdir(special)
            self.locker()

        elif "sd" in lister:
            rename(seps + "sd", seps + special)
            chdir(special)
            self.locker()

        elif special in lister:
            rename(seps + special, seps + "sd")
            chdir("sd")
            self.locker()

    def locker(self):
        for (dirpath, dirname, filenames) in walk("."):
            for filename in filenames:
                if filename not in self.forbidden:
                    absulpathR = path.abspath(sep.join([dirpath, filename]))

                    name = self.E.main(filename)

                    print(filename, name, sep="   ")

                    rename(absulpathR, absulpathR.replace(filename, name))

    # def unlock(self):
    #     for (dirpath, dirname, filenames) in walk("."):
    #         for filename in filenames:
    #             if filename not in self.forbidden:
    #                 absulpathR = path.abspath(sep.join([dirpath, filename]))
    #
    #                 name = self.E.main(filename)
    #
    #                 print(filename, name, sep="   ")
    #
    #                 rename(absulpathR, absulpathR.replace(filename, name))


P = Private("D:\\MY Projects\\Python\\Protect\\")
# E = Enigma(";mwp#s9qh") #"hihihi.hi")
