"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Generation Day
10/17/22

The Cookbook.py file houses the Cookbook class, which is called by the main 
function and initialized by the file list, the targeted generation number, and 
the mutation rate.  It houses the following functions... 
    - evaluate: evaluate the fitness of the recipes
    - evaluate_unique_ingredients: Calls evaluate_novel_ingredient on the 
        current recipe
    - evaluate_ingredient_cohesion: Calls evaluate_ingredient_cohesion on the 
        current recipe
    - evaluate_essential_ingredient: Calls evaluate_essential_ingredient on the
        current recipe
    - evaluate_ingredients_length: Calls evaluate_ingredients_length on the 
        current recipe
    - combo_evaluate: Returns the combined average of all evaluations 
    - rank_initial_cohesion: Sort recipe array by their ingredients cohesion
    - rank: Ranks the recipes on the basis of the evaluate function
    - adds_recipe_instance: Creates a recipe instance from an inputted file 
    - make_initial_cookbook: Collates recipes to create a cookbook
    - get_pivot_array: Gathers an array of ingredients on one side of the pivot
    - convert_to_dict: Converts arrays to dictionaries
    - create_recipe_files: creates new recipes files 
    - get_pivot: Returns first and second pivot from pivot array
    - get_parents: Returns lists of the parents' ingredient dictionary items
    - partition_parent1: Partitions parent into first and second pivot halves
    - partition_parent2: Partitions parent into first and second pivot halves
    - merge_parents: Merges two parents to make new babies.
    - merge: Merge parents to create two children
    - breed_generations: Loops merge to create new generations
