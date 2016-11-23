from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import tensorflow as tf

def inference(metrics, hidden_units, NUM_METRICS, NUM_CLASSES):
  # Hidden 1
  with tf.name_scope('hidden1'):
    weights = tf.Variable(
        tf.truncated_normal([NUM_METRICS, hidden_units[0]], stddev=1.0 / math.sqrt(float(NUM_METRICS))), name='weights')
    biases = tf.Variable(tf.zeros([hidden_units[0]]), name='biases')
    hidden = tf.nn.relu(tf.matmul(metrics, weights) + biases)

  # Hidden layers
  for num,size in enumerate(hidden_units[1:], 1):
      with tf.name_scope('hidden%s' % str(num)):
        weights = tf.Variable(
            tf.truncated_normal([hidden_units[num-1], hidden_units[num]], stddev=1.0 / math.sqrt(float(hidden_units[num-1]))), name='weights')
        biases = tf.Variable(tf.zeros([hidden_units[num]]), name='biases')
        hidden = tf.nn.relu(tf.matmul(hidden, weights) + biases)

  # Linear
  with tf.name_scope('softmax_linear'):
    weights = tf.Variable(
        tf.truncated_normal([hidden_units[-1], NUM_CLASSES], stddev=1.0 / math.sqrt(float(hidden_units[-1]))), name='weights')
    biases = tf.Variable(tf.zeros([NUM_CLASSES]), name='biases')
    logits = tf.matmul(hidden, weights) + biases
  return logits


def loss(logits, labels):
  labels = tf.to_int64(labels)
  cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits, labels, name='xentropy')
  loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
  return loss


def training(loss, learning_rate):
  # Add a scalar summary for the snapshot loss.
  tf.scalar_summary(loss.op.name, loss)
  # Create the gradient descent optimizer with the given learning rate.
  optimizer = tf.train.GradientDescentOptimizer(learning_rate)
  # Create a variable to track the global step.
  global_step = tf.Variable(0, name='global_step', trainable=False)
  # Use the optimizer to apply the gradients that minimize the loss
  # (and also increment the global step counter) as a single training step.
  train_op = optimizer.minimize(loss, global_step=global_step)
  return train_op


def evaluation(logits, labels):
  # For a classifier model, we can use the in_top_k Op.
  # It returns a bool tensor with shape [batch_size] that is true for
  # the examples where the label is in the top k (here k=1)
  # of all logits for that example.
  correct = tf.nn.in_top_k(logits, labels, 1)
  # Return the number of true entries.
  return tf.reduce_sum(tf.cast(correct, tf.int32)), tf.nn.top_k(logits, 1).indices, labels