"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Presentation Day
10/20/2022

The main function takes user input to determine the number of cookie 
generations and probability of mutation before breeding generations using a 
newly created cookbook instance.  It also asks user if they want a plot of 
average fitness of each generation. 

This file contains the following functions...
    - get_generation_value: gets user input to determine the number of cookie 
        recipe generations
    - get mutation probability: gets user input to determine the mutation rate 
        of the cookie recipes
    - generate_statistic_plot: generates a statistics plot tracking the average
        fitness of each generation
"""

from cookbook import Cookbook
from convergence import Convergence
import os

def get_generation_value():
    """
    Gets user input to determine the number of cookie recipe generations 
    and ensures that the value is a digit.
    """

    #asks user to input the number of cookie generations
    generation_val = input("How many cookie generations do you want? ")

    #ensures generation_val is a digit and greater than one
    while not generation_val.isdigit() or int(generation_val) < 1:
        print('Please input a valid generation value!')
        generation_val = input("How many cookie generations do you want? ")
    return generation_val

def get_mutation_probability():
    """
    Gets user input to determine the mutation rate of the cookie recipes 
    and ensures it is a value between 0 and 1, inclusive.
    """

    #asks user to input the rate of mutation
    mutation_rate = input("What probability do you want the cookie \
    recipes to mutate (0.0 to 1.0, inclusive)?")

    #sets mutation rate to 0.5 if use wants it done automatically
    if mutation_rate != 0 and not mutation_rate:
        print('Automatically setting the mutation rate to 50%')
        mutation_rate = 0.5
        return mutation_rate
    
    #asks to input new rate if it is less than zero or greater than one
    while float(mutation_rate) < 0 or float(mutation_rate) > 1:
        print('Please input a valid mutation rate. You can also press \
        enter for default mutation value\n')
        mutation_rate = input("What probability do you want the cookie \
        recipes to mutate (0.0 to 1.0, inclusive)?")
    
        #again gives the user an option to automatically set rate
        if mutation_rate != 0 and not mutation_rate:
            print('Automatically setting the mutation rate to 50%')
            mutation_rate = 0.5
            return mutation_rate
    
    return float(mutation_rate)

def generate_statistic_plot():
    """
    Generates a statistics plot tracking the average fitness of each 
    generation to show were average fitness plateaus.
    """

    generate_plot = input('Would you like to generate a statistic plot?(y/n)')
    while generate_plot.lower() != 'y' and generate_plot.lower() != 'n':
        generate_plot = input('Would you like to generate a statistic plot?(y/n)')
    if generate_plot.lower() == 'y':
        return True

def main():
    """
    Gets user input for the number of generations and mutation 
    rate before inputting files for the inspiring set and breeding 
    generations using a Cookbook.
    """

    generation_val = get_generation_value()
    mutation_rate = get_mutation_probability()
    input_path = './input'
    dir_list = os.listdir(input_path)
    initial_cookbook = Cookbook(dir_list, generation_val, mutation_rate)

    #breeds generations and creates plot if user says so 
    #otherwise, only breeds generations
    if generate_statistic_plot():
        initial_cookbook.breed_generations()
        convergence_instance = Convergence(initial_cookbook, mutation_rate)
        convergence_instance.generation_data()
        convergence_instance.plotting()
    else:
        initial_cookbook.breed_generations()

if __name__ == '__main__':
    main()