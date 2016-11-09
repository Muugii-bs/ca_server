"""Trains and Evaluates the MNIST network using a feed dictionary."""
# pylint: disable=missing-docstring
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from config import configs

import os.path
import time
import linear
import input_data 

from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf


# Basic model parameters as external flags.
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_float('learning_rate', configs['learning_rate'], 'Initial learning rate.')
flags.DEFINE_integer('max_steps', configs['max_steps'], 'Number of steps to run trainer.')
flags.DEFINE_integer('hidden1', configs['hidden1'], 'Number of units in hidden layer 1.')
flags.DEFINE_integer('hidden2', configs['hidden2'], 'Number of units in hidden layer 2.')
flags.DEFINE_integer('batch_size', configs['batch_size'], 'Batch size.  '
                     'Must divide evenly into the dataset sizes.')
flags.DEFINE_string('train_dir', 'data', 'Directory to put the training data.')
flags.DEFINE_string('num_class', configs['classes'], 'The number of classes.')
flags.DEFINE_string('num_factors', configs['factors'], 'The length of input vectro.')

def placeholder_inputs(batch_size):
  """Generate placeholder variables to represent the input tensors.
  These placeholders are used as inputs by the rest of the model building
  code and will be fed from the downloaded data in the .run() loop, below.
  Args:
    batch_size: The batch size will be baked into both placeholders.
  Returns:
    metrics_placeholder: Metrics placeholder.
    labels_placeholder: Labels placeholder.
  """
  # Note that the shapes of the placeholders match the shapes of the full
  # image and label tensors, except the first dimension is now batch_size
  # rather than the full size of the train or test data sets.
  metrics_placeholder = tf.placeholder(tf.float32, shape=(batch_size, FLAGS.num_factors))
  labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))
  return metrics_placeholder, labels_placeholder


def fill_feed_dict(data_set, metrics_pl, labels_pl):
  """Fills the feed_dict for training the given step.
  A feed_dict takes the form of:
  feed_dict = {
      <placeholder>: <tensor of values to be passed for placeholder>,
      ....
  }
  Args:
    data_set: The set of metircs and labels, from input_data.read_data_sets()
    metrics_pl: The metrics placeholder, from placeholder_inputs().
    labels_pl: The labels placeholder, from placeholder_inputs().
  Returns:
    feed_dict: The feed dictionary mapping from placeholders to values.
  """
  # Create the feed_dict for the placeholders filled with the next
  # `batch size` examples.
  metrics_feed, labels_feed = data_set.next_batch(FLAGS.batch_size)
  feed_dict = {
      metrics_pl: metrics_feed,
      labels_pl: labels_feed,
  }
  return feed_dict


def do_eval(sess,
            eval_correct,
            metrics_placeholder,
            labels_placeholder,
            data_set):
  """Runs one evaluation against the full epoch of data.
  Args:
    sess: The session in which the model has been trained.
    eval_correct: The Tensor that returns the number of correct predictions.
    metrics_placeholder: The metrics placeholder.
    labels_placeholder: The labels placeholder.
    data_set: The set of metrics and labels to evaluate, from
      input_data.read_data_sets().
  """
  # And run one epoch of eval.
  true_count = 0  # Counts the number of correct predictions.
  steps_per_epoch = data_set.num_examples // FLAGS.batch_size
  num_examples = steps_per_epoch * FLAGS.batch_size
  recall_all = {}
  for step in xrange(steps_per_epoch):
    feed_dict = fill_feed_dict(data_set,
                               metrics_placeholder,
                               labels_placeholder)
    res = sess.run(eval_correct, feed_dict=feed_dict)
    #true_count += sess.run(eval_correct, feed_dict=feed_dict)
    tmp = recall(res[1].reshape(1, len(res[1]))[0], res[2])
    for i in range(0,FLAGS.num_class):
       if not i in recall_all: recall_all[i] = {}
       for j in range(0,FLAGS.num_class):
           if not j in recall_all[i]: recall_all[i][j] = 0
           if not 'all' in recall_all[i]: recall_all[i]['all'] = 0
           recall_all[i][j] += tmp[i][j]
       recall_all[i]['all'] += tmp[i]['all']
    true_count += res[0]
  precision = true_count / num_examples
  print('  Num examples: %d  Num correct: %d  Precision @ 1: %0.04f' %
        (num_examples, true_count, precision))
  print(' Recall: ', recall_all)

