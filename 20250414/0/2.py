import gettext

trans = gettext.translation("Wcount", "po", fallback = True)
_, ng = trans.gettext, trans.ngettext

while s := input():
    N = len(s.split())
    print(gettext.ngettext("Entered {} word", "Entered {} words", N).format(N))