uzbek_words = ['a', 'b', 'd', 'e', 'f', 'g', 'g\'', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'o\'', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'x', 'y', 'z', 'sh', 'ch', "'", 'yo', 'yu', 'ya']
cyrillic_words = ['а', 'б', 'д', 'е', 'ф', 'г', 'ғ', 'ҳ', 'и', 'ж', 'к', 'л', 'м', 'н', 'о', 'ў', 'п', 'қ', 'р', 'с',
                  'т', 'у', 'в', 'х', 'й', 'з', 'ш', 'ч', "ъ", 'ё', 'ю', 'я']


def latin_to_cyrillic(text: str):
    text = text.replace("o'", 'ў')
    text = text.replace("g'", 'ғ')
    text = text.replace("sh", 'ш')
    text = text.replace("ch", 'ч')
    text = text.replace("yo", 'ё')
    text = text.replace("yu", 'ю')
    text = text.replace("ya", 'я')
    for i in text:
        if i.isupper():
            for j in range(len(uzbek_words)):
                if i.lower() == uzbek_words[j].lower():
                    text = text.replace(i, cyrillic_words[j].upper())
        else:
            for j in range(len(uzbek_words)):
                if i == uzbek_words[j]:
                    text = text.replace(i, cyrillic_words[j])
    return text


def cyrillic_to_latin(text: str):
    for i in text:
        if i.isupper():
            for j in range(len(cyrillic_words)):
                if i.lower() == cyrillic_words[j].lower():
                    text = text.replace(i, uzbek_words[j].upper())
        else:
            for j in range(len(cyrillic_words)):
                if i == cyrillic_words[j]:
                    text = text.replace(i, uzbek_words[j])
    return text
