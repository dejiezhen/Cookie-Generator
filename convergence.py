
from cookbook import Cookbook 
import matplotlib.pyplot as plt 


class Convergence:
    def __init__(self, cookbook) -> None:
        """

        """
        self.cookbook = cookbook
        self.generation_scores = []
     
    def generation_data(self):
        
        average_scores = self.cookbook.average_scores
        print(len(average_scores))
        for i in range(0, len(average_scores), 12):
            generation_average = sum(average_scores[i:i+12]) / 12
            print("gen avg: " + str(generation_average))
            self.generation_scores.append(generation_average)

        print(self.generation_scores)
        print(len(self.generation_scores))

    def plotting(self):
        plt.plot(list(range(1, len(self.generation_scores)+1)), \
            self.generation_scores)

        # naming the x axis 
        plt.xlabel('generation') 
        # naming the y axis 
        plt.ylabel('average score') 
            
        # giving a title to my graph 
        plt.title('My first graph!') 
    
        plt.show() 
