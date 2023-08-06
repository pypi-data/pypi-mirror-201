class Student(object):
    def __init__(self, username, uni):
        self.username = username
        self.uni = uni
        self.classes = []
        self.profs = []

    def _cmpkey(self):
        return self.uni

    def __str__(self) -> str:
        ret = ""
        ret += self.username + ", " + self.uni + ", ["
        for c in self.classes:
            ret += c + ", "
        ret += "], ["

        for p in self.profs:
            ret += p + ", "
        ret += "]"
        return ret

    def set_uni(self, u):
        self.uni = u

    def add_class(self, c):
        if c not in self.classes:
            self.classes.append(c)
            print("added!")
        else:
            print("already added")

    def remove_class(self, c):
        if c in self.classes:
            self.classes.remove(c)
            print("removed")
        else:
            print("class not found")

    def add_prof(self, p):
        if p not in self.profs:
            self.profs.append(p)
            print("added!")

    def remove_prof(self, p):
        if p in self.profs:
            self.profs.remove(p)
            print("removed")
        else:
            print("prof not found")

    def get_profs(self):
        return self.profs

    def get_classes(self):
        return self.classes
