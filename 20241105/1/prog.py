import sys

class Omnibus:
    cnt = {}
    cnt_set = set()
    def __setattr__(self, name, value):
        if not name.startswith("_"):
            if name in Omnibus.cnt:
                Omnibus.cnt[name] += 1
            else:
                Omnibus.cnt[name] = 1
        self.cnt_set.add(name)

    def __getattr__(self, name):
        if not name.startswith("_"):
            return Omnibus.cnt.get(name, 0)

    def __delattr__(self, name):
        if name in self.cnt_set:
            self.cnt_set.remove(name)
            if name in Omnibus.cnt:
                if Omnibus.cnt[name] == 1:
                    del Omnibus.cnt[name]
                else:
                    Omnibus.cnt[name] -= 1

exec(sys.stdin.read())
