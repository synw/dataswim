from collections import Counter
import pandas as pd
import nltk


class Text():
    """
    Class to process text
    """

    def flat_(self, col, nums=True):
        """
        Returns a flat representation of a column's values
        """
        try:
            res = ""
            i = 0
            vals = self.df[col].tolist()
            for el in vals:
                if nums is True:
                    res = res + str(i) + " " + el
                else:
                    res = res + el
                if i < (len(vals)-1):
                    res += " "
                i += 1
            return res
        except Exception as e:
            self.err(e, "Can not flat " + col)

    def mfw_(self, col, sw_lang="english", limit=100):
        """
        Returns a Dataswim instance with the most frequent words in a
        column exluding the most common stop words
        """
        df = self._mfw(col, sw_lang, limit)
        if df is None:
            self.err("Can not find most frequent words")
            return
        return self._duplicate_(df)

    def _mfw(self, col, sw_lang, limit):
        try:
            stopwords = nltk.corpus.stopwords.words(sw_lang)
            RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
            # replace '|'-->' ' and drop all stopwords
            words = (self.df[col]
                     .str.lower()
                     .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
                     .str.cat(sep=' ')
                     .split()
                     )
            df = pd.DataFrame(Counter(words).most_common(limit),
                              columns=['Word', 'Frequency']).set_index('Word')
        except Exception as e:
            self.err(e, "Can not finc most frequent words")
            return
        return df
