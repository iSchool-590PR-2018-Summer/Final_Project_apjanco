import numpy as np
import random

'Hyperparameters'
total_images = 60000

samples = 1000000  # use only one samples variable in Modified PERT so no mismatch between variable distributions.

'number of times that the simulation is run'
simulation_iterations = 2000000

'''The percent of values in the transcription distribution that are set to 0. 
This simulates missed shifts and other unforeseen missed work time.'''
irregular_percent = 0.8


class Bag:
    """An object to store Bag Variable Settings.  Time between when a new bag is available to process.
       Each bag is a compressed file using the LOC baggit structure.
       Values are in minutes.  I created classes so that objects for future research questions
       where I search for optimal values for these variables.
    """
    def __init__(self):
        self.low = 0 # Bags can be received in batches via USB drive
        self.likely = 2800
        self.high = 10080
        self.confidence = 2


class BagSize:
    """Bag Size Variables.  Creates a distribution of bag sizes.
   Values are in bytes."""

    def __init__(self):
        self.low = 1103657593
        self.likely = 5165691277
        self.high = 9502383139
        self.confidence = 15

class FileSize:
    """File Size Variables. Creates a distribution of file sizes. Values in bytes."""

    def __init__(self):
        self.low = 83700454
        self.likely = 101128426
        self.high = 102454984
        self.confidence = 15


class Download:
    """Download speed.  Time needed to download the bag from object storage to the server running Archivematica."""
    def __init__(self):
        self.low = 90000000  # b/min
        self.likely = 390000000  # b/min
        self.high = 480000000  # b/sec
        self.confidence = 6


class Archivematica:
    """Archivematica Variable Settings. Time needed by Archivematica to transfer and ingest a bag.  Output
    is a DIP (jpg files for access with metadata) and AIP (tiff files for preservation and metadata).
   Values are in minutes"""

    def __init__(self):
        self.low = 20  # Bags can be received in batches via USB drive
        self.likely = 40  # minutes
        self.high = 200  # Bags can contain errors in which case they must be resent
        self.confidence = 6


class Transcription:
    """Transcription Settings. Time needed by students to manually transcribe images.
    Values are in minutes per image."""

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
                student_min = student_time

        self.low = student_min
        self.likely = student_max - student_min
        self.high = student_max
        self.confidence = 10


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


# Calculate distributions for each variable
def simple_simulation():
    """Produce objects and distributions for the variables, bag, BagSize, Archivematica and Transcribe.
        """
    bag = Bag()
    _bag_values = mod_pert_random(bag.low, bag.likely, bag.high, bag.confidence, samples)

    bag_size = BagSize()
    file_size = FileSize()
    _no_images = mod_pert_random((bag_size.low / file_size.low),
                                (bag_size.likely / file_size.likely),
                                (bag_size.high / file_size.high),
                                file_size.confidence,
                                samples)

    download = Download()
    _download_values = mod_pert_random((bag_size.low /download.low),
                                       (bag_size.likely / download.likely),
                                       (bag_size.high/download.high),
                                       download.confidence,
                                       samples)

    archivematica = Archivematica()
    _archivematica_values = mod_pert_random(archivematica.low,
                                            archivematica.likely,
                                            archivematica.high,
                                            archivematica.confidence,
                                            samples)

    transcribe = Transcription()
    _transcribe_values = mod_pert_random(transcribe.low,
                                         transcribe.likely,
                                         transcribe.high,
                                         transcribe.confidence,
                                         samples)

    return simulation_iterations, _bag_values, _download_values, _archivematica_values, _transcribe_values, _no_images


