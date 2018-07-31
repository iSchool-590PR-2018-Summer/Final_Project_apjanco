import numpy as np
import matplotlib.pyplot as plt
import random


total_images = 60000
samples = 10000  # use only one samples variable so no mismatch between variables


class Bag:
    '''An object to store Bag Variable Settings.  Time between when a new bag is available to process.
       Each bag is a compressed file using the LOC baggit structure.
       Values are in minutes
    '''
    def __init__(self):
        self.low = 0
        self.likely = 2800
        self.high = 10080
        self.confidence = 2

class Bag_Size:
    '''Bag Size Variables.  Creates a distribution of bag sizes.
   Values are in bytes'''

    def __init__(self):
        self.low = 1103657593 #Bags can be received in batches via USB drive
        self.likely = 5165691277
        self.high = 9502383139
        self.confidence = 15

class Download:
    '''Download speed.  Time needed to download the bag from object storage to the server running Archivematica.'''
    def __init__(self):
        self.low = 90000000 #b/min
        self.likely = 390000000 #b/min
        self.high = 480000000 #b/sec
        self.confidence = 6

class Archivematica:
    '''Archivematica Variable Settings. Time needed by Archivematica to transfer and ingest a bag.  Output
    is a DIP (jpg files for access with metadata) and AIP (tiff files for preservation and metadata).
   Values are in minutes'''

    def __init__(self):
        self.low = 20 #Bags can be received in batches via USB drive
        self.likely = 40 #minutes
        self.high = 200
        self.confidence = 6
class Transcription:
    '''Transcription Settings. Time needed by students to manually transcribe images.
    Values are in minutes'''

    def __init__(self):
        i = 0
        student_max = 100
        student_min = 10
        while i < 10000:
            number_of_students = random.randrange(1, 6, 1)  # between one and six workers
            pages_per_minute = random.randrange(1, 3, 1)  # between 1 and 3 pages/minute
            student_work_hours = random.randrange(1, 4, 1)  # variable hours between one and four per week
            number_of_images = random.randrange(50, 120, 1)  # variable number of images per bag.
            student_time = number_of_students * (pages_per_minute * (student_work_hours/60) / number_of_images)
            i += 1
            if student_time > student_max:
                student_max = student_time
            if student_time < student_min:
                result_min = student_time

        self.low = student_min
        self.likely = student_max - student_min
        self.high = student_max
        self.confidence = 3




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



### Calculate distributions for each variable
bag = Bag()
bag_values = mod_pert_random(bag.low, bag.likely, bag.high, bag.confidence, samples)

bag_size = Bag_Size()
download = Download()
download_values = mod_pert_random((bag_size.low /download.low) , (bag_size.likely / download.likely), (bag_size.high / download.high), download.confidence, samples)

archivematica = Archivematica()
archivematica_values = mod_pert_random(archivematica.low, archivematica.likely, archivematica.high, archivematica.confidence, samples)

transcribe = Transcription()
transcribe_values = mod_pert_random(transcribe.low, transcribe.likely, transcribe.high, transcribe.confidence, samples)

'''BENCHMARKS
   Here I compute the shortest, median and longest time values in the numpy arrays.
   Will the Monte Carlo results simply return the same values or are they more effective?
'''

print('Shortest time to completion is: ', bag_values.min() + archivematica_values.min() + transcribe_values.min())
print('Median time to completion is: ', np.median(bag_values) + np.median(archivematica_values) + np.median(transcribe_values))
print('Longest time to completion is: ', bag_values.max() + archivematica_values.max() + transcribe_values.max())



def choose_random(values):
    '''A function that takes a numpy array probability distribution as input.  It then randomly chooses from the possible
    index values to select a value from the array.
    param: values, a numpy array
    return: single random value from the array'''
    index = random.randrange(0, values.shape[0], 1)
    time =  values[index]
    return time

result_max = 1000
result_min = 100

simulation = 1000000 # number of times that the simulation is run
if __name__ == '__main__':
    i = 0
    avg = []
    while i < simulation:
        time = choose_random(bag_values) + choose_random(download_values) + choose_random(archivematica_values) + choose_random(transcribe_values)
        i += 1
        avg.append(time)
        if time > result_max:
            result_max = time
        if time < result_min:
            result_min = time
    result_avg = sum(avg)/len(avg)

    print('MC Shortest time to completion is: ', result_min)
    print('MC Average time to completion is: ', result_avg)
    print('MC Longest time to completion is: ', result_max)


    #Idea, work in whole integers rather than long floats

    #Train the bag and archivematical objects to find the optimal path, optimize their parameters