"""


from recipes import Recipes
from ingredients import Ingredients
import os, time, random, copy

class Cookbook:
    def __init__(self, file_list, target_generation, mutation_rate) -> None:
        """
        Cookbook class where a cookbook stores multiple recipes and where 
        multiple generations of cookbooks are created.

        Args: 
            file_list: array of file names to read in for recipes.
            target_generation: the total number of generations desired.
            mutation_rate: the probability that mutation will occur
            each time.
        """

        self.file_list = file_list
        self.pantry = Ingredients()
        self.curr_generation = 1
        self.target_generation = int(target_generation)
        self.cookbook = []
        self.inspiring_set = []
        self.curr_time = ""
        self.mutation_rate = mutation_rate
        self.average_scores = []
     
    def evaluate(self, curr_dictionary):
        """
        Return the length of the keys, which corresponds to the fitness 
        (diversity of ingredients).
       
        Args: 
            curr_dictionary: current dictionary of the sort list
        """

        return len(curr_dictionary.ingredients_dictionary.keys())
        
    def evaluate_unique_ingredients(self, curr_recipe):
        """
        Calls evaluate_novel_ingredient on the current recipe.

        Args:
            curr_recipe: the current recipe
        """

        return curr_recipe.evaluate_novel_ingredient(self.inspiring_set)

    def evaluate_ingredient_cohesion(self, curr_recipe):
        """
        Calls evaluate_ingredient_cohesion on the current recipe.

        Args:
            curr_recipe: the current recipe
        """

        return curr_recipe.evaluate_ingredient_cohesion()

    def evaluate_essential_ingredient(self, curr_recipe):
        """
        Calls evaluate_essential_ingredient on the current recipe.

        Args:
            curr_recipe: the current recipe
        """

        return curr_recipe.evaluate_essential_ingredient

    def evaluate_ingredients_length(self, curr_recipe):
        """
        Calls evaluate_ingredients_length on the current recipe.

        Args:
            curr_recipe: the current recipe
        """

        return curr_recipe.evaluate_ingredients_length

    def combo_evaluate(self, curr_recipe):
        """
        Returns the combined average of evaluations (novel ingredients, 
        ingredient cohesion, essential ingredients, and ingredients length).

        Args:
            curr_recipe: the current recipe
        """

        avg_score = curr_recipe.evaluate_novel_ingredient(self.inspiring_set) \
             * curr_recipe.evaluate_ingredient_cohesion() * \
                curr_recipe.evaluate_essential_ingredients() * \
                    curr_recipe.evaluate_ingredients_length()
        
        self.average_scores.append(avg_score)
        return avg_score


    def rank_initial_cohesion(self, recipe_array):
        """
        Sort array of recipes by the cohesion of its ingredients.

        Args:
            array: array of recipes

        """

        recipe_array.sort(reverse=True, key=self.evaluate_ingredient_cohesion)   
        return recipe_array

    def rank(self, recipe_array): 
        """
        Ranks the recipes on the basis of the evaluate function.
        
        Args:
            array: array of recipes
        """       
        recipe_array.sort(reverse=True, key=self.combo_evaluate)   
        return recipe_array

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
            self.pantry.update_pantry_categories(recipe.ingredients_dictionary)
        self.inspiring_set = copy.deepcopy(self.cookbook)
        self.cookbook = self.rank_initial_cohesion(self.cookbook)

    def get_pivot_array(self):
        """
        Gets an array of the ingredients on one side of the pivot.
       
        Args:
            none
        """

        pivot_array = [recipe.pivot() for recipe in self.cookbook]
        return pivot_array
    
    def convert_to_dict(self, baby_recipe):
        """
        Fills an empty dictionary by taking the baby_recipe array and arranging 
        its contents into key, value pairs.
     
        Args:
            baby_recipe: the recipe created from merging parent recipes
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
            new_cookbook: the cookbook the recipe files will be made from
        """

        for recipe in new_cookbook:
            recipe.save_recipe_cookbook(self.curr_generation, self.curr_time, \
                self.target_generation)
    
    def get_pivot(self, pivot_array, i):
        """
        Returns the current and next pivot from the pivot array.

        Args:
            pivot_array: the array of pivots
            i: current index within the pivot array
        """
        
        first_pivot = pivot_array[i] 
        second_pivot = pivot_array[i+1] 
        return first_pivot, second_pivot

    def get_parents(self, i):
        """
        Returns lists of the parent1's ingredients and parent2's ingredients.

        Args:
            i: the current parent's index in the cookbook
        """

        parent1 = list(self.cookbook[i].ingredients_dictionary.items())
        parent2 = list(self.cookbook[i+1].ingredients_dictionary.items())
        return parent1, parent2

    def partition_parent1(self, first_pivot, parent1):
        """
        Partitions parent1 into the first and second pivot halves.

        Args:
            first_pivot: pivot for parent1
            parent1: parent1's ingredient list from get_parents
        """

        parent1_first_half, parent1_second_half = \
                parent1[:first_pivot], parent1[first_pivot:]
        return parent1_first_half, parent1_second_half
    
    def partition_parent2(self, second_pivot, parent2):
        """
        Partitions parent2 into the first and second pivot halves.

        Args:
            first_pivot: pivot for parent2
            parent1: parent2's ingredient list from get_parents
        """

        parent2_first_half, parent2_second_half  = \
            parent2[:second_pivot], parent2[second_pivot:]
        return parent2_first_half, parent2_second_half

    def merge_parents(self, parent1_first_half, parent1_second_half, \
        parent2_first_half, parent2_second_half):
        """
        Merges parent1 halves and parent2 halves to make new recipes.
        
        Args:
            parent1_first_half: first half of the array of parent1
            parent1_second_half: second half of the array of parent1
            parent2_first_half: first half of the array of parent2
            parent2_second_half: second half of the array of parent2
        """
        
        first_baby_arr = parent1_first_half + parent2_second_half
        second_baby_arr = parent1_second_half + parent2_first_half
        first_baby_dict = self.convert_to_dict(first_baby_arr)
        second_baby_dict = self.convert_to_dict(second_baby_arr)
        return first_baby_dict, second_baby_dict

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
            first_pivot, second_pivot = self.get_pivot(pivot_array, i)
            parent1, parent2 = self.get_parents(i)
        
            parent1_first_half, parent1_second_half = \
                self.partition_parent1(first_pivot, parent1)
        
            parent2_first_half, parent2_second_half = \
                self.partition_parent2(second_pivot, parent2)
            
            new_babies = self.merge_parents(parent1_first_half, \
                parent1_second_half, parent2_first_half, parent2_second_half)

            first_baby_dict, second_baby_dict = new_babies

            # add together parents' mutations in lineage to then 
            # sum those for the new babies 
            parent_mutations_in_lineage = self.cookbook[i].mutations_in_lineage + \
                self.cookbook[i+1].mutations_in_lineage

            # self.cookbook[i], self.cookbook[i+1]
            # create new baby instances
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

            self.pantry.update_pantry_categories(first_baby.ingredients_dictionary)
            self.pantry.update_pantry_categories(second_baby.ingredients_dictionary)
        

            baby_list.append(first_baby)
            baby_list.append(second_baby)

        new_baby_list = self.rank(baby_list)

        # extract the 50% best of the older cookbook and the 50% 
        # best of the baby list to make new cookbook 
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
        
        print(self.pantry.pantry)
        print(self.pantry.category_dictionary)