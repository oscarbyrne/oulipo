import spacy.en

nlp = spacy.en.English()


class DocFrame(object):

    def __init__(self, tokens):
        self.tokens = list(tokens)

    @property
    def nouns(self):
        return DocFrame(t for t in self.tokens if t.is_noun)

    @property
    def verbs(self):
        return DocFrame(t for t in self.tokens if t.is_verb)

    @property
    def adjectives(self):
        return DocFrame(t for t in self.tokens if t.is_adjective)

    @property
    def notable(self):
        return DocFrame(t for t in self.tokens if t.is_notable)

    @property
    def people(self):
        return DocFrame(t for t in self.tokens if t.is_person)


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.tokens[key]
        else:
            return DocFrame(t for t in self.tokens if t.lower == key.lower())

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        self.tokens[key].string = value


    def __str__(self):
        return "[" + ", ".join([str(token) for token in self.tokens]) + "]"

    def __repr__(self):
        return str(self)


class MutableToken(object):

    def __init__(self, parent, i):
        self.parent = parent
        self.i = i

    @property
    def token(self):
        return self.parent._doc[self.i]

    @property
    def string(self):
        return self.token.string

    @property
    def lower(self):
        return self.token.lower_

    @string.setter
    def string(self, value):
        self.parent.mutate_token(self.i, value)

    @property
    def is_noun(self):
        return self.token.pos_ == u'NOUN' and not self.is_person

    @property
    def is_verb(self):
        return self.token.pos_ == u'VERB'

    @property
    def is_adjective(self):
        return self.token.pos_ == u'ADJ'

    @property
    def is_notable(self):
        raise NotImplementedError

    @property
    def is_person(self):
        try:
            return self.token.ent_type_ == u'PERSON'
        except AttributeError:
            return False


    def __str__(self):
        return self.string

    def __repr__(self):
        return str(self)


class MutableDoc(DocFrame):

    def __init__(self, string):
        if isinstance(string, str):
            string = string.decode('utf-8')
        self._doc = nlp(string)
        for ent in reversed(self._doc.ents):
            ent.merge(ent.root.tag_, ent.root.lemma_, ent.label_)
        self.tokens = [MutableToken(self, i) for i in xrange(len(self._doc))]

    def mutate_token(self, i, value):
        strings = [token.string for token in self._doc]
        strings[i] = value
        self.__init__("".join(strings))