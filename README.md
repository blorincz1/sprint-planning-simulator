# sprint-planning-simulator
Sprint planning simulator tool for Scrum teams.

## Background
I got the idea for developing this tool while working as an Agile Coach. I read an article about reducing risk and increasing predictability in Scrum using Monte Carlo simulations and it got me thinking. The end result is a tool designed to be used during sprint planning to assist Scrum teams with understanding the probability of completing their forecasted sprint backlog, based on their historical velocity.

## Prerequisites
Python 3.x

## Execution
From the command line run:  
`python spsim.py`

**You will be prompted to:**

`Enter team's historical velocity in story points (comma separated):`  
This is the team’s completed story points per sprint over the past X sprints. Enter values as a comma separated list. The more historical velocity you provide, the better the simulation results will be. We’re using 44, 52, 47, 39, 55, 41, 55 in this example.

`Enter the number of working days in sprint:`  
The number of working days in the sprint. One week is 5, two weeks is 10, etc. We’re using 10 in this example.

`Enter the forecasted number of sprint backlog points:`  
This is the team’s forecasted number of story points for the upcoming sprint. The number of story points they’re *planning* to complete. We’re using 45 in this example.  

## Results
The script will run 100,000 simulations to determine the probability of completing the forecasted number of story points. Using values from the example above, the output will look something like this.

```
Running 100,000 simulations to determine probability of completing the work on time...

============================================= RESULTS ==================================================
Forecasted points: 45

66369 out of 100000 runs completed in 10 days or less. That’s a 66.4% chance of completing the proposed
45-point backlog within the sprint. 95% of simulations completed in 12.0 days or less.

Bin #                1       2       3       4       5       6       7       8       9      10  
Bin boundary:  6.16    7.79    9.42    11.05   12.68   14.31   15.93   17.56   19.19   20.82   22.45   
# runs in Bin:     4633    44091   38198   10724    1922    347     71      10       3       1  

========================================================================================================
```

![Matplotlib graph](https://raw.githubusercontent.com/blorincz1/sprint-planning-simulator/master/plot.png)

**You will be prompted to run another scenario or exit. If you choose to run another scenario, you will only be asked to enter a new forecasted number of story points. The historical velocity and number of days in sprint entered previously are re-used.**