def recall(y, label):
    res = {}
    for i,v in enumerate(label):
        if not v in res: 
            t = {'all':0,}
            for j in range(0,FLAGS.num_class):
                t[j] = 0
            res[v] = t
        res[v][y[i]]  += 1 
        res[v]['all'] += 1
    return res

def run_training():
  """Train METRICS for a number of steps."""
  # Get the sets of metrics and labels for training, validation, and
  # test on MNIST.
  data_sets = input_data.read_data_sets(FLAGS.train_dir)

  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():
    # Generate placeholders for the metrics and labels.
    metrics_placeholder, labels_placeholder = placeholder_inputs(FLAGS.batch_size)

    # Build a Graph that computes predictions from the inference model.
    logits = linear.inference(metrics_placeholder,
                             FLAGS.hidden1,
                             FLAGS.hidden2)

    # Add to the Graph the Ops for loss calculation.
    loss = linear.loss(logits, labels_placeholder)

    # Add to the Graph the Ops that calculate and apply gradients.
    train_op = linear.training(loss, FLAGS.learning_rate)

    # Add the Op to compare the logits to the labels during evaluation.
    eval_correct = linear.evaluation(logits, labels_placeholder)

    # Build the summary operation based on the TF collection of Summaries.
    summary_op = tf.merge_all_summaries()

    # Add the variable initializer Op.
    init = tf.initialize_all_variables()

    # Create a saver for writing training checkpoints.
    saver = tf.train.Saver()

    # Create a session for running Ops on the Graph.
    sess = tf.Session()

    # Instantiate a SummaryWriter to output summaries and the Graph.
    summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph)

    # And then after everything is built:

    # Run the Op to initialize the variables.
    sess.run(init)

    # Start the training loop.
    for step in xrange(FLAGS.max_steps):
      start_time = time.time()

      # Fill a feed dictionary with the actual set of metrics and labels
      # for this particular training step.
      feed_dict = fill_feed_dict(data_sets.train,
                                 metrics_placeholder,
                                 labels_placeholder)

      # Run one step of the model.  The return values are the activations
      # from the `train_op` (which is discarded) and the `loss` Op.  To
      # inspect the values of your Ops or variables, you may include them
      # in the list passed to sess.run() and the value tensors will be
      # returned in the tuple from the call.
      _, loss_value = sess.run([train_op, loss], feed_dict=feed_dict)

      duration = time.time() - start_time

      # Write the summaries and print an overview fairly often.
      if step % 100 == 0:
        # Print status to stdout.
        print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
        # Update the events file.
        summary_str = sess.run(summary_op, feed_dict=feed_dict)
        summary_writer.add_summary(summary_str, step)
        summary_writer.flush()

      # Save a checkpoint and evaluate the model periodically.
      if (step + 1) % 1000 == 0 or (step + 1) == FLAGS.max_steps:
        checkpoint_file = os.path.join(FLAGS.train_dir, 'checkpoint')
        saver.save(sess, checkpoint_file, global_step=step)
        # Evaluate against the training set.
        print('Training Data Eval:')
        do_eval(sess,
                eval_correct,
                metrics_placeholder,
                labels_placeholder,
                data_sets.train)
        # Evaluate against the validation set.
        """
        print('Validation Data Eval:')
        do_eval(sess,
                eval_correct,
                metrics_placeholder,
                labels_placeholder,
                data_sets.validation)
        """
        # Evaluate against the test set.
        print('Test Data Eval:')
        do_eval(sess,
                eval_correct,
                metrics_placeholder,
                labels_placeholder,
                data_sets.test)

def main(_):
  run_training()


if __name__ == '__main__':
  tf.app.run()
