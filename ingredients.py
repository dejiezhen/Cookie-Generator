"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Generation Day
09/29/22

The Ingredients.py file houses the Ingredients class, which takes in the 
original input files of ingedients and creates new files of recipes. It houses 
the update_pantry function that will tweak the ingreidents and/or their 
averages in the pantry.
"""

from flavor_pairing import INGRED_CATEGORIES, INGREDIENT_LIST

class Ingredients:
    def __init__(self):  
        """
        Reads in the original input files of ingredients and creates new files 
        of recipes
        """      
        self.pantry = {}
        self.category_dictionary = {}

    def get_category_amount(self, ingredient):
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

    def find_category_commonality(self, curr_ingredient_arr, category_set, category):
        common_words = curr_ingredient_arr.intersection(category_set)
        if len(common_words) > 0:
            return category
  
    def category_match(self, curr_ingredient):
        categories = None
        category_set = set(INGRED_CATEGORIES.values())
        for category in category_set:
            category_copy = category[:]
            curr_ingredient_arr = set(curr_ingredient.split(' '))
            if self.find_category_commonality(curr_ingredient_arr, set([category[:]]), category):
                categories = category

            curr_category_set = set(category[:].split('/'))
            if len(curr_category_set) > 1 and \
                self.find_category_commonality(curr_ingredient_arr, curr_category_set, category):
                categories = self.find_category_commonality(curr_ingredient_arr, curr_category_set, category) 

            curr_category_set = set(category_copy.split(' '))
            if len(curr_category_set) > 1 and \
                self.find_category_commonality(curr_ingredient_arr, curr_category_set, category):
                categories = self.find_category_commonality(curr_ingredient_arr, curr_category_set, category) 

        return categories


    def word_match(self, curr_ingredient):
        category = None
        for category_ingredient in list(INGRED_CATEGORIES.keys()):
            if category_ingredient[0] != curr_ingredient[0]:
                continue
            min_ingredient = min(len(curr_ingredient), len(category_ingredient))
            max_ingredient = max(len(curr_ingredient), len(category_ingredient))
            counter  = 0
            for i in range(min_ingredient):
                if curr_ingredient[i] == category_ingredient[i]:
                    counter += 1
            if (counter/max_ingredient)>= .75:
                category = \
                    INGRED_CATEGORIES[curr_ingredient] if curr_ingredient in INGRED_CATEGORIES else INGRED_CATEGORIES[category_ingredient]
        return category
    

    def update_category_dict(self, ingredient_category, amount):
        if ingredient_category in self.category_dictionary:
            current_category_amount = self.category_dictionary[ingredient_category]
            new_category_amount = (current_category_amount + amount) / 2
            self.category_dictionary[ingredient_category] = new_category_amount
        else:
            self.category_dictionary[ingredient_category] = amount

    def update_category_amount(self, recipe):
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
        self.update_pantry(recipe)
        self.update_category_amount(recipe)
