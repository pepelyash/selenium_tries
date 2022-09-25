

class Wk:
    def __init__(self, log, pwd):
        self.log = log
        self.pwd = pwd
        self.tkn = 'none'
        self.ua = 'none'
        self.did = 'none'


class Ama:
    def __init__(self, amal):
        self.ts = 0
        self.log = 'none'
        self.pwd = 'none'
        self.tkn = 'none'
        self.ua = 'none'
        self.did = 'none'
        self.amal = amal
        self.wkid = 'none'
        self.isfr = True

    def set_issns(self, issns, snsval):
        setattr(self, issns, snsval)


class Au:
    def __init__(self):
        self.log = 'none'
        self.pwd = 'none'
        self.tkn = 'none'
        # self.ua = 'none'


class DbRecord:
    def __init__(self):
        self.ts = 0
        self.wklog = 'none'
        self.wkpwd = 'none'
        self.wktkn = 'none'
        self.wkid = 'none'
        self.ua = 'none'
        self.amal = 'none'
        self.aulog = 'none'
        self.aupwd = 'none'
        self.autkn = 'none'
        self.amar = 'none'
