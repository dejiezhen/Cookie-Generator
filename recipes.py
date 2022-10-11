"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Generation Day
09/29/22

The Recipes.py file houses the Recipes class that is initialized by the file, 
ingredients dictionary and pantry from the Cookbook class; it deals 
specifically with the maintanence of recipes through these various functions...
    - process_recipe: places ingredients and their amounts in a dictionary
    - pivot: detemrines where in the array the pivot will be
    - normalize_recipe: ensures the recipe amounts sum to one-hundred
    - mutate: mutates the recipe in one of four ways
    - change_amt: chnages the amount of an ingredient
    - change_ing: changed the ingreident
    - add_ing: adds ingredient to recipe
    - del_ingredient: deletes ingredient from reicpe
    - save_recipe_cookbook: turns recipe into .txt file
"""

import random

class Recipes:
    def __init__(self, file, ingredients_dictionary, pantry, mutations_in_lineage) -> None:
        """
        Recipe class where recipe is primarily used and stored as a dictionary
        where the keys are the ingredients and the values are the corresponding 
        amounts

        Args: 
            file (.txt): recipe file
            ingredients_dictionary (dict): dictionary representation of 
                                            ingredients
            pantry (dict): cumulative pantry of ingredients 
        """
        self.file = file
        self.ingredients_dictionary = ingredients_dictionary
        self.pantry = pantry
        self.mutations_in_lineage = mutations_in_lineage


    def process_recipe(self):
        """
        This function read the lines from a file and iterates through to 
        establish the ingredient and amount of ingredient; then that ingredient 
        and its amount is placed in a dictionary. 

        Args:
            None
        """
        files = open('./input/' + self.file, 'r')
        ingredient_lines = files.readlines()
        for ingredient in ingredient_lines:
            ingredient_amount_array = ingredient.split("oz")
            amount, name = ingredient_amount_array
            name = name.strip()
            amount = amount.strip() 
            # if same ingredient name, average
            if name in self.ingredients_dictionary:
                current_ingredient_amount = self.ingredients_dictionary[name]
                new_average = (current_ingredient_amount + float(amount)) / 2
                self.ingredients_dictionary[name] = new_average
            else:
                self.ingredients_dictionary[name] = float(amount)

    def pivot(self):
        """
        Returns an int to be used as the pivot point in the recipes.
        Args:
            None
        """
        # do not let pivot be at very beginning or end 
        return random.randint(1, len(self.ingredients_dictionary)-2)    

    def normalize_recipe(self):
        """
        Makes sure all amounts in recipe sum to 55, the average oz total of 
        all input recipes

        Args:
            None
        """
        sum_val = sum(self.ingredients_dictionary.values())
        rescalar = 55 / sum_val
        for ingredient, amount in self.ingredients_dictionary.items():
            self.ingredients_dictionary[ingredient] = amount * rescalar

    def mutate(self):
        """
        Uses random choice to determine which out of four mutation possibilities
        to implement on the listed ingredients

        Args:
            None
        """
        mutation_options = ["change_amt", "change_ing", "add_ing", \
             "del_ingredient"]
        mutation_type = random.choice(mutation_options)
        list_ingredients = list(self.ingredients_dictionary.keys())
        if mutation_type == "change_amt":
            self.change_amt(list_ingredients)
        elif mutation_type == "change_ing":
            self.change_ing(list_ingredients)
        elif mutation_type == "add_ing":
            self.add_ing()
        else:                                                                     
            self.del_ingredient(list_ingredients)
        
    def change_amt(self, list_ingredients):
        """
        Changes the amount of an indregient by a random modifier.
       
        Args:
            list_ingredients (arr): list of ingredients
        """
        ingredient_to_change = random.choice(list_ingredients)       
        original_amount = self.ingredients_dictionary[ingredient_to_change]
        # decrease or increase by up to 50%
        amount_modifier = random.uniform(0.5, 1.5)    
        self.ingredients_dictionary[ingredient_to_change] = original_amount * \
            amount_modifier

    def change_ing(self, list_ingredients):
        """
        Randomly removes an ingredient from the recipe then randomly add an 
        ingredient (not currently in the recipe) from the pantry list

        Args:
            list_ingredients (arr): list of ingredients
        """
        pantry_ing_list = list(self.pantry.pantry.keys())
        ingredient_to_remove = random.choice(list_ingredients)
        ingredient_to_add = random.choice(pantry_ing_list)    

        while len(pantry_ing_list) != len(list_ingredients) and \
            ingredient_to_add in self.ingredients_dictionary: 
            ingredient_to_add = random.choice(pantry_ing_list)

        del self.ingredients_dictionary[ingredient_to_remove]
        self.ingredients_dictionary[ingredient_to_add] = \
            self.pantry.pantry[ingredient_to_add]     # use pantry amount 

    def add_ing(self):
        """
        Add a new ingredient to the recipe from the pantry (not already in the 
        recipe)
        
        Args:
            None
        """
        pantry_ing_list = list(self.pantry.pantry.keys())
        # grab new ingredient from pantry
        ingredient_to_add = random.choice(pantry_ing_list)     

        while len(pantry_ing_list) != len(self.ingredients_dictionary) and \
            ingredient_to_add in self.ingredients_dictionary:  
            ingredient_to_add = random.choice(pantry_ing_list)    
        self.ingredients_dictionary[ingredient_to_add] = \
            self.pantry.pantry[ingredient_to_add]      # use pantry amount 

    def del_ingredient(self, list_ingredients):
        """
        Deletes a random ingredient from the recipe
        
        Args:
            None
        """
        ingredient_to_remove = random.choice(list_ingredients)
        del self.ingredients_dictionary[ingredient_to_remove]

    def name_recipe(self):
        """
        Give a name based on the second and third most populous ingredient 
        in the recipe. 
        """ 
        ingredient_remove_array = ['baking soda', 'flour', 'baking powder']
        # Sorted recipe by value, largest to smallest
        sorted_recipe = sorted(self.ingredients_dictionary.items(), \
            key=lambda x: x[1], reverse=True)

        first_random_idx = random.randint(1, len(self.ingredients_dictionary)-1)
        first_random_name = sorted_recipe[first_random_idx][0]
        while first_random_name in ingredient_remove_array:
            first_random_idx = random.randint(1, len(self.ingredients_dictionary)-1)
            first_random_name = sorted_recipe[first_random_idx][0]

        second_random_idx = random.randint(1, len(self.ingredients_dictionary)-1)
        second_random_name = sorted_recipe[second_random_idx][0]
        while second_random_name in ingredient_remove_array:
            second_random_idx = \
                random.randint(1, len(self.ingredients_dictionary)-1)
            second_random_name = sorted_recipe[second_random_idx][0]

        while first_random_idx == second_random_idx:
            second_random_idx = random.randint(1, len(self.ingredients_dictionary)-1)
            
        
        recipe_name = sorted_recipe[first_random_idx][0] + " and " + \
             sorted_recipe[second_random_idx][0]

        recipe_underscore = recipe_name.replace(' ', '_')

        return recipe_underscore

    def evaluate_novel_ingredient(self, inspiring_set):
        score = 0
        for inspiring_recipe in inspiring_set: 
            inspiring_ingredients_list = set(inspiring_recipe.ingredients_dictionary.keys())
            ingredients_list = set(self.ingredients_dictionary.keys())
            different_ingredients = inspiring_ingredients_list.symmetric_difference(ingredients_list)
            score += len(different_ingredients)
        return score

    def save_recipe_cookbook(self, generation, idx, curr_time):
        """
        Saves recipe as .txt file
        
        Args:
            generation (int): integer than represents the generation
            idx (int): number corresponding to the given recipe in the \
                generation 
            curr_time (str): current time
        """
        recipe_name = self.name_recipe()
        file_name = 'gen'+ str(generation) + "_" + recipe_name + '.txt'
        # print(recipe_name)
        with open("output/" + curr_time + "/" + file_name, 'w') as f:
            for ingredient, amount in self.ingredients_dictionary.items(): 
                amount = round(amount, 2)
                f.write(str(amount) + " oz " + str(ingredient) + "\n")
