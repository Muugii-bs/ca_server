from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os.path
import time
import json
import sys
import linear
import input_data 

from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import numpy as np


def load_configs(file_name):
    with open(file_name, 'r') as fp:
        return json.load(fp)['configs']


flags = tf.app.flags
FLAGS = flags.FLAGS

configs = load_configs(sys.argv[1])
hidden_units = configs['hidden_units']

flags.DEFINE_float('learning_rate', configs['learning_rate'], 'Initial learning rate.')
flags.DEFINE_integer('max_steps', configs['max_steps'], 'Number of steps to run trainer.')
flags.DEFINE_integer('batch_size', configs['batch_size'], 'Batch size.  '
                     'Must divide evenly into the dataset sizes.')
flags.DEFINE_string('train_dir', 'data', 'Directory to put the training data.')
flags.DEFINE_string('num_class', configs['classes'], 'The number of classes.')
flags.DEFINE_string('num_factors', configs['factors'], 'The length of input vectro.')
flags.DEFINE_string('result_dir', './result_20161123/', 'The length of input vectro.')
flags.DEFINE_string('train_result_file', configs['train_result_file'], 'Log file for result')
flags.DEFINE_string('test_result_file', configs['test_result_file'], 'Log file for result')

AVERAGE = {
        FLAGS.result_dir + FLAGS.train_result_file: { 'sum': [0.0] * 11, 'cnt':0 },
        FLAGS.result_dir + FLAGS.test_result_file: {'sum': [0.0] * 11, 'cnt': 0}
}

def placeholder_inputs(batch_size):
  # Note that the shapes of the placeholders match the shapes of the full
  # image and label tensors, except the first dimension is now batch_size
  # rather than the full size of the train or test data sets.
  metrics_placeholder = tf.placeholder(tf.float32, shape=(batch_size, FLAGS.num_factors))
  labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))
  return metrics_placeholder, labels_placeholder


def fill_feed_dict(data_set, metrics_pl, labels_pl):
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
            data_set,
            file_name):
  # And run one epoch of eval.
  true_count = 0  # Counts the number of correct predictions.
  steps_per_epoch = data_set.num_examples // FLAGS.batch_size
  num_examples = steps_per_epoch * FLAGS.batch_size
  recall_all = {}
  try:
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
      if len(recall_all) == FLAGS.num_class:
          res1 = []
          for idx in range(0, FLAGS.num_class):
              base = 0
              for a,b in recall_all.items():
                  base += b[idx] if a != idx else 0
              base = base + recall_all[idx][idx] if base + recall_all[idx][idx] > 0 else 1
              tmp  = {
                    'rec': recall_all[idx][idx]/recall_all[idx]['all'],
                    'pre': recall_all[idx][idx]/base
              }
              res1.append(tmp)
          print(num_examples, true_count, precision)
          print(recall_all)
          print(res1)
          with open(file_name, 'a') as fp:
              fp.write(str(num_examples) + '\t' +
                    str(true_count) + '\t' + 
                    str(precision) + '\t' + 
                    str(res1[0]['rec']) + '\t' + 
                    str(res1[0]['pre']) + '\t' + 
                    str(res1[1]['rec']) + '\t' + 
                    str(res1[1]['pre']) + '\t' + 
                    str(res1[2]['rec']) + '\t' + 
                    str(res1[2]['pre']) + '\t' + 
                    str(res1[3]['rec']) + '\t' + 
                    str(res1[3]['pre']) + '\t' + '\n')
          AVERAGE[file_name]['sum'][0] += num_examples
          AVERAGE[file_name]['sum'][1] += true_count
          AVERAGE[file_name]['sum'][2] += precision
          AVERAGE[file_name]['sum'][3] += res1[0]['rec']
          AVERAGE[file_name]['sum'][4] += res1[0]['pre']
          AVERAGE[file_name]['sum'][5] += res1[1]['rec']
          AVERAGE[file_name]['sum'][6] += res1[1]['pre']
          AVERAGE[file_name]['sum'][7] += res1[2]['rec']
          AVERAGE[file_name]['sum'][8] += res1[2]['pre']
          AVERAGE[file_name]['sum'][9] += res1[3]['rec']
          AVERAGE[file_name]['sum'][10] += res1[3]['pre']
          AVERAGE[file_name]['cnt']    += 1
  except Exception as e:
    print(e)

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

def run_training(hidden_units):
  # Get the sets of metrics and labels for training, validation, and
  # test on MNIST.
  data_sets = input_data.read_data_sets(FLAGS.train_dir, configs)

  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():
    # Generate placeholders for the metrics and labels.
    metrics_placeholder, labels_placeholder = placeholder_inputs(FLAGS.batch_size)

    # Build a Graph that computes predictions from the inference model.
    logits = linear.inference(metrics_placeholder,
                             hidden_units,
                             FLAGS.num_factors,
                             FLAGS.num_class)

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
      if (step + 1) % 5000 == 0 or (step + 1) == FLAGS.max_steps:
        checkpoint_file = os.path.join(FLAGS.train_dir, 'checkpoint')
        saver.save(sess, checkpoint_file, global_step=step)
        # Evaluate against the training set.
        print('Training Data Eval:')
        do_eval(sess,
                eval_correct,
                metrics_placeholder,
                labels_placeholder,
                data_sets.train,
                FLAGS.result_dir + 
                FLAGS.train_result_file)
        # Evaluate against the test set.
        print('Test Data Eval:')
        do_eval(sess,
                eval_correct,
                metrics_placeholder,
                labels_placeholder,
                data_sets.test,
                FLAGS.result_dir + 
                FLAGS.test_result_file)

def main(_):

    header = 'samples\tcorrect\tacc\tpre1\trec1\tpre2\trec2\tpre3\trec3\tpre4\trec4\n'
    with open(FLAGS.result_dir + FLAGS.test_result_file, 'w') as fp:
        fp.write(header)
    with open(FLAGS.result_dir + FLAGS.train_result_file, 'w') as fp:
        fp.write(header)

    run_training(hidden_units)
    
    with open(FLAGS.result_dir + FLAGS.test_result_file, 'a') as fp:
        fp.write("\n\n")
        fp.write("\t".join(
            [str(x) for x in np.array(AVERAGE[FLAGS.result_dir + FLAGS.test_result_file]['sum']) / 
             AVERAGE[FLAGS.result_dir + FLAGS.test_result_file]['cnt']]))
    with open(FLAGS.result_dir + FLAGS.train_result_file, 'a') as fp:
        fp.write("\n\n")
        fp.write("\t".join(
            [str(x) for x in np.array(AVERAGE[FLAGS.result_dir + FLAGS.train_result_file]['sum']) / 
             AVERAGE[FLAGS.result_dir + FLAGS.train_result_file]['cnt']]))


if __name__ == '__main__':
  tf.app.run()
