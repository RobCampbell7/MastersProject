def weaklyDominates(s1, s2):
    """
    returns True iff s1 weakly dominates s2
    """
    i = 0
    result = True
    while result == True and i < len(s1):
        if s2[i] <= s1[i]:
            result = False
        i += 1

    return result

def dominates(s1, s2):
    """
    returns True iff s1 dominates s2
    """
    return weaklyDominates(s1, s2) and (s1 != s2)

def strictlyDominates(s1, s2):
    """
    returns True iff s1 dominates s2
    """
    i = 0
    result = True
    while result == True and i < len(s1):
        if s2[i] < s1[i]:
            result = False
        i += 1

    return result

def dominant(s1, s2):
    """
    Return types:
    if s1 dominates s2         -> return s1
    if s2 dominates s1         -> return s2
    if mutually non-dominating -> return ()
    """
    if dominates(s1, s2) == True:
        return s1
    elif dominates(s2, s1) == True:
        return s2
    else:
        return ()

def weaklyDominant(s1, s2):
    """
    Return types:
    if s1 weakly-dominates s2  -> return s1
    if s2 weakly-dominates s1  -> return s2
    if mutually non-dominating -> return ()
    """
    if weaklyDominates(s1, s2) == True:
        return s1
    elif weaklyDominates(s2, s1) == True:
        return s2
    else:
        return ()

def strictlyDominant(s1, s2):
    """
    Return types:
    if s1 strictly-dominates s1 -> return s1
    if s2 strictly-dominates s1 -> return s2
    if mutually non-dominating  -> return ()
    """
    if strictlyDominates(s1, s2) == True:
        return s1
    elif strictlyDominates(s2, s1) == True:
        return s2
    else:
        return ()