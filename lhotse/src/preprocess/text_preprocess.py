import re

class AsrTextPreprocess:
    def __init__(self):
        self.punctuation = "!\"#$%&'()*+,-./:;“”‘’<=>?@[\]^_`{|}«»~—–。一，。"

    def remove_punctuation(self, text):
        punctuation = self.punctuation
        cleaned_text = re.sub(f'[{re.escape(punctuation)}]', ' ', text)
        return cleaned_text

    def remove_punctuation_without_accent(self, text):
        punctuation = self.punctuation
        punctuation = punctuation.replace('+','')
        cleaned_text = re.sub(f'[{re.escape(punctuation)}]', ' ', text)
        return cleaned_text

    def text_lower(self, text):
        return text.lower()

    def replace_e(self, text):
        return text.replace('ё','е')

    def replace_space(self, input_text):
        text = input_text
        while True:
            if text.find('  ') > -1:
                text = text.replace('  ',' ')
            else:
                break
        text = text.strip()
        return text

    def preprocess_asr(self, text, replace_space = True, replace_e = False, text_lower = True, remove_punct = True):
        new_text = text
        
        if remove_punct:
            new_text = self.remove_punctuation(new_text)
        if text_lower:
            new_text = self.text_lower(new_text)
        if replace_e:
            new_text = self.replace_e(new_text)
        if replace_space:
            new_text = self.replace_space(new_text)
        
        return new_text