def irregular_work():
    """Produce objects and irregular distributions for the variables, bag, BagSize, Archivematica and Transcribe.
    """
    bag = Bag()
    _bag_values = mod_pert_random(bag.low, bag.likely, bag.high, bag.confidence, samples)

    bag_size = BagSize()
    file_size = FileSize()
    _no_images = mod_pert_random((bag_size.low / file_size.low),
                                 (bag_size.likely / file_size.likely),
                                 (bag_size.high / file_size.high),
                                 file_size.confidence,
                                 samples)
    download = Download()
    _download_values = mod_pert_random((bag_size.low / download.low), (bag_size.likely / download.likely),
                                      (bag_size.high / download.high), download.confidence, samples)

    archivematica = Archivematica()
    _archivematica_values = mod_pert_random(archivematica.low, archivematica.likely, archivematica.high,
                                           archivematica.confidence, samples)

    transcribe = Transcription()
    transcribe.confidence = 3
    _transcribe_values = mod_pert_random(transcribe.low, transcribe.likely, transcribe.high, transcribe.confidence,
                                        samples)
    #  Randomly sets values in the distribution to 0 based on irregularity
    _percentage = irregular_percent
    irregularity = int(_transcribe_values.size * _percentage)
    drop_index = np.random.choice(_transcribe_values.size, size=irregularity)
    _transcribe_values[drop_index] = 0

    return simulation_iterations, _bag_values, _download_values, _archivematica_values, _transcribe_values, _no_images


def choose_random(values):
    """A function that takes a numpy array probability distribution as input.  It then randomly chooses from the possible
    index values to select a value from the array.
    param: values, a numpy array
    return: single random value from the array"""
    index = random.randrange(0, values.shape[0], 1)
    time = values[index]
    return time


def run_simulation(simulation_iterations, bag_values, download_values, archivematica_values, transcribe_values, no_images):
    """Produce random numbers according to the 'Modified PERT'
        distribution.
        Source: https://github.com/iSchool-590PR-2018-Summer/in-class-examples/blob/master/class12_Prob_Distributions.ipynb

        :param simulation_iterations: Number of times to run the simulation
        :param bag_values: Array of values for bags.
        :param download_values: Array of values for download times.
        :param archivematica_values: Array of values for Archivematica processing time.
        :param transcribe_values: Array of values to model time needed for transcription.
        :param no_images: Distribution of images per bag.
        """
    result_max = 1000
    result_min = 100
    i = 0
    avg = []
    while i < simulation_iterations:
        bag_value = choose_random(bag_values)
        download_value = choose_random(download_values)
        archivematica_value = choose_random(archivematica_values)
        transcribe_value = choose_random(transcribe_values)
        image_value = choose_random(no_images)
        time = bag_value + download_value + archivematica_value + transcribe_value
        i += 1
        avg.append(time)
        if time > result_max:
            result_max = time
        if time < result_min:
            result_min = time
    result_avg = sum(avg) / len(avg)

    return result_min, result_avg, result_max, image_value


def total_time(total_images, no_images, result_min, result_avg, result_max):
    """Calculate the total amount of time needed to process a set number of images.
    :param total_images: The total number of images to be processed.
    :param no_images: The number of images per bag.
    :param result_min: The minimum value returned by run_simulation() after a number of iterations.
    :param result_avg: The average value returned by run_simulation() after a number of iterations.
    :param result_max: The maximum value returned by run_simulation() after a number of iterations.
    """
    total_number_of_images = total_images
    images_per_bag = no_images
    number_of_bags = total_number_of_images / images_per_bag
    min_time_bag = (result_min * number_of_bags)
    avg_time_bag = (result_avg * number_of_bags)
    max_time_bag = (result_max * number_of_bags)

    return min_time_bag, avg_time_bag, max_time_bag


def minutes_to_hours(minutes):
    hours = minutes / 60
    return hours


def minutes_to_work_weeks(minutes: float) -> float:
    hours = minutes / 60
    work_weeks = hours * 0.025 #Conversion from https://www.calculateme.com/Time/Hours/ToWorkWeeks
    return work_weeks


