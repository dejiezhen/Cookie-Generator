"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Generation Day
09/29/22

The Ingredients.py file houses the Ingredients class, which takes in the 
original input files of ingedients and creates new files of recipes. It houses 
the following functions...
    - get_category_amount: gets the amount of an ingredient based on category
    - update_pantry: tweak the ingreidents and/or their averages in the pantry
    - find_category_commonality: finds the common ingredients between the 
        ingredient array and category set
    - category_match: matches an ingredient with a category
    - word_match: determines which category to retunr for similarly spelled 
        ingredients
    - update_category_dict: updates the category dictionary by changing 
    the amount in the category or by creating a new dictionary item 
    - update_category_amount: Updates the amount of an ingredient through its 
        category
    - update_pantry_categories: Updates the pantry categories and the category 
        amounts
"""

from flavor_pairing import INGRED_CATEGORIES

class Ingredients:
    def __init__(self):  
        """
        Reads in the original input files of ingredients and creates new files 
        of recipes

        Args:
            none
        """      

        self.pantry = {}
        self.category_dictionary = {}

    def get_category_amount(self, ingredient):
        """
        Uses a hard coded dictionary of categories and amounts we refer to 
        when determing the amount of the inputted ingredient.

        Args:
            ingredient - the current ingredient we are getting an amount for
        """

        category_inspiring_set = {
                                "dairy": 8, 
                                "plant derivative": 8, 
                                "animal product": 8, 
                                "nut/seed/pulse": 10, 
                                "spice": 2, 
                                "herb": 2, 
                                "fruit": 4, 
                                "cereal": 1, 
                                "plant": 1, 
                                "flower": 0.5, 
                                "vegetable": 0.5,
                                "cereal/crop": 0.5, 
                                "fish/seafood": 0.5, 
                                "meat": 0.5
                                }
        ingredient_category = INGRED_CATEGORIES.get(ingredient)
        if not ingredient_category:
            return self.category_dictionary['Other']
        else:
            if ingredient_category not in self.category_dictionary:
                default_val = category_inspiring_set[ingredient_category]
                self.category_dictionary[ingredient_category] = default_val
            return self.category_dictionary[ingredient_category]

    def update_pantry(self, recipe):
        """
        Add new ingredients / update ingredient averages to the pantry based 
        on a given recipe
        
        Args:
            recipe (dict): a dictionary form of the recipe, where ingredients 
            are keys and amounts are values
        """

        for name, amount in recipe.items():
            if name in self.pantry:
                pantry_regularized_total = self.pantry[name]
                new_regularized_total = (pantry_regularized_total + amount) / 2
                self.pantry[name] = new_regularized_total
            else:
                self.pantry[name] = amount

    def find_category_commonality(self, curr_ingredient_arr, \
        category_set, category):
        """
        Finds the common ingredients between the ingredient array and category 
        set and returns them.
        
        Args:
            curr_ingredient_arr: current ingredient array
            category_set: set of categories
            category: the current category
        """

        common_words = curr_ingredient_arr.intersection(category_set)
        if len(common_words) > 0:
            return category
  
    def category_match(self, curr_ingredient):
        """
        Matches an ingredient with a category. Determines if current 
        ingredients share commonality with the category, then it returns an 
        updated category.

        Args:
            curr_ingredient: current ingredient
        """

        categories = None
        category_set = set(INGRED_CATEGORIES.values())

        for category in category_set:
            category_copy = category[:]
            curr_ingredient_arr = set(curr_ingredient.split(' '))
            if self.find_category_commonality(curr_ingredient_arr, \
                set([category[:]]), category):
                categories = category

            curr_category_set = set(category[:].split('/'))
            if len(curr_category_set) > 1 and \
                self.find_category_commonality(curr_ingredient_arr, \
                    curr_category_set, category):
                categories = self.find_category_commonality\
                    (curr_ingredient_arr, curr_category_set, category) 

            curr_category_set = set(category_copy.split(' '))
            if len(curr_category_set) > 1 and \
                self.find_category_commonality(curr_ingredient_arr, \
                    curr_category_set, category):
                categories = self.find_category_commonality\
                    (curr_ingredient_arr, curr_category_set, category) 

        return categories

    def word_match(self, curr_ingredient):
        """
        If the word form ingredient category or ingredient lists are 
        essentially matching, return the category that is in categories.

        Args:
            curr_ingredient: current ingredient
        """

        category = None

        for category_ingredient in list(INGRED_CATEGORIES.keys()):

            if category_ingredient[0] != curr_ingredient[0]:
                continue

            min_len_ingredient = min(len(curr_ingredient), \
                len(category_ingredient))
            max_len_ingredient = max(len(curr_ingredient), \
                len(category_ingredient))
            counter  = 0

            for i in range(min_len_ingredient):
                if curr_ingredient[i] == category_ingredient[i]:
                    counter += 1
            
            if (counter/max_len_ingredient)>= .75:
                category = \
                    INGRED_CATEGORIES[curr_ingredient] if curr_ingredient in \
                        INGRED_CATEGORIES else \
                            INGRED_CATEGORIES[category_ingredient]
        return category

    def update_category_dict(self, ingredient_category, amount):
        """
        Updates the category dictionary by either 1. changing the amount in the 
        category by halfing the sum of the category amount by the inputted 
        amount or 2. creating a new dictionary item using the inputted amount.

        Args:
            ingredient_category: category of ingredient
            amount: amount of ingredient
        """

        if ingredient_category in self.category_dictionary:
            current_category_amount = self.category_dictionary\
                [ingredient_category]
            new_category_amount = (current_category_amount + amount) / 2
            self.category_dictionary[ingredient_category] = new_category_amount
        else:
            self.category_dictionary[ingredient_category] = amount

    def update_category_amount(self, recipe):
        """
        Updates the amount of an ingredient through its category.  Determines 
        if ingredient is already a category first.  If it is, we update that 
        category's amount.  If it is not, then me match it to a category and 
        set its amount equal to a category amount.

        Args:
            recipe: current recipe we are updating the category amount
        """
        
        for ingredient, amount in recipe.items():
            ingredient_category = INGRED_CATEGORIES.get(ingredient, None)
            if not ingredient_category:
                initial_category_match = self.category_match(ingredient)
                word_match_category = self.word_match(ingredient)
                if initial_category_match:
                    self.update_category_dict(initial_category_match, amount)
                elif word_match_category:
                    self.update_category_dict(word_match_category, amount)
                else:
                    self.update_category_dict('Other', .5)
            else :
                self.update_category_dict(ingredient_category, amount)

    def update_pantry_categories(self, recipe):
        """
        Updates the pantry categories and the category amounts.

        Args:
            recipe: current recipe we want to update the pantry
        """

        self.update_pantry(recipe)
        self.update_category_amount(recipe)
