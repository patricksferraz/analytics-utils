from analytics_utils.lang import phrases, words, langs


class Lang:
    _phrases = phrases
    _words = words
    _langs = langs

    def __init__(self, lang: str = "pt"):
        """Constructor of Lang class

        Keyword Arguments:
            lang {str} -- Language for use (default: {"pt"})
        """
        self.lang = lang

    def phrases(self) -> [str]:
        """Function for return all familiar phrases

        Returns:
            [str] -- Keys of phrases
        """
        return self._phrases.keys()

    def phrase(self, phrase: str, complement=None) -> str:
        """Function for return one phrase with complement

        Arguments:
            phrase {str} -- Choice phrase

        Keyword Arguments:
            complement {Any} -- Complement of phrase (default: {None})

        Raises:
            ValueError: Unsupported phrase

        Returns:
            str -- Phrase
        """
        if phrase not in self._phrases:
            word = self._words["phrase"]["en"]
            raise ValueError(f"{self._phrases['unsupported']['en'](word)}")
        return self._phrases[phrase][self.lang](complement)

    def words(self):
        """Function for return all familiar words

        Returns:
            [str] -- Keys of words
        """
        return self._words.keys()

    def word(self, word):
        """Function for return one word

        Arguments:
            phrase {str} -- Choice word

        Raises:
            ValueError: Unsupported word

        Returns:
            str -- Word
        """
        if word not in self._words:
            word = self._words["word"]["en"]
            raise ValueError(f"{self._phrases['unsupported']['en'](word)}")
        return self._words[word][self.lang]

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        if lang not in self._langs:
            word = self._words["lang"]["en"]
            raise ValueError(f"{self._phrases['unsupported']['en'](word)}")
        self._lang = lang
