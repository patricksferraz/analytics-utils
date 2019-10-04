from analytics_utils.lang import phrases, words, langs


class Lang:
    _phrases = phrases
    _words = words
    _langs = langs

    def __init__(self, lang: str = "pt"):
        """Constructor of Lang class

        Parameters
        ----------
        lang : str, optional
            Language for use, by default "pt"
        """
        self.lang = lang

    def phrases(self) -> [str]:
        """Function for return all familiar phrases

        Returns
        -------
        [str]
            Keys of phrases
        """
        return self._phrases.keys()

    def phrase(self, phrase: str, complement=None) -> str:
        """Function for return one phrase with complement

        Parameters
        ----------
        phrase : str
            Choice phrase
        complement : [type], optional
            Complement of phrase, by default None

        Returns
        -------
        str
            Phrase

        Raises
        ------
        ValueError
            Unsupported phrase
        """
        if phrase not in self._phrases:
            raise ValueError(
                f"{self.phrase('unsupported', self.word('phrase'))}"
            )
        return self._phrases[phrase][self.lang](complement)

    def words(self) -> [str]:
        """Function for return all familiar words

        Returns
        -------
        [str]
            Keys of words
        """
        return self._words.keys()

    def word(self, word: str) -> str:
        """Function for return one word

        Parameters
        ----------
        word : str
            Choice word

        Returns
        -------
        str
            Word

        Raises
        ------
        ValueError
            Unsupported word
        """
        if word not in self._words:
            raise ValueError(
                f"{self.phrase('unsupported', self.word('word'))}"
            )
        return self._words[word][self.lang]

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, lang: str):
        if lang not in self._langs:
            word = self._words["lang"]["en"]
            raise ValueError(f"{self._phrases['unsupported']['en'](word)}")
        self._lang = lang
