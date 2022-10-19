
from cookbook import Cookbook 
import matplotlib.pyplot as plt 


class Convergence:
    def __init__(self, cookbook, mutation_rate) -> None:
        """

        """
        self.cookbook = cookbook
        self.generation_scores = []
        self.mutation_rate = mutation_rate
     
    def generation_data(self):
        """
        Appends average score of every 12 recipe scores (1 generation) 
        that will be used to plot our data
       
        Args: 
            None
        """
        average_scores = self.cookbook.average_scores
        print(len(average_scores))
        for i in range(0, len(average_scores), 12):
            generation_average = sum(average_scores[i:i+12]) / 12
            print("gen avg: " + str(generation_average))
            self.generation_scores.append(generation_average)

        # print(self.generation_scores)
        print(len(self.generation_scores))

    def plotting(self):
        """
        Return a plot that tracks average scores over time through multiple
        generations
       
        Args: 
            None
        """
        plt.plot(list(range(1, len(self.generation_scores)+1)), \
            self.generation_scores)
        
        # plt.plot(list(range(1, len(self.generation_scores)+1)), \
        #     self.convergence_value())

        if len(self.generation_scores) >= 300: 
            plt.hlines(self.convergence_value(), 1, \
                len(self.generation_scores), color="red")

        # naming the x axis 
        plt.xlabel('generation') 
        # naming the y axis 
        plt.ylabel('average score') 
            
        # giving a title to my graph 
        plt.title('Average Score per Generation (Mutation Rate: ' + \
            str(self.mutation_rate) + ')') 
        plt.show() 

    def convergence_value(self):
        """
        Take the average of the converged second half of score data 
        ** ASSUMING WE HAVE OVER 300 GENERATIONS**
        """

        sum_second_half = \
            sum(self.generation_scores[len(self.generation_scores)//2:])

        average_second_half = sum_second_half / (len(self.generation_scores)/2)

        return average_second_half