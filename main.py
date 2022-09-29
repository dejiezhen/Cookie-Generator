"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Generation Day
09/29/22

The main function takes user input to determine the number of cookie generations 
and probability of mutation before breeding generations using a newly created 
cookbook instance. 
"""


from cookbook import Cookbook
import os
import glob


def get_generation_value():
    generation_val = input("How many cookie generations do you want? ")
    return generation_val

def get_mutation_probability():
    mutation_rate = float(input("What probability do you want the cookie \
recipes to mutate (0.0 to 1.0, inclusive)?"))
    
    if mutation_rate < 0 or mutation_rate > 1:
        mutation_rate = input("What probability do you want the cookie \
recipes to mutate (0.0 to 1.0, inclusive)?")
    
    if mutation_rate != 0 and not mutation_rate:
        print('Automatically setting the mutation rate to 50%')
        mutation_rate = .5
    
    return mutation_rate


def main():
    generation_val = get_generation_value()
    mutation_rate = get_mutation_probability()
    input_path = './input'
    dir_list = os.listdir(input_path)
    initial_cookbook = Cookbook(dir_list, generation_val, mutation_rate)
    initial_cookbook.breed_generations()


if __name__ == '__main__':
    main()

