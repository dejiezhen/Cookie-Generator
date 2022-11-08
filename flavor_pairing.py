"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Presentation Day
10/20/2022

flavor_pairing.py contains methods used to determine the similarity of 
ingredients using dot product, create a dictionary of ingredient pairings foar
an ingredient, and displaying those pairings in a human readable format. 
This fie containts the following functions...
    - similarity: returns the similarity between two ingredients
    - pairing: describes what flavors are similar to the specified ingredient
    - request_pairing: Displays a specific pairing in a human readable way

Credit for this goes to Professor Harmon for providing it for us!
"""

import numpy as np

WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

def similarity(n1, n2):
    """
    Returns the similarity between two ingredients based on our data.
    
    Args:
        n1: the first ingrient
        n2: the second ingredient
    """

    #take the dot product of v1 and v2
    v1 = WORD_EMBED_VALS[n1]
    v2 = WORD_EMBED_VALS[n2]
    return np.dot(v1, v2)

def pairing(ingr, threshold, cat=None):
    """
    Describes what flavors are similar to the specified ingredient based on
    a similarity threshold and an optional category to which the flavors
    belong.

    Args:
        ingr: the ingredient we want to create flavor pairings for
        threshold: the threshold for similarity between ingredients
        cat: category of ingredient
    """

    pairings = {}

    #creates list of the set difference between indredient list and ingr
    ilist = list(set(INGREDIENT_LIST) - set([ingr]))

    #iterates pairings and uses threshold to create pairings key, value pairs
    for i in ilist:
        if similarity(ingr, i) >= threshold:
            if cat is not None:
                if i in INGRED_CATEGORIES:
                    if INGRED_CATEGORIES[i] == cat:
                        pairings[i] = similarity(ingr, i)
            else:
                pairings[i] = similarity(ingr, i)
    
    return pairings

def request_pairing(ingr, threshold, cat=None):
    """
    Displays a specific pairing to the user in a readable way.

    Args:
        ingr: the ingredient we want to create flavor pairings for
        threshold: the threshold for similarity between ingredients
        cat: category of ingredient
    """

    if cat:
        print("\nWhat pairs well with " + ingr + " that is a " + cat + "?")
        pairing(ingr, threshold, cat)
    else:
        print("\nWhat pairs well with " + ingr + "?")
        pairing(ingr, threshold)

def main():
    """
    Requests pairings for green tea and fruit and chocolate.

    Args:
        none
    """

    print("* * * Here are some examples of searching for Western flavor \
    pairings: * * *")
    """request_pairing("orange", 0.1, "herb")
    request_pairing("chocolate", 0.1, "spice")"""
    request_pairing("green tea", 0.6, "fruit")
    request_pairing("chocolate", 0.45)

if __name__ == "__main__":
    main()