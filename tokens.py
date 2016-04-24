import weakref
import inspect

import numpy as np

import nlp
import toolkit
import apis



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

    @string.setter
    def string(self, value):
        self.parent.mutate_token(self.i, value)

    @property
    def lower(self):
        return self._tkn.lower_

    @property
    def notability(self):
        return - self._tkn.prob

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
        return self.notability > 10

    @property
    def is_person(self):
        try:
            return self._tkn.ent_type_ == u'PERSON'
        except AttributeError:
            return False

    @property
    def is_location(self):
        try:
            return self._tkn.ent_type_ in [u'FACILITY', u'GPE', u'LOC']
        except AttributeError:
            return False

    @property
    def is_group(self):
        try:
            return self._tkn.ent_type_ in [u'NORP', u'ORG']
        except AttributeError:
            return False

    @property
    def is_entity(self):
        return any([self.is_person, self.is_location, self.is_group])


    def fetch_images(self):
        raise NotImplementedError

    def fetch_gifs(self):
        raise NotImplementedError

    def fetch_definition(self):
        return apis.dictionary.define(self._tkn.lemma_)

    def fetch_clinaments(self):
        return toolkit.clinaments(self.lower)

    def fetch_similar(self):
        return toolkit.lexemes_ranked_by_similarity_to(self._tkn)


    def images(self):
        raise NotImplementedError

    def gifs(self):
        raise NotImplementedError


    def definition(self):
        try:
            return self._definition
        except AttributeError:
            self._definition = self.fetch_definition()
            return self.definition()

    def clinaments(self):
        try:
            return self._clinaments
        except AttributeError:
            self._clinaments = self.fetch_clinaments()
            return self.clinaments()

    def rhymes(self):
        try:
            return self._rhymes
        except AttributeError:
            self._rhymes = self.fetch_rhymes()
            return self.rhymes()

    def similar(self, number=5):
        try:
            return [lex.orth_ for lex in self._similar[:number]]
        except AttributeError:
            self._similar = self.fetch_similar()
            return self.similar()


    def __str__(self):
        return self.string

    def __repr__(self):
        return str(self)


class GroupedMethods(object):

    #TODO: use threads

    def __init__(self, methods):
        self.methods = list(methods)

    def __call__(self, *args, **kwargs):
        return [method(*args, **kwargs) for method in self.methods]


class MutableDocFrame(object):

    def __init__(self, tokens):
        self.tokens = list(tokens)

    @property
    def words(self):
        return MutableDocFrame(t for t in self.tokens if not t.is_punctuation)

    @property
    def punctuation(self):
        return MutableDocFrame(t for t in self.tokens if t.is_punctuation)

    @property
    def notable(self):
        return MutableDocFrame(t for t in self.tokens if t.is_notable)

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
    def people(self):
        return MutableDocFrame(t for t in self.tokens if t.is_person)

    @property
    def places(self):
        return MutableDocFrame(t for t in self.tokens if t.is_location)

    @property
    def groups(self):
        return MutableDocFrame(t for t in self.tokens if t.is_group)

    @property
    def entities(self):
        return MutableDocFrame(t for t in self.tokens if t.is_entity)


    @property
    def by_notability(self):
        return MutableDocFrame(sorted(self.tokens, key=lambda t: t.notability, reverse=True))


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.tokens[key]
        else:
            return MutableDocFrame(t for t in self.tokens if t.lower == key.lower())

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        self.tokens[key].string = value

    def __getattr__(self, name):
        if hasattr(MutableToken, name):
            attributes = [getattr(token, name) for token in self.tokens]
            if inspect.ismethod(getattr(MutableToken, name)):
                return GroupedMethods(attributes)
            else:
                return attributes


    def __len__(self):
        return len(self.tokens)

    def __str__(self):
        return "[" + ", ".join([str(token) for token in self.tokens]) + "]"

    def __repr__(self):
        return str(self)



class MutableDoc(MutableDocFrame):

    def __init__(self, string):
        string = toolkit.ensure_unicode(string)
        self._doc = nlp.nlp(string)
        for ent in reversed(self._doc.ents):
            ent.merge(ent.root.tag_, ent.root.lemma_, ent.label_)
        self.tokens = [MutableToken(self, token.i) for token in self._doc]

    def mutate_token(self, i, string):
        strings = [token.string for token in self._doc]
        strings[i] = string + self._doc[i].whitespace_
        self.__init__("".join(strings))


    def __str__(self):
        return self._doc.string

    def __repr__(self):
        return str(self)
