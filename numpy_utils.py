#!/usr/bin/python

"""
    A general tool for converting data from the
    dictionary format to an (n x k) python list that's
    ready for training an sklearn algorithm

    n--no. of key-value pairs in dictonary
    k--no. of features being extracted

    dictionary keys are names of persons in dataset
    dictionary values are dictionaries, where each
        key-value pair in the dict is the name
        of a feature, and its value for that person

    In addition to converting a dictionary to a numpy
    array, you may want to separate the labels from the
    features--this is what targetFeatureSplit is for

    so, if you want to have the poi label as the target,
    and the features you want to use are the person's
    salary and bonus, here's what you would do:

    feature_list = ["poi", "salary", "bonus"]
    data_array = featureFormat( data_dictionary, feature_list )
    label, features = targetFeatureSplit(data_array)

    the line above (targetFeatureSplit) assumes that the
    label is the _first_ item in feature_list--very important
    that poi is listed first!
"""


import numpy as np


def datapoint_dict_to_numpy(dictionary, features=None, remove_NaN=True, remove_all_zeroes=True,
                            remove_any_zeroes=False):
    if not features:
        # use features from firt
        features = dictionary[keys[0]].keys()

    tmp_list = []
    for feature in features:
        try:
            dictionary[feature]
        except KeyError:
            print "Error: key ", feature, " not present. return from dict_to_numpy."
            return
        value = dictionary[feature]

        if value == "NaN" and remove_NaN:
            value = 0
        tmp_list.append(float(value))

    # Logic for deciding whether or not to add the data point.
    append = True

    if remove_all_zeroes:
        append = False
        for item in tmp_list:
            if item != 0 and item != "NaN":
                append = True
                break

    if remove_any_zeroes:
        if 0 in tmp_list or "NaN" in tmp_list:
            append = False

    return np.array(tmp_list) if append else None


def dict_to_numpy(dictionary, features=None, remove_NaN=True, remove_all_zeroes=True,
                  remove_any_zeroes=False, sort_keys=False):
    """ convert dictionary to numpy array of features
        remove_NaN = True will convert "NaN" string to 0.0
        remove_all_zeroes = True will omit any data points for which
            all the features you seek are 0.0
        remove_any_zeroes = True will omit any data points for which
            any of the features you seek are 0.0
        sort_keys = True sorts keys by alphabetical order. Setting the value as
            a string opens the corresponding pickle file with a preset key
            order (this is used for Python 3 compatibility, and sort_keys
            should be left as False for the course mini-projects).
        NOTE: first feature is assumed to be 'poi' and is not checked for
            removal for zero or missing values.
    """

    return_list = []

    keys = sorted(dictionary.keys()) if sort_keys else dictionary.keys()

    return_arr = np.array()
    for key in keys:
        datapoint = datapoint_dict_to_numpy(dictonary[key])
        return_arr.append(datapoint)

    return return_arr


def targetFeatureSplit(data):
    """
        given a numpy array like the one returned from
        dict_to_numpy, separate out the first feature
        and put it into its own list (this should be the
        quantity you want to predict)

        return targets and features as separate lists

        (sklearn can generally handle both lists and numpy arrays as
        input formats when training/predicting)
    """

    target = []
    features = []
    for item in data:
        target.append(item[0])
        features.append(item[1:])

    return target, features
