"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Generation Day
09/29/22

The Cookbook.py file houses the Cookbook class, which is called by the main 
function and initialized by the file list, the targeted generation number, and 
the mutation rate. It houses the following functions... 
    - evaluate: evaluate the fitness of the recipes 
    - rank: returns the length of keys 
    - adds recipe instance: creates a new recipe from a new file input 
    - make_initial_cookbook: collates recipes to create a cookbook
    - get_pivot_array: gathers the pivoted array from parents
    - convert_to_dict: converts arrays to dictionary
    - create_recipe_files: creates new recipes files 
    - merge: merge parents to create children
    - breed_generations: breeds the parent recipes
"""

from recipes import Recipes
from ingredients import Ingredients
import os, time, random, copy

class Cookbook:
    def __init__(self, file_list, target_generation, mutation_rate) -> None:
        """
        Cookbook class where a cookbook stores multiple recipes and where 
        multiple generations of cookbooks are created

        Args: 
            file_list (arr): list of file names to read in for recipes
            target_generation (int): the total number of generations desired
            mutation_rate (float): the probability that mutation will occur 
                                    each time 
        """
        self.file_list = file_list
        self.pantry = Ingredients()
        self.curr_generation = 0
        self.target_generation = int(target_generation)
        self.cookbook = []
        self.inspiring_set = []
        self.curr_time = ""
        self.mutation_rate = mutation_rate
     
    def evaluate(self, curr_dictionary):
        """
        Return the length of the keys, which corresponds to the fitness 
        (diversity of ingredients)
       
        Args: 
            curr_dictionary (dict): current dictionary of the sort list 
        """
        return len(curr_dictionary.ingredients_dictionary.keys())
    
    def rank_new_ingredient(self, array):
        score = 0
        for recipe in array:
            ingredients_list = set(recipe.ingredients_dictionary.keys())
            for inspiring_recipe in self.inspiring_set: 
                inspiring_ingredients_list = set(inspiring_recipe.ingredients_dictionary.keys())
                different_ingredients = inspiring_ingredients_list.symmetric_difference(ingredients_list)
                score += len(different_ingredients)
        return score

    def rank(self, array): 
        """
        Ranks the recipes on the basis of the evaluate function
        
        Args:
            None
        """       
        # compare new ingredients for each baby to inspiring set, divide by 6 then divide 
        array.sort(reverse=True, key=self.evaluate)
        return array

    def add_recipe_instance(self):
        """
        Creates a recipe instance from an inputted file.
       
        Args:
            None
        """
        for file in self.file_list:
            new_recipe = Recipes(file, {}, self.pantry, 0)
            self.cookbook.append(new_recipe)

    def make_initial_cookbook(self):
        """
        Processes and normalizes recipes while updating the pantry to make 
        a cookbook.
       
        Args:
            None
        """
        self.add_recipe_instance()

        for recipe in self.cookbook:
            recipe.process_recipe()
            recipe.normalize_recipe()
            self.pantry.update_pantry(recipe.ingredients_dictionary)
        self.inspiring_set = copy.deepcopy(self.cookbook)
        self.cookbook = self.rank(self.cookbook)

    def get_pivot_array(self):
        """
        Gets an array of the ingredients on one side of the pivot.
       
        Args:
            self: accesses the current class instance
        """
        pivot_array = [recipe.pivot() for recipe in self.cookbook]
        return pivot_array
    
    def convert_to_dict(self, baby_recipe):
        """
        Fills an empty dictionary by taking the baby_recipe array and arranging 
        its contents into key, value pairs.
     
        Args:
            self: accesses the current class instance
            baby_recipe: the recipe created from mergin parents
        """
        ingredient_dict = {}
        for ingredient in baby_recipe:
            name = ingredient[0]
            value = ingredient[1]
            if name in ingredient_dict:
                curr_ingredient_value = ingredient_dict[name]
                new_value = (value + curr_ingredient_value) / 2
                ingredient_dict[name] = new_value
            else:
                ingredient_dict[name] = value
        return ingredient_dict

    def create_recipe_files(self, new_cookbook):
        """
        Iterates through cookbook to create recipe files.
       
        Args:
            self: accesses the current class instance
            new_cookbook: the cookbook the recipe files will be made from
        """
        curr_baby_idx = 0
        for recipe in new_cookbook:
            recipe.save_recipe_cookbook(self.curr_generation,curr_baby_idx, \
                self.curr_time)
            curr_baby_idx += 1

    def merge_parents(self, parent1_first_half, parent1_second_half, \
        parent2_first_half, parent2_second_half):
        """
        Merges two parents to make new babies
       
        Args:
            parent1_first_half (arr): first half of the array of parent 1
            parent1_second_half (arr): second half of the array of parent 1
            parent2_first_half (arr): first half of the array of parent 2
            parent2_second_half (arr): second half of the array of parent 2
        """
        first_baby_arr = parent1_first_half + parent2_second_half
        second_baby_arr = parent1_second_half + parent2_first_half
        first_baby_dict = self.convert_to_dict(first_baby_arr)
        second_baby_dict = self.convert_to_dict(second_baby_arr)
        return [first_baby_dict, second_baby_dict]

    def merge(self):
        """
        Merges parent recipes by their pivot arrays to create two new recipes, 
        which can them be mutated before being placed in a ranked cookbook.
      
        Args:
            None
        """
        baby_list = []
        pivot_array = self.get_pivot_array()
        for i in range(0, len(self.cookbook), 2):
            first_pivot = pivot_array[i] 
            second_pivot = pivot_array[i+1] 

            parent1 = list(self.cookbook[i].ingredients_dictionary.items())
            parent2 = list(self.cookbook[i+1].ingredients_dictionary.items())
            
            parent1_first_half, parent1_second_half = \
                parent1[:first_pivot], parent1[first_pivot:]
            parent2_first_half, parent2_second_half  = \
                parent2[:second_pivot], parent2[second_pivot:]
            

            new_babies = self.merge_parents(parent1_first_half, \
                parent1_second_half, parent2_first_half, parent2_second_half)
            first_baby_dict, second_baby_dict = new_babies

            # add together parents' mutations in lineage to then 
            #   sum those for the new babies 
            parent_mutations_in_lineage = self.cookbook[i].mutations_in_lineage + \
                self.cookbook[i+1].mutations_in_lineage
            self.cookbook[i], self.cookbook[i+1]
            # Create new baby instances
            first_baby = Recipes(None, first_baby_dict, self.pantry, \
                parent_mutations_in_lineage)
            second_baby = Recipes(None, second_baby_dict, self.pantry, \
                parent_mutations_in_lineage)

            mutation_chance = random.random()    # generate random float 0 to 1 
            if mutation_chance <= self.mutation_rate:
                first_baby.mutate()
                second_baby.mutate()
                first_baby.mutations_in_lineage += 1
                second_baby.mutations_in_lineage += 1
            
            first_baby.normalize_recipe()
            second_baby.normalize_recipe()

            self.pantry.update_pantry(first_baby.ingredients_dictionary)
            self.pantry.update_pantry(second_baby.ingredients_dictionary)

            baby_list.append(first_baby)
            baby_list.append(second_baby)
        new_baby_list = self.rank_new_ingredient(baby_list)
        new_baby_list = self.rank(baby_list)
        # extract the 50% best of the older cookbook and the 50% 
        #   best of the baby list to make new cookbook 
        new_cookbook = self.cookbook[:len(self.cookbook)//2] + \
            new_baby_list[:len(new_baby_list)//2] 
        new_cookbook = self.rank(new_cookbook)
        self.create_recipe_files(new_cookbook)
        self.cookbook = new_cookbook
    
    def breed_generations(self):
        """
        Breeds new generations by looping the merge function to create new 
        recipes/files until the targeted generation is reached. 
     
        Args:
            None
        """
        self.make_initial_cookbook()

        curr_time =  time.strftime("%H:%M:%S", time.localtime())
        self.curr_time = curr_time
        parent_dir = "./output/"
        path = os.path.join(parent_dir, self.curr_time)
        os.mkdir(path)

        while self.curr_generation <= self.target_generation:
            self.merge()
            self.curr_generation += 1

            