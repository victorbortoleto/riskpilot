from languages.pt import translations as pt
from languages.en import translations as en
from languages.es import translations as es

LANGUAGES = {
    "Português": pt,
    "English": en,
    "Español": es,
}


def get_translations(language):
    return LANGUAGES.get(language, pt)
