import os
import fasttext
from settings import ROOT

fasttext.FastText.eprint = lambda x: None
lang_model = fasttext.load_model(os.path.join(ROOT, 'models', 'bin', 'langdetect.ftz'))


def detect(text: str) -> str:
    """Detect language with FastText."""
    pred = lang_model.predict(text)
    if pred and pred[0] and pred[0][0]:
        return pred[0][0][len('__label__'):]
    return ''
