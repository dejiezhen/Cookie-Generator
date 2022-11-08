"""
Sofía Hamby, Khalil Jackson, Bjorn Ludwig, and Dejie Zhen
CSCI 3725
PQ2: Presentation Day
10/20/2022

convergence.py contains methods used to collate data relating to generation 
fitness averages and mutation rates.

This file contains the followign functions...
    - generation_data: appends average score of every 12 recipe scores
    - plotting: returns a plot that tracks average scores over time through 
        multiple generations
    - convergence_value: take the average of the converged second half of 
        score data
"""

import matplotlib.pyplot as plt 

class Convergence:

    def __init__(self, cookbook, mutation_rate) -> None:
        """
        Initializes the Convergence class with cookbook and mutation rate.

        Args:
            cookbook: cookbook of recipes
            mutation_rate: mutation rate inputted from user
        """

        self.cookbook = cookbook
        self.generation_scores = []
        self.mutation_rate = mutation_rate
     
    def generation_data(self):
        """
        Appends average score of every 12 recipe scores (1 generation) 
        that will be used to plot our data.
       
        Args: 
            None
        """

        average_scores = self.cookbook.average_scores
        
        for i in range(0, len(average_scores), 12):
            generation_average = sum(average_scores[i:i+12]) / 12
            print("gen avg: " + str(generation_average))
            self.generation_scores.append(generation_average)

    def plotting(self):
        """
        Return a plot that tracks average scores over time through multiple
        generations.
       
        Args: 
            None
        """
        
        plt.plot(list(range(1, len(self.generation_scores)+1)), \
            self.generation_scores)
        
        if len(self.generation_scores) >= 300: 
            plt.hlines(self.convergence_value(), 1, \
                len(self.generation_scores), color="red")

        # naming the x axis 
        plt.xlabel('generation') 

        # naming the y axis 
        plt.ylabel('average score') 
            
        # giving a title to the graph 
        plt.title('Average Score per Generation (Mutation Rate: ' + \
            str(self.mutation_rate) + ')') 
        plt.show() 

    def convergence_value(self):
        """
        Take the average of the converged second half of score data, assuming 
        we have over 300 generations. 
        
        Args:
            None
        """

        sum_second_half = \
            sum(self.generation_scores[len(self.generation_scores)//2:])

        average_second_half = sum_second_half / (len(self.generation_scores)/2)

        return average_second_half