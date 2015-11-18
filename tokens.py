import weakref

import spacy.en

import toolkit
import apis

nlp = spacy.en.English()


class MutableToken(object):

    def __init__(self, parent, i):
        self.parent = weakref.proxy(parent)
        self.i = i

    @property
    def _tkn(self):
        return self.parent._doc[self.i]

    @property
    def string(self):
        return self._tkn.orth_

    @property
    def lower(self):
        return self._tkn.lower_

    @string.setter
    def string(self, value):
        self.parent.mutate_token(self.i, value)

    @property
    def is_punctuation(self):
        return self._tkn.is_punct

    @property
    def is_noun(self):
        return self._tkn.pos_ == u'NOUN' and not self.is_person

    @property
    def is_verb(self):
        return self._tkn.pos_ == u'VERB'

    @property
    def is_adjective(self):
        return self._tkn.pos_ == u'ADJ'

    @property
    def is_notable(self):
        raise NotImplementedError

    @property
    def is_person(self):
        try:
            return self._tkn.ent_type_ == u'PERSON'
        except AttributeError:
            return False


    def images(self):
        raise NotImplementedError

    def gifs(self):
        raise NotImplementedError

    def definition(self):
        return apis.dictionary.define(self.lower)

    def clinaments(self):
        return toolkit.clinaments(self.lower)

    def rhymes(self):
        raise NotImplementedError

    def related(self):
        raise NotImplementedError


    def __str__(self):
        return self.string

    def __repr__(self):
        return str(self)



class MutableDocFrame(object):

    def __init__(self, tokens):
        self.tokens = list(tokens)

    @property
    def words(self):
        return MutableDocFrame(t for t in self.tokens if not t.is_punctuation)

    @property
    def nouns(self):
        return MutableDocFrame(t for t in self.tokens if t.is_noun)

    @property
    def verbs(self):
        return MutableDocFrame(t for t in self.tokens if t.is_verb)

    @property
    def adjectives(self):
        return MutableDocFrame(t for t in self.tokens if t.is_adjective)

    @property
    def notable(self):
        return MutableDocFrame(t for t in self.tokens if t.is_notable)

    @property
    def people(self):
        return MutableDocFrame(t for t in self.tokens if t.is_person)


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.tokens[key]
        else:
            return MutableDocFrame(t for t in self.tokens if t.lower == key.lower())

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        self.tokens[key].string = value


    def __len__(self):
        return len(self.tokens)

    def __str__(self):
        return "[" + ", ".join([str(token) for token in self.tokens]) + "]"

    def __repr__(self):
        return str(self)



class MutableDoc(MutableDocFrame):

    def __init__(self, string):
        string = toolkit.ensure_unicode(string)
        self._doc = nlp(string)
        for ent in reversed(self._doc.ents):
            ent.merge(ent.root.tag_, ent.root.lemma_, ent.label_)
        self.tokens = [MutableToken(self, token.i) for token in self._doc]

    def mutate_token(self, i, string):
        strings = [token.string for token in self._doc]
        strings[i] = string if self._doc[i+1].is_punct else string + " "
        self.__init__("".join(strings))


    def __str__(self):
        return self._doc.string

    def __repr__(self):
        return str(self)
