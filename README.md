Code Breakdown
main.py
The main function takes user input to determine the number of cookie generations, the probability that a recipe is mutated, and whether the user wants to generate a statistics plot of fitness across generations. Recipe files are inputted here to begin the generation of recipes.

convergence.py
If the user wants a statistics plot, the main function creates an instance of the Convergence class to collate data relating to generation fitness averages and plots it.

cookbook.py
The main creates an instance of the cookbook class using the inputted recipes from main and begins breeding generations by looping the merge function to create new recipes/files until the targeted generation is reached. 
The file contains five methods of evaluating fitness: the number of ingredients, the number of ingredients, the cohesiveness of ingredients, the number of essential ingredients, and the length of the ingredients.
In essence, the merge function merges parent recipes by their pivot arrays to create two new recipes, which can them be mutated before being placed in a ranked cookbook. This process is done until a generation is created.

recipe.py
recipe.py houses the Recipes class that is initialized by the file, ingredients dictionary and pantry from the Cookbook class; it deals specifically with the maintenance of recipes which includes processing them from files, determining the pivots, normalization, mutations, and other recipe specific functions.

flavor_pairing.py
flavor_pairing.py is primarily concerned with the similarity of ingredients and the pairing of ingredients and uses the dot product to do so; it contains methods used to determine the similarity of ingredients using dot product, create a dictionary of ingredient pairings for an ingredient, and displaying those pairings in a human readable format.

ingredients.py
This file is made to manage the ingredient categories and the pantry; it ensured that both are update and has the mechanisms needed to change aspects of the ingredients as generations are created.

Two Distinct Creativity Metrics
The user is initially asked if they want to generate a statistics plot; if so, an instance of the Convergence class appends the average scores of recipe generations to its generation scores variable and then plots it. Plotting average fitness across all generations allows us to see the marginal rise in fitness and its plateau, which allows us to infer the benefit of an additional generation. The statistics plot allows us to understand when an additional generation provides tangible increases in fitness or when it is ineffectually swapping non-essential ingredients.
Though it is not explicitly shown to the user, we also keep track of the number of mutations in a recipe’s lineage; this is done in the merge function by updating a recipe instance’s mutations_in_lineage with the number of mutations in their parents’ lineage (plus one if the recipe is also being mutated). in a recipe’s class instance in the merge function. Mutations change the contents of recipes, which goes beyond simply merging parents and directly affects the fitness of a recipe. Knowing the number of mutations in a recipe’s lineage helps us determine if there is a relationship between the number of mutations and the fitness of a recipe and generations by extension.
The idea is that these two metrics combined would give us a sense as to when recipes reach their peak fitness and what leads those recipes to their peak.

*metrics subfolder*
