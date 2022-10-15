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
    - change_ingredient: changed the ingreident
    - add_ingredient: adds ingredient to recipe
    - del_ingredient: deletes ingredient from reicpe
    - save_recipe_cookbook: turns recipe into .txt file
"""

import random
from collections import Counter
from flavor_pairing import *

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
        self.allergies = set(['macadamia nut', 'walnut', 'pecan', 'cashew nut', \
            'pistachio', 'almond', 'brazil nut'])


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
        if len(self.ingredients_dictionary) >= 3:
            return random.randint(1, len(self.ingredients_dictionary)-2) 
        else: 
            # Check edge case if arr length is less than 3
            return random.randint(0, len(self.ingredients_dictionary)-1)   

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
        mutation_options = ["add_flavor_ingredient"]
        """mutation_options = ["change_amt", "change_ingredient", "add_ingredient", \
             "add_flavor_ingredient", "del_ingredient"]"""
        mutation_type = random.choice(mutation_options)
        list_ingredients = list(self.ingredients_dictionary.keys())
        if mutation_type == "change_amt":
            self.change_amt(list_ingredients)
        elif mutation_type == "change_ingredient":
            self.change_ingredient(list_ingredients)
        elif mutation_type == "add_ingredient":
            self.add_ingredient()
        elif mutation_type == "add_flavor_ingredient":
            self.add_flavor_ingredient()
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
        # amount_modifier = random.uniform(0.5, 1.5)  
        # amount_modifier = random.uniform(0.75, 1.25)        
        amount_modifier = random.uniform(0.9, 1.1)    
        self.ingredients_dictionary[ingredient_to_change] = original_amount * \
            amount_modifier

    def change_ingredient(self, list_ingredients):
        """
        Randomly removes an ingredient from the recipe then randomly adds an 
        ingredient (not currently in the recipe) from the pantry list

        Args:
            list_ingredients (arr): list of ingredients
        """
        pantry_ingredient_set = \
            set(self.pantry.pantry.keys()).difference(self.allergies)
        ingredient_to_remove = random.choice(list_ingredients)
        ingredient_to_add = random.choice(pantry_ingredient_set)    

        while len(pantry_ingredient_set) != len(list_ingredients) and \
            ingredient_to_add in self.ingredients_dictionary: 
            ingredient_to_add = random.choice(pantry_ingredient_set)

        del self.ingredients_dictionary[ingredient_to_remove]
        self.ingredients_dictionary[ingredient_to_add] = \
            self.pantry.pantry[ingredient_to_add]     # use pantry amount 

        # pass        # addition_options = ["add_ing"re"dient, add_flavored_ing"redient]

    def add_ingredient(self):
        """
        Add a new ingredient to the recipe from the pantry (not already in the 
        recipe)
        # pick random ingredient and find something to pair with and have add
        
        Args:
            None
        """
        # keys = ingredients
        pantry_ingredient_set = \
            set(self.pantry.pantry.keys()).difference(self.allergies) 
        # grab new ingredient from pantry
        ingredient_to_add = random.choice(pantry_ingredient_set)     

        while len(pantry_ingredient_set) != len(self.ingredients_dictionary) \
            and ingredient_to_add in self.ingredients_dictionary:  
            ingredient_to_add = random.choice(pantry_ingredient_set)  
                        
        self.ingredients_dictionary[ingredient_to_add] = \
            self.pantry.pantry[ingredient_to_add]      
            # use pantry amount 

    def add_flavor_ingredient(self):

        base_ingredient = \
            random.choice(list(self.ingredients_dictionary.keys()))
        recipe_ingredient_set = \
            set(self.ingredients_dictionary.keys()).difference(self.allergies)
        ingredient_list_set = set(INGREDIENT_LIST).difference(self.allergies)
        set_common = recipe_ingredient_set.intersection(ingredient_list_set)
        base_amount = 0
        print(INGREDIENT_LIST)

        if len(set_common) == 0:
            # if they don't have anything in common 
            choices = ingredient_list_set# .difference(self.allergies)
            base_ingredient = random.choice(list(choices))
            base_amount = 0.55
        else:
            # if they do have in commom
            choices = recipe_ingredient_set.intersection(ingredient_list_set)
            base_ingredient = random.choice(list(choices))
            base_amount = self.ingredients_dictionary[base_ingredient]

        pairings_dictionary = {}
        threshold = 0.001       # could have dicts still that are zero size 

        pairings_dictionary = pairing(base_ingredient, threshold)
        #new_ingredient = max(pairings_dictionary, key=pairings_dictionary.get)
        
        #random choice of top three most cohesive
        find_top_three = Counter(pairings_dictionary)
        top_three = find_top_three.most_common(3)
        random_top_three = dict(top_three)  
        new_ingredient = random.choice(list(random_top_three.keys()))

        #add new, fun ingredient to recipe
        self.ingredients_dictionary[new_ingredient] = base_amount
   
    def del_ingredient(self, list_ingredients):
        """
        Deletes a random ingredient from the recipe, but leaves fundamental 
        baking ingredients alone
        
        Args:
            None
        """
        essential_ingredients = ['flour', 'sugar', 'egg', 'butter', 
        'baking soda', 'baking powder']
        deletable_list = [ingredient for ingredient in list_ingredients \
                            if ingredient not in essential_ingredients]
        ingredient_to_remove = random.choice(deletable_list)
        del self.ingredients_dictionary[ingredient_to_remove]
    
    def get_name(self, sorted_recipe):
        random_idx = random.randint(0, len(sorted_recipe)-1)
        random_name = sorted_recipe[random_idx][0]
        return random_name
    
    def name_recipe(self):
        """
        Give a name based on the second and third most populous ingredient 
        in the recipe. 
        """ 
        ingredient_remove_array = ['baking soda', 'flour', 'baking powder']
        # Sorted recipe by value, largest to smallest
        sorted_recipe = sorted(self.ingredients_dictionary.items(), \
            key=lambda x: x[1], reverse=True)

        # first_random_idx = random.randint(0, len(sorted_recipe)-1)
        # first_random_name = sorted_recipe[first_random_idx][0]
        first_random_name = self.get_name(sorted_recipe)
        while first_random_name in ingredient_remove_array and \
            len(sorted_recipe) > len(ingredient_remove_array):
            first_random_name = self.get_name(sorted_recipe)

        second_random_name = self.get_name(sorted_recipe)
        # plus one since we don't want the same first random name
        while second_random_name in ingredient_remove_array and \
            len(sorted_recipe) > len(ingredient_remove_array) + 1:
            second_random_name = self.get_name(sorted_recipe)

        while first_random_name == second_random_name and len(sorted_recipe) > 1:
            second_random_name = self.get_name(sorted_recipe)
            
        recipe_name = (first_random_name + " and " + \
             second_random_name).replace(' ', '_')
             
        return recipe_name

    def evaluate_novel_ingredient(self, inspiring_set):
        """
        neeed docstring 
        """
        score = 0
        for inspiring_recipe in inspiring_set: 
            inspiring_ingredients_list = set(inspiring_recipe.ingredients_dictionary.keys())
            ingredients_list = set(self.ingredients_dictionary.keys())
            different_ingredients = ingredients_list.difference(inspiring_ingredients_list)
            score += len(different_ingredients)
        
        regularized_score = score / len(self.ingredients_dictionary)
        return regularized_score

    def evaluate_ingredient_cohesion(self):
        """
        need docstring 
        """

        forbidden_ingredients = ["baking soda", "cream of tartar", 
        "sugar", "flower", "shortening", "white chocolate", 
        "light brown sugar", "dark brown sugar"]

        ingredients_to_see = list(self.ingredients_dictionary.keys())
        score = 0
        threshold = 0.01      # check this !!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        for first_index in range(0, len(ingredients_to_see) - 1):
            for second_index in range(first_index + 1, len(ingredients_to_see)):
                first_ingredient = ingredients_to_see[first_index]
                second_ingredient = ingredients_to_see[second_index]                
                # print(first_ingredient)
                # print(second_ingredient)

                if first_ingredient in INGREDIENT_LIST and \
                    second_ingredient in INGREDIENT_LIST:

                    cohesion = similarity(first_ingredient, second_ingredient)
                    if cohesion >= threshold: 
                        score += 1 

                else: 
                    pass

        score = score/len(self.ingredients_dictionary)  # regularize 
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

