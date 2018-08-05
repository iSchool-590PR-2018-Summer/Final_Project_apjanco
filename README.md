# 590PR Final_Project
## Monte Carlo Simulation Scenario & Purpose:<br>
This is a Monte Carlo simulation for the management of digitization projects.  It can be useful to generate time estimates given a number of variables for transfer, ingest, and processing.  It is built around the workflow currently being used by Haverford College in our project with the *Grupo de Apoyo Mutuo* in Guatemala.  Our partners in Guatemala scan their records and upload them as zipped [LOC baggit files](https://tools.ietf.org/id/draft-kunze-bagit-14.txt) to cloud [object storage](https://www.digitalocean.com/products/storage/).  The simulation uses a modified probability density function (PERT) to generate values for the Monte Caro simulation.  For each variable, a probability distribution is created given estimates for the lowest value expected, the most likely value and the highest value expected.  There is also a confidence score, which indicates higher or lower confidence in the given values.  Each time that the simulation is run, a random value is chosen from the PERT distribution.  A benchmark is printed to compare the results of the Monte Carlo simulation as compared to simply taking the maximum, minimum and median values from the distributions.  The model also compares simulations with relatively high and low uncertainty in transcription and processing.  These values can be useful for generating a relatively conservative estimate to compare against the standard Monte Carlo and the benchmark.      

## Simulation's variables of uncertainty
The simulation models the following variables:
- The time between bags.  This simulates the fact that we never know when a new bag will be uploaded by the GAM.  Sometimes we receive dozens of them at once via USB, while at other times the transfer fails given connectivity issues and a bag must be re-uploaded. 
- The size of each bag.  The simulation creates a distribution that models variance in the size of each uploaded bag.  
- The size of the tiff files in each bag is also variable.  
- The time to download the bag from object storage is relatively constant but can vary none-the-less.  This was a good variable to represent a highly consistent and confident variable. 
- Once downloaded, the bags are processed using an open-source application called [Archivematica](https://www.archivematica.org/en/). The application decompresses and checks fixity of the files in the bag.  It then generates preservation metadata, creates an AIP for preservation (tiffs) in DuraCloud and DIP (jpegs) for our processing and access applications.  The time required to transfer and ingest our materials depends mostly on the size of the bag, but can be very computationally intensive.  We are currently using a machine with a 6-core Xeon processor for these tasks. 
- Finally, the images are transcribed and authority records are created for people, places, and organizations in the archive.  This work is done by student employees and volunteer community members using our processing application.  This variable is the least predictable and can be highly irregular.  To model this irregularity, the model will drop a given percentage of values from the probability distribution to simulate irregularity of work. 

## Hypothesis or hypotheses before running the simulation:
Given a high level of irregularity, I would expect that the irregular simulation would require a significantly longer period of time to complete a given number of images. 

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
Greater irregularity is most visible on the extremes of the prediction.  The benchmark, simple simulation and irregular simulation all have similar values on the average.  It is 3865 for the benchmark, 4086 for simple and 4028 for irregular.  The minimal value for the irregular model is closer to benchmark than Simple Monte Carlo.  However, the maximum for Irregular is higher. While I expected that irregularity would be exhibited in higher overall values, it actually returns a much larger range between the minimum and maximum predictions.  

| Simulation   | Minimum (work weeks) | Average (work weeks) | Maximum (work weeks) |
|--------------|:--------------------:|----------------------|----------------------|
| Benchmark    | 18.56                | 1402.60              | 3752.23              |
| Simple MC    | 48.95                | 2000.28              | 5000.12              |
| Irregular MC | 22.57                | 2142.54              | 5432.75              |

### Prerequisites
The script was written using Python 3.6.5. 
To run the script, you will need to install numpy:<br>
`pip install numpy`

## Authors

* **Andrew Janco** - *For University of Illinois iSchool 590PRO, Summer 2018* - [@apjanco](https://github.com/apjanco)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## All Sources Used:
Jeff Bradberry, *Introduction to Monte Carlo Tree Search* [(blog, 07 September 2015)](https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/)


