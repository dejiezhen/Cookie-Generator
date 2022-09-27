"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ1: Let's Get Cooking
09/22/22

The Ingredients.py file houses the Ingredients class, which takes in the orininal 
input files of ingedients and creates new files of recipes. It houses the update_pantry 
function that will tweak the ingreidents and/or their averages in the pantry.
"""

class Ingredients:
    def __init__(self):  
        """
        Reads in the original input files of ingredients and creates new files of recipes
        """      
        self.pantry = {}

    def update_pantry(self, recipe):
        """
        Add new ingredients / update ingredient averages to the pantry based on a given recipe
        
        Args:
            recipe (dict): a dictionary form of the recipe, where ingredients are keys and amounts are values

        """
        for name, amount in recipe.items():
            if name in self.pantry:
                curr_pantry_average = self.pantry[name]
                average = (curr_pantry_average + amount) / 2
                self.pantry[name] = average
            else:
                self.pantry[name] = amount
