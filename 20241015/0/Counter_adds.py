from collections import Counter


def can_make_note_from_article(article: str, note: str) -> bool:
    article_words = article.split()
    note_words = note.split()
    article_counter = Counter(article_words)
    note_counter = Counter(note_words)
    result = note_counter - article_counter
    return not result


article = ""
while a := input():
    article += a
note = input()

if can_make_note_from_article(article, note):
    print("Можно составить записку")
else:
    print("Нельзя составить записку")
