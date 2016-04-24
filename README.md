**"Uselessness will increase, and be seen as a positive antidote to an era of utility"** - Prof Andrew Hugill 2025 prediction

A pataphysical toolkit for exploring (n)oulipian literature.

####Usage
    
    python -i tokens.py
    
    >>> import apis, random
    >>> text = MutableDoc(apis.prose.get_paragraph())
    >>> print(text)
    The stars were still shining brightly in a cloudless sky when the sound of the horns warned the people to set out on their march. Meanwhile the vanguard had been sent forward to inform Moses of the condition of the tribes, and after the review was over, Ephraim followed them.
    >>> for n in text.nouns:
          n.string = random.choice(n.clinaments())
    >>> print(text)
    The frats were still shining brightly in a cloudless muskeg when the found of the morns warned the popper to set out on their marls. Meanwhile the Winograd had been sent forward to inform Moses of the condition of the wries, and after the review was over, Ephraim followed thug.
    
