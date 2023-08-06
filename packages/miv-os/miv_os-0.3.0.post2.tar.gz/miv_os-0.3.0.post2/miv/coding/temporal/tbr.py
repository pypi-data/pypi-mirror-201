class ThresholdBasedRepresentation:
    """
    Threshold Based Representation encoding [1]_

    .. [1] Delbruck, T., & Lichtsteiner, P. (2007, May). Fast sensory motor control based on event-based hybrid neuromorphic-procedural system. In 2007 IEEE International Symposium on Circuits and Systems (pp. 845-848). IEEE.

    """

    def __init__(self, data, threshold=0.5):
        """
        :param numpy.ndarray data:
            See :py:mod: nucube.utils.ReadCSV
        :param float threshold:
            Threshold to cut off spike detection.
        """

        super().__init__()
        self.data = data
        self.threshold = threshold

    def get_spikes(self):
        """Returns TBR spikes.

        :rtype: numpy.ndarray
        :return: spikes

        >>> spikes = TBR()
        >>> spikes.get_spikes()
            [[[0 0 0 ..., 0 0 0]
            [1 1 1 ..., 1 1 1]
            [0 0 1 ..., 1 0 1]
            ...,
            [0 0 0 ..., 1 0 0]
            [0 0 0 ..., 0 0 1]
            [0 0 0 ..., 0 0 0]]
            |
            [[0 0 0 ..., 0 0 0]
            [0 0 0 ..., 0 0 0]
            [0 1 0 ..., 0 1 1]
            ...,
            [0 0 0 ..., 0 0 0]
            [0 0 0 ..., 0 0 1]
            [1 0 1 ..., 0 0 1]]]

        """

        sample_feature_threshold = self._get_threshold()
        row_diff = self._get_training_element_difference()

        spikes = []
        for idx, sample in enumerate(row_diff):
            spikes.append(
                np.where(
                    np.greater(sample, sample_feature_threshold[idx]),
                    1,
                    np.where(np.less(sample, -sample_feature_threshold[idx]), -1, 0),
                )
            )

        # np.array([np.sign(sample_feature_threshold[i] - a) for i, a in enumerate(row_diff)])  # Possible answer

        return np.asarray(spikes, dtype=np.int8)

    def get_spike_time(self, offset=100):
        """
        Merges the samples and returns the time at which the spike happens. Spike time always startes with ``1`` and
        increases with :param: offset.

        :param int offset:
            Shifting the spike index to the given number, if the first index is ``0``, then it will always be ``1``
        :rtype: list
        :return: Spike time with an offset.
        """

        reshaped_raw_spikes = np.vstack(self.get_spikes())

        spike_times = []

        for _feature in reshaped_raw_spikes.T:
            _idx_of_ones = np.squeeze(np.add(np.where(_feature == 1), 1))
            if _idx_of_ones[0] == 1:
                spike_times.append(
                    np.insert(np.multiply(_idx_of_ones[1:], offset), 0, 1).tolist()
                )
            else:
                spike_times.append(np.multiply(_idx_of_ones, offset).tolist())

        return spike_times

    def _get_training_element_difference(self):
        """Returns row-by-row difference for each sample.

        :rtype: numpy.ndarray
        :return: row_diff
        """

        train_data = self.data

        row_diff = []
        for index in range(train_data.shape[0]):
            row_diff.append(np.diff(train_data[index], axis=0))

        return np.asarray(row_diff)

    def _get_mean_sd_sample(self):
        """Returns mean and standard deviation of absolute data.

        :rtype: (numpy.ndarray, numpy.ndarray)
        :return: mean, sd
        """

        diff_data = self._get_training_element_difference()
        abs_data = np.abs(diff_data)
        abs_data_shape_range = range(abs_data.shape[0])

        mean = []
        sd = []
        for index in abs_data_shape_range:
            mean.append(np.mean(abs_data[index], axis=0))

        for index in abs_data_shape_range:
            sd.append(np.std(abs_data[index], axis=0))

        return np.asarray(mean), np.asarray(sd)

    def _get_threshold(self):
        """Returns threshold values for each feature of every sample.

        :rtype: ndarray
        :return: threshold
        """

        mean, sd = self._get_mean_sd_sample()

        return np.add(mean, np.multiply(sd, self.threshold))
