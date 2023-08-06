"""
Functions to load and epoch BIDS data
=====================================================


Copyright 2023, Max van den Boom (Multimodal Neuroimaging Lab, Mayo Clinic, Rochester MN)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def load_data_epochs(data_path, retrieve_channels, onsets,
                     trial_epoch=(-1, 3), baseline_norm=None, baseline_epoch=(-1, -0.1),
                     out_of_bound_handling='error',
                     high_pass=False, early_reref=None, line_noise_removal=None, late_reref=None, preproc_priority='mem'):
    """
    Load and epoch the data into a matrix based on channels, the trial onsets and the epoch range (relative to the onsets)

    Args:
        data_path (str):                    Path to the data file or folder
        retrieve_channels (list or tuple):  The channels (by name) of which the data should be retrieved, the output will
                                            be sorted accordingly according to this input argument.
        onsets (1d list or tuple):          The onsets of the trials around which to epoch the data
        trial_epoch (tuple):                The time-span that will be considered as the signal belonging to a single trial.
                                            Expressed as a tuple with the start- and end-point in seconds relative to
                                            the onset of the trial (e.g. the standard tuple of '-1, 3' will extract
                                            the signal in the period from 1s before the trial onset to 3s after trial onset).
        baseline_norm (None or str):        Baseline normalization setting [None, 'Mean' or 'Median']. If other than None,
                                            normalizes each trial epoch by subtracting the mean or median of part of the
                                            trial (the epoch of the trial indicated in baseline_epoch)
        baseline_epoch (tuple):             The time-span on which the baseline is calculated, expressed as a tuple with the
                                            start- and end-point in seconds relative to the trial onset (e.g. the
                                            standard tuple of '-1, -.1' will use the period from 1s before trial onset
                                            to 100ms before trial onset to calculate the baseline on); this argument
                                            is only used when baseline_norm is set to mean or median
        out_of_bound_handling (str):        Configure the handling of out-of-bound trial epochs;
                                                'error': (default) Throw an error and return when any epoch is out of bound;
                                                'first_last_only': Allows only the first trial epoch to start before the
                                                                   data-set and the last trial epoch to end beyond the
                                                                   length of the data-set, the trial epochs will be padded
                                                                   with NaN values. Note that the first and last trial are
                                                                   determined by the first and last entry in the 'onsets'
                                                                   parameter, which is not sorted by this function;
                                                'allow':           Allow trial epochs to be out-of-bound, NaNs values will
                                                                   be used for part of, or the entire, the trial epoch
        preproc_priority (str):             Set the preprocessing priority, can be set to either 'mem' (default) or 'speed'

    Returns:
        sampling_rate (int or double):      the sampling rate at which the data was acquired
        data (ndarray):                     A three-dimensional array with data epochs per channel (format: channel x
                                            trials/epochs x time); or None when an error occurs

    Note: this function's input arguments are in seconds relative to the trial onsets because the sample rate will
          only be known till after we read the data
    """
    pass




def load_data_epochs_averages(data_path, retrieve_channels, conditions_onsets,
                              trial_epoch=(-1, 3), baseline_norm=None, baseline_epoch=(-1, -0.1),
                              out_of_bound_handling='error', metric_callbacks=None,
                              high_pass=False, early_reref=None, line_noise_removal=None, late_reref=None, preproc_priority='mem'):


    """
    Load, epoch and return the average for each channel and condition (i.e. the signal in time averaged
    over all trials that belong to the same condition).

    Note: Because this function only has to return the average signal for each channel and condition, it is much more
          memory efficient (this is particularly important when the amount of memory is limited by a Docker or VM)
    Note 2: For the same reason, metric callbacks are implemented here, so while loading, but before averaging, metrics
            can be calculated on subsets of data with minimum memory usage. If memory is not an issue,
            load_data_epochs function can be used to retrieve the full dataset first and then perform calculations.

    Args:
        data_path (str):                      Path to the data file or folder
        retrieve_channels (list or tuple):    The channels (by name) of which the data should be retrieved, the output
                                              will be sorted accordingly
        conditions_onsets (2d list or tuple): A two-dimensional list to indicate the conditions, and the onsets
                                              of the trials that belong to each condition.
                                              (format: conditions x condition onsets)
        trial_epoch (tuple):                  The time-span that will be considered as the signal belonging to a single
                                              trial. Expressed as a tuple with the start- and end-point in seconds
                                              relative to onset of the trial (e.g. the standard tuple of '-1, 3' will
                                              extract the signal in the period from 1s before the trial onset to 3s
                                              after the trial onset).
        baseline_norm (None or str):          Baseline normalization setting [None, 'Mean' or 'Median']. If other
                                              than None, normalizes each trial epoch by subtracting the mean or median
                                              of part of the trial (the epoch of the trial indicated in baseline_epoch)
        baseline_epoch (tuple):               The time-span on which the baseline is calculated, expressed as a tuple with
                                              the start- and end-point in seconds relative to the trial onset (e.g. the
                                              standard tuple of '-1, -.1' will use the period from 1s before the trial
                                              onset to 100ms before the trial onset to calculate the baseline on);
                                              this argument is only used when baseline_norm is set to mean or median
        out_of_bound_handling (str):          Configure the handling of out-of-bound trial epochs;
                                                'error': (default) Throw an error and return when any epoch is out of bound;
                                                'first_last_only': Allows only the first trial epoch to start before the
                                                                   data-set and the last trial epoch to end beyond the
                                                                   length of the data-set, the trial epochs will be padded
                                                                   with NaN values. Note that the first and last trial are
                                                                   determined by the first and last entry in the 'onsets'
                                                                   parameter, which is not sorted by this function;
                                                'allow':           Allow trial epochs to be out-of-bound, NaNs values will
                                                                   be used for part of, or the entire, the trial epoch
        metric_callbacks (func or tuple):     Function or tuple of functions that are called to calculate metrics based
                                              on subsets of the un-averaged data. The function(s) are called per
                                              with the following input arguments:
                                                sampling_rate -    The sampling rate of the data
                                                data -             A subset of the data in a 2d array: trials x samples
                                                baseline -         The corresponding baseline values for the trials
                                              If callbacks are defined, a third variable is returned that holds the
                                              return values of the metric callbacks in the format: channel x condition x metric
        preproc_priority (str):              Set the preprocessing priority, can be set to either 'mem' (default) or 'speed'

    Returns:
        sampling_rate (int or double):        The sampling rate at which the data was acquired
        data (ndarray):                       A three-dimensional array with signal averages per channel and condition
                                              (format: channel x condition x samples); or None when an error occurs
        metrics (ndarray):                    If metric callbacks are specified, will return a three-dimensional array
                                              with the metric callback results (format: channel x condition x metric),
                                              else wise None

    Note: this function input arguments are in seconds relative to trial onsets because the sample rate will
          only be known till after we read the data
    """
    pass

