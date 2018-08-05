# 590PR Final_Project

This is a Monte Carlo simulation for digitization projects.  It can be useful to generate time estimates given a number of variables for transfer, ingest, and processing.  It is built around the workflow currently being used by Haverford College in our project with the Grupo de Apoyo Mutuo in Guatemala.  Our partners in Guatemala scan their records and upload them as zipped [LOC baggit files](https://tools.ietf.org/id/draft-kunze-bagit-14.txt) to cloud [object storage](https://www.digitalocean.com/products/storage/).  The simulation uses a modified probability density function (PERT) to generate values for the Monte Caro simulation.  For each variable, a probabilty distribution is created given estimates for the lowest value expexted, the most likely value and the highest value expected.  There is also a confidence score, which establishes the indicates higher or lower confidence in the expected values.  Each time that the simulation is run, a random value is chosen from the PERT distribution.  A benchmark is printed to compare the results of the Monte Carlo simulation as compared to simply taking the maximum, minimum and median values from the distributions.  The model also compares simulations with relatively hight and low uncertainty in transcription and processing.  These values can be useful for generating a relatively conservative estimate to compare against the standard Monte Carlo and the benchmark.    

### Prerequisites
The script was written using Python 3.6.5. 
To run the script, you will need to install numpy:<br>
`pip install numpy`

## Running the tests

Explain how to run the automated tests for this system


## Authors

* **Andrew Janco** - *For University of Illinois iSchool 590PRO, Summer 2018* - [@apjanco](https://github.com/apjanco)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