if __name__ == '__main__':

    simulation_iterations, bag_values, download_values, archivematica_values, transcribe_values, no_images = simple_simulation()
    '''BENCHMARKS
       Here I compute the shortest, median and longest time values in the numpy arrays.
       Will the Monte Carlo results simply return the same values? No!
    '''
    b_result_min = bag_values.min() + archivematica_values.min() + transcribe_values.min()
    b_result_avg = np.median(bag_values) + np.median(archivematica_values) + np.median(transcribe_values)
    b_result_max = bag_values.max() + archivematica_values.max() + transcribe_values.max()
    s_images = no_images.max() - no_images.min()
    print('****************************************************')
    print('Benchmark shortest time per bag is: {:.2f}'.format(b_result_min))
    print('Benchmark median time per bag is: {:.2f}'.format(b_result_avg))
    print('Benchmark longest time per bag is: {:.2f}'.format(b_result_max))
    print('Benchmark number of images per bag between {:.2f} and {:.2f}'. format(no_images.min(), no_images.max()))

    min_time_bag, avg_time_bag, max_time_bag = total_time(total_images, s_images, b_result_min, b_result_avg,
                                                          b_result_max)
    print(
        'The total time needed for {} documents is between a minimum of {:.2f} hours (or {:.2f} work weeks), an average of {:.2f} hours ({:.2f} weeks) and a maximum of {:.2f} hours ({:.2f} weeks)'.format(
            total_images, minutes_to_hours(min_time_bag), minutes_to_work_weeks(min_time_bag), minutes_to_hours(avg_time_bag), minutes_to_work_weeks(avg_time_bag),
            minutes_to_hours(max_time_bag), minutes_to_work_weeks(max_time_bag)))

    # Simple simulation
    print('****************************************************')
    s_result_min, s_result_avg, s_result_max, s_images = run_simulation(simulation_iterations, bag_values, download_values, archivematica_values, transcribe_values, no_images)
    print('Simple Monte Carlo Shortest time per bag is: {:.2f}'.format(s_result_min))
    print('Simple Monte Carlo Average time per bag is: {:.2f}'.format(s_result_avg))
    print('Simple Monte Carlo Longest time per bag is: {:.2f}'.format(s_result_max))
    min_time_bag, avg_time_bag, max_time_bag = total_time(total_images, s_images, s_result_min, s_result_avg, s_result_max)
    print(
        'The total time needed for {} documents is between a minimum of {:.2f} hours (or {:.2f} work weeks), an average of {:.2f} hours ({:.2f} weeks) and a maximum of {:.2f} hours ({:.2f} weeks)'.format(
            total_images, minutes_to_hours(min_time_bag), minutes_to_work_weeks(min_time_bag),
            minutes_to_hours(avg_time_bag), minutes_to_work_weeks(avg_time_bag),
            minutes_to_hours(max_time_bag), minutes_to_work_weeks(max_time_bag)))

    # Simulation with irregular work
    print('****************************************************')
    simulation_iterations, bag_values, download_values, archivematica_values, transcribe_values, no_images = irregular_work()
    i_result_min, i_result_avg, i_result_max, i_images = run_simulation(simulation_iterations, bag_values, download_values, archivematica_values, transcribe_values, no_images)
    print('Irregular Monte Carlo Shortest time per bag is: {:.2f}'.format(i_result_min))
    print('Irregular Monte Carlo Average time per bag is: {:.2f}'.format(i_result_avg))
    print('Irregular Monte Carlo Longest time per bag is: {:.2f}'.format(i_result_max))
    min_time_bag, avg_time_bag, max_time_bag = total_time(total_images, i_images, i_result_min, i_result_avg,
                                                          s_result_max)

    print(
        'The total time needed for {} documents is between a minimum of {:.2f} hours (or {:.2f} work weeks), an average of {:.2f} hours ({:.2f} weeks) and a maximum of {:.2f} hours ({:.2f} weeks)'.format(
            total_images, minutes_to_hours(min_time_bag), minutes_to_work_weeks(min_time_bag),
            minutes_to_hours(avg_time_bag), minutes_to_work_weeks(avg_time_bag),
            minutes_to_hours(max_time_bag), minutes_to_work_weeks(max_time_bag)))


"""experiments 
x calculate storage, processing time and total time for given number of images
x scenario where transcription work is consistent versus highly irregular 

as each variable is increased or decreased, what is effect on time to end result (calculate a weight for each step in 
the process) 
high learning curve (rate of progress slowly rises over time) 
academic year only (work only done during academic year) 


Apparently this project is going to take 31 years to complete, omg!
"""
