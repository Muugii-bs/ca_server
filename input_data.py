"""Functions for downloading and reading MNIST data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip

import numpy
from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes
from tensorflow.python.platform import gfile

class DataSet(object):

  def __init__(self,
               metrics,
               labels):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.
    """
    self._metrics = metrics
    self._labels = labels
    self._num_examples = metrics.shape[0]
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def metrics(self):
    return self._metrics

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def next_batch(self, batch_size):
    """Return the next `batch_size` examples from this data set."""
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    if self._index_in_epoch > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Shuffle the data
      perm = numpy.arange(self._num_examples)
      numpy.random.shuffle(perm)
      self._metrics = self._metrics[perm]
      self._labels = self._labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size
      assert batch_size <= self._num_examples
    end = self._index_in_epoch
    return self._metrics[start:end], self._labels[start:end]


def read_data_sets(train_dir):

  all_data = numpy.load(train_dir + '/dataset.npy')
  numpy.random.shuffle(all_data) 

  TRAIN_CNT = 1806
  VALIDATION_SIZE = 0#362
  train_metrics, train_labels = numpy.split(all_data[:TRAIN_CNT], [8], 1)
  train_labels                = train_labels.reshape(1, len(train_labels))[0].astype(int)
  test_metrics,  test_labels  = numpy.split(all_data[TRAIN_CNT:], [8], 1)
  test_labels                 = test_labels.reshape(1, len(test_labels))[0].astype(int)

  validation_metrics = train_metrics[:VALIDATION_SIZE]
  validation_labels = train_labels[:VALIDATION_SIZE]
  train_metrics = train_metrics[VALIDATION_SIZE:]
  train_labels = train_labels[VALIDATION_SIZE:]

  train = DataSet(train_metrics, train_labels)
  validation = DataSet(validation_metrics, validation_labels)
  test = DataSet(test_metrics, test_labels)

  return base.Datasets(train=train, validation=validation, test=test)
