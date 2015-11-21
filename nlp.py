import numpy as np
import spacy.en

nlp = spacy.en.English()

unique_words = {w.lower_ for w in nlp.vocab if w.has_vector}
unique_words = np.asarray([nlp.vocab[w] for w in unique_words])
