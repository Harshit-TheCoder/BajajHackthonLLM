vague_words = [
    # General ambiguity
    "thing", "things", "stuff", "something", "anything", "everything", "it", "that", "this", "those", "these",

    # Non-specific quantities or references
    "some", "several", "many", "few", "a lot", "lots", "bunch", "kind of", "sort of", "part of it", "a little", 
    "more or less", "a few", "somehow", "somewhat", "a bit", "a couple", "a number of", "quite a few",

    # Ambiguous phrases
    "you know", "and so on", "and whatnot", "and all that", "all sorts of things", "all that stuff", 
    "that kind of thing", "whatchamacallit", "doohickey", "thingamajig", "thingamabob", "gizmo", "etc",

    # Uncertain modal expressions
    "maybe", "possibly", "probably", "I guess", "I think", "I feel", "I believe", "it seems", "could be", 
    "might be", "should be", "must be", "sort of", "kind of", "likely", "apparently", "presumably",

    # Unclear references or generalization
    "everyone", "everything", "everywhere", "all of them", "people", "someone", "they", "them", "that one",
    "a place", "some place", "somewhere", "anywhere", "over there", "over here", "around here", "in the area",

    # Filler & conversational padding
    "uh", "um", "er", "like", "just", "actually", "basically", "literally", "really", "honestly", "seriously",

    # Vague temporal references
    "someday", "sometimes", "recently", "lately", "a while ago", "soon", "nowadays", "in the past", 
    "in the future", "before", "after", "later", "once", "occasionally",

    # Unclear requests or commands
    "do something", "help me with it", "deal with it", "fix that", "show me stuff", "give info", 
    "tell me more", "explain it", "make it better", "give details", "talk about that",

    # Vague comparative/superlative
    "better", "worse", "faster", "slower", "more", "less", "big", "small", "huge", "tiny", "good", "bad", 
    "best", "worst", "nice", "great", "cool", "interesting", "important", "useful"
]



vague_phrases = [
    r"\ba lot\b", r"\blots\b", r"\bbunch\b", r"\bkind of\b", r"\bsort of\b", r"\bpart of it\b",
    r"\bmore or less\b", r"\ba few\b", r"\bsomehow\b", r"\bsomewhat\b", r"\ba bit\b", r"\ba couple\b",
    r"\ba number of\b", r"\bquite a few\b",
    r"\byou know\b", r"\band so on\b", r"\band whatnot\b", r"\band all that\b", r"\ball sorts of things\b",
    r"\ball that stuff\b", r"\bthat kind of thing\b", r"\bwhatchamacallit\b", r"\bdoohickey\b",
    r"\bthingamajig\b", r"\bthingamabob\b", r"\bgizmo\b",
    r"\bi guess\b", r"\bi think\b", r"\bi feel\b", r"\bi believe\b", r"\bit seems\b", r"\bcould be\b",
    r"\bmight be\b", r"\bshould be\b", r"\bmust be\b",
    r"\ball of them\b", r"\bthat one\b", r"\ba place\b", r"\bsome place\b", r"\bover there\b", r"\bover here\b",
    r"\baround here\b", r"\bin the area\b",
    r"\bsomeday\b", r"\bsometimes\b", r"\brecently\b", r"\blately\b", r"\ba while ago\b", r"\bin the past\b",
    r"\bin the future\b",
    r"\bdo something\b", r"\bhelp me with it\b", r"\bdeal with it\b", r"\bfix that\b", r"\bshow me stuff\b",
    r"\bgive info\b", r"\btell me more\b", r"\bexplain it\b", r"\bmake it better\b", r"\bgive details\b",
    r"\btalk about that\b"
]