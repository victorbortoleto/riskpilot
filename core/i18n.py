from languages.pt import translations as pt
from languages.en import translations as en
from languages.es import translations as es


class SafeTranslations(dict):
    def __missing__(self, key):
        return key


LANGUAGES = {
    "Português": pt,
    "English": en,
    "Español": es,
}


def get_translations(language):
    base = pt.copy()
    selected = LANGUAGES.get(language, pt)

    base.update(selected)

    return SafeTranslations(base)
