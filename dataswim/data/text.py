from collections import Counter
import pandas as pd
import nltk


class Text():
    """
    Class to process text
    """

    def mfw_(self, col, sw_lang="english", limit=100):
        """
        Returns a Dataswim instance with the most frequent words in a
        column exluding the most common stop words
        """
        try:
            ds2 = self.new_(self._mfw(col, sw_lang, limit))
            return ds2
        except Exception as e:
            self.err(e, self.first, "Can not find most common words")

    def _mfw(self, col, sw_lang, limit):
        """
        Returns a dataframe with the most frequent words in a
        column exluding the most common stop words
        """
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
        return df
