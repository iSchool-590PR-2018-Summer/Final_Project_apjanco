import numpy as np
import matplotlib.pyplot as plt
import random


total_images = 60000


'''Bag Variable Settings.  Time between when a new bag is available to process. 
   Each bag is a compressed file using the LOC baggit structure.
   Values are in minutes'''
bag_low = 0 #Bags can be received in batches via USB drive
bag_likely = 2880 #minutes
bag_high = 10080
bag_confidence = 2
samples = 10000 #use only one samples variable so no mismatch between variables
#def lower_variation():
    #reduct difference of low and high

'''Bag Size Variables.  Creates a distribution of bag sizes. 
   Values are in bytes'''
bag_size_low = 1103657593 #Bags can be received in batches via USB drive
bag_size_likely = 5165691277
bag_size_high = 9502383139
bag_size_confidence = 15


'''Download speed.  Time needed to download the bag from object storage to the server running Archivematica.'''
download_low = 90000000 #b/min
download_likely = 390000000 #b/min
download_high = 480000000 #b/sec
download_confidence = 6

'''Archivematica Variable Settings. Time needed by Archivematica to transfer and ingest a bag.  Output 
is a DIP (jpg files for access with metadata) and AIP (tiff files for preservation and metadata). 
   Values are in minutes'''
archivematica_low = 20 #Bags can be received in batches via USB drive
archivematica_likely = 40 #minutes
archivematica_high = 200
archivematica_confidence = 6




def mod_pert_random(low, likely, high, confidence, samples):
    """Produce random numbers according to the 'Modified PERT'
    distribution.
    Source: https://github.com/iSchool-590PR-2018-Summer/in-class-examples/blob/master/class12_Prob_Distributions.ipynb

    :param low: The lowest value expected as possible.
    :param likely: The 'most likely' value, statistically, the mode.
    :param high: The highest value expected as possible.
    :param confidence: This is typically called 'lambda' in literature
                        about the Modified PERT distribution. The value
                        4 here matches the standard PERT curve. Higher
                        values indicate higher confidence in the mode.
                        Currently allows values 1-18

    Formulas from "Modified Pert Simulation" by Paulo Buchsbaum.
    """
    # Check minimum & maximum confidence levels to allow:
    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta




bag_values = mod_pert_random(bag_low, bag_likely, bag_high, bag_confidence, samples)

download_values = mod_pert_random((bag_size_low /download_low) , (bag_size_likely / download_likely ), (bag_size_high / download_high), download_confidence, samples)

archivematica_values = mod_pert_random(archivematica_low, archivematica_likely, archivematica_high, archivematica_confidence, samples)

'''BENCHMARKS
   Here I compute the shortest, median and longest time values in the numpy arrays.
   Will the Monte Carlo results simply return the same values or are they more effective?
'''

print('Shortest time to completion is: ', bag_values.min() + archivematica_values.min())
print('Median time to completion is: ', np.median(bag_values) + np.median(archivematica_values))
print('Longest time to completion is: ', bag_values.max() + archivematica_values.max())



def choose_random(values):
    '''A function that takes a probability distribution as input.  It then randomly chooses from the possible
    index values to select a value from the array.
    param: values, a numpy array
    return: single random value from the array'''
    index = random.randrange(0, values.shape[0], 1)
    time =  values[index]
    return time

result_max = 1000
result_min = 100

i = 0
while i < 10000:
    time = choose_random(bag_values) + choose_random(download_values) + choose_random(archivematica_values)
    i += 1
    if time > result_max:
        result_max = time
    if time < result_min:
        result_min = time
print(result_min, result_max)


#Idea, work in whole integers rather than long floats

#Train the bag and archivematical objects to find the optimal path
