import getopt
import sys
import math
import random
import time
import numpy as np

import matplotlib
from matplotlib.ticker import FormatStrFormatter

#import warnings
#warnings.filterwarnings("ignore")

simu_len_picked = False

x_label = "Predicted days-to-completion"
y_label = "Number of Simulations"
title = "Simulation Results"

# code to bootstrap matlablib
gui_env = ['TKAgg','GTKAgg','Qt4Agg','WXAgg']
for gui in gui_env:
    try:
        #print ("testing", gui)
        matplotlib.use(gui, force=True)
        from matplotlib import pyplot as plt
        break
    except:
        continue

# main simulation class
class Simulation:
    def __init__(self,velocity_array,simulation_length,days_in_sprint,forecasting_points):
        
        # velocity_array is a list of number of points completed in previous sprints
        # simulation_length is an integer specifying number of simulations to run
        # days_in_sprint is the number of days over which the points in velocity_array were completed
        
        # forecasting_points is the current sprint backlog for which you'd like an estimate
        # of days-to-completion. If not provided, will be the average of the list of previous
        # completed sprint points
        
        self.days_in_sprint = days_in_sprint
        
        # here, velocity_array is converted into sprint points per day
        self.velocity_array = [velocity/self.days_in_sprint for velocity in velocity_array]
        
        self.simulation_length = simulation_length
        self.forecasting_points = forecasting_points
        
        # If forecasting points is not provided, predict average days-to-completion
        if forecasting_points == '':
            self.forecasting_points = int(sum(velocity_array)/len(velocity_array))
        
        # simu_target should have just been days_in_sprint:
        # if your sprints are 10 days long, your target is to complete the next one
        # in less than 10 days.
        
        self.simu_target = days_in_sprint
        self.count_below_target = 0

    @property
    def avg(self):
        # This returns the average sprint velocity in points per day
        a = 0.0
        if self.velocity_array is not None:
        # a = sum(self.velocity_array) / len(self.velocity_array)
            a = np.mean(self.velocity_array)
        return a
    
    @property
    def variance(self):
        # No longer using this function, it's a numpy built-in
        return sum([d*d for d in  [(x-self.avg) for x in self.velocity_array]])/len(self.velocity_array)

    def plot_hist(self,samples,bins=10):
        
        # Compute histogram of
        hist, bins = np.histogram(samples, bins=bins)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.ion()
        plt.clf()
        plt.bar(center, hist, align='center', width=width)
        plt.xticks(center)
        ax = plt.gca()
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        print("Bin #\t\t",end='')
        for i in range(1,len(bins)):
            print("{:=6d}".format(i),end='\t')
        print("\nBin boundary:\t",end='')
        for x in bins:
            print("{:4.2f}".format(x),end='\t')
        print("\n# runs in Bin:\t",end='')
        for i in hist: 
            print("{:=6d}".format(i),end='\t')
        print("\n")

    def print_results(self):
        results = """{0} out of {1} runs completed in {2} days or less. That’s a {3}% chance of completing the proposed\n{4}-point backlog within the sprint. 95% of simulations completed in {5} days or less.\n"""
        percent = 100.0 * self.count_below_target / self.simulation_length
        msg = results.format(self.count_below_target,
                             self.simulation_length,
                             self.days_in_sprint,
                             np.round((percent), 1),
                             self.forecasting_points,
                             np.round(np.percentile(self.samples,95), 1))
        print(msg)

    def run_simulation(self):
        
        # n = len(self.velocity_array)

        # Use numpy's built-in standard deviation
        sd = np.std(self.velocity_array)
        # sd = n * math.sqrt(self.variance) / (n-1)

        # Use numpy's built-in normal distribution sampler
        self.velocity_samples = np.random.normal(self.avg, sd, self.simulation_length)
        # Clip to be above zero, just in case
        # self.velocity_samples[self.velocity_samples<=0]=1e-3
        # replaced line above with this line, setting minimum possible sprint velocity to 1 point per day
        self.velocity_samples[self.velocity_samples<=1]=1
        # distribution = lambda : random.gauss(self.avg,sd)
        # self.samples = [ distribution() for _ in range(1,self.simulation_length)]

        # Those were samples of sprint velocities. To compute
        # days-to-completion, we need to calculate forecasting_points/sprint_velocity
        # This gives us points / (points/day) -> days
        self.samples = self.forecasting_points / self.velocity_samples
        
        # Finally, count how many simulations predict sprint completion sooner than days_in_sprint
        self.count_below_target = np.sum(self.samples <= self.simu_target)
        # for sample in self.samples:
            # if sample < self.simu_target:
                # self.count_below_target += 1

        print("============================================= RESULTS ==================================================")
        # print("Days in sprint: ",self.days_in_sprint)
        # print("Number of simulations run: ",self.simulation_length)
        # print("Average points per sprint: ",int(self.avg*self.days_in_sprint))
        print("Forecasted points:",int(self.forecasting_points))
        print("\n")
        self.print_results()
        self.plot_hist(self.samples)
        print("========================================================================================================")
        print("\n")
 
# helper code to get user input
def get_int_from_user(msg,blank=False):
    
    # Ask user for an integer, accept blank input if blank=True
    # Return the integer as int
    
    integer_input = None
    while integer_input is None:
        try:
            integer_input = input(msg)
            if integer_input == '' and blank:
                return ''
            integer_input = int(integer_input)
        except ValueError:
            print("Please enter an integer value")
            integer_input = None
    return integer_input

def get_intlist_from_user(msg):
    
    # Ask user for a comma-separated list of integers
    # Return as list of ints
    
    integer_input = map(int,input(msg).split(","))
    return list(integer_input)

# simulation driver
if __name__ == '__main__':
    print("\n")
    print("==================== WELCOME TO THE SPRINT PLANNING SIMULATOR ====================")
    print("This tool is designed to assist teams with understanding the probability of\ncompleting their forecasted sprint backlog, based on their historical velocity.")
    print("\n")
    input("Press Enter to continue...")
    print("\n")

    velocities = get_intlist_from_user("Enter team's historical velocity in story points (comma separated): ")
    print("\n")
    days_n = get_int_from_user("Enter the number of working days in sprint: ")
    print("\n")
    cont = True
    while cont:
        sprint_points = get_int_from_user("Enter the forecasted number of sprint backlog points: ",blank=True)
        print("\n")
        print("Running 100,000 simulations to determine probability of completing the work on time...")
        print("\n")
        time.sleep(2)
        if not simu_len_picked:
            simu_len_picked = True
            simu_points_n = int("100000")
            # simu_points_n = get_int_from_user("Enter the number of simulations to run: ") 
        simu = Simulation(velocities,simu_points_n,days_n,sprint_points)
        simu.run_simulation()

        run_again = input("Would you like to run another scenario? (Y/N): ")
        if not "Y" in run_again:
            cont = False
