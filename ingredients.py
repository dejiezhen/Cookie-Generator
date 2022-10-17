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

class Ingredients:
    def __init__(self):  
        """
        Reads in the original input files of ingredients and creates new files 
        of recipes
        """      
        self.pantry = {}

    def get_category_amount(category):
        #add hard coded values into dictionary with the category name as key and amount as value
        
        pass;

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
