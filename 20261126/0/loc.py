import locale
print(locale.getlocale())
print("йуцпеиепкмук".encode())
print("сацмуквпиккмк".encode("KOI8-R"))
ы = "йуцпеиепкмук".encode("KOI8-R")
print(ы.decode("KOI8-R"))

print('вопрос'.encode('CP1251').decode('KOI8-R'))
print('бМХЛЮМХЕ'.encode('KOI8-R').decode('CP1251'))
print('ОХРЮМХЕ'.encode('KOI8-R').decode('CP1251'))