# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Runs a trained audio graph against a WAVE file and reports the results.

The model, labels and .wav file specified in the arguments will be loaded, and
then the predictions from running the model against the audio data will be
printed to the console. This is a useful script for sanity checking trained
models, and as an example of how to use an audio model from Python.

Here's an example of running it:

python tensorflow/examples/speech_commands/label_wav.py \
--graph=/tmp/my_frozen_graph.pb \
--labels=/tmp/speech_commands_train/conv_labels.txt \
--wav=/tmp/speech_dataset/left/a5d485dc_nohash_0.wav

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

import json

import csv
import logging
logging.basicConfig(level=logging.DEBUG)
from os import walk


import time

import tensorflow as tf

# pylint: disable=unused-import
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
# pylint: enable=unused-import

FLAGS = None

class PrettyFloat(float):
    def __repr__(self):
        return '%.4f' % self

def pretty_floats(obj):
    if isinstance(obj, float):
        return PrettyFloat(obj)
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_floats, obj)             
    return obj

def load_graph(filename):
  """Unpersists graph from file as default graph."""
  with tf.gfile.FastGFile(filename, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


def load_labels(filename):
  """Read in labels, one label per line."""
  return [line.rstrip() for line in tf.gfile.GFile(filename)]


def run_graph(wav_data, labels, input_layer_name, output_layer_name,
              num_top_predictions):
  """Runs the audio data through the graph and prints predictions."""
    

  ts = time.time()
  with tf.Session() as sess:
    logging.debug('tf.Session(): %s', (time.time() - ts))
    ts = time.time()
    with open('%s.%s.csv' % (FLAGS.graph, FLAGS.csv) , 'w') as csvfile:
      fieldnames = ['fname', 'label']
      kaggle_labels = []
      for index, label in enumerate(labels):
        if label == '_unknown_':
          label = 'unknown'
        elif label == '_silence_':
          label = 'silence'
        kaggle_labels.append(label)
      print( kaggle_labels)


      if FLAGS.csv == "analysis":
        num_top_predictions = len(labels)
        #fieldnames = fieldnames + labels
        fieldnames.append('fpath')
        fieldnames.append('sorted_label')
      csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      csv_writer.writeheader()

      for (dirpath, dirnames, filenames) in walk(wav_data):
        for f in filenames:
          if f.split(".")[-1] != "wav":
            continue

          csv_raw = {'fname': f}

          wav_fullpath = '%s%s' % (dirpath,f)
          logging.debug('process %s', wav_fullpath)
          ts = time.time()
          with open( wav_fullpath, 'rb') as wav_file:
            wav_data = wav_file.read()
          logging.debug('read wav: %s', (time.time() - ts))
          # Feed the audio data as input to the graph.
          #   predictions  will contain a two-dimensional array, where one
          #   dimension represents the input image count, and the other has
          #   predictions per class
          softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
          ts = time.time()
          predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})
          logging.debug('sess.run(..): %s', (time.time() - ts))

          # Sort to show labels in order of confidence
          top_k = predictions.argsort()[-num_top_predictions:][::-1]
          if len(top_k) > 0:
            highest_score_id = top_k[0]
            if FLAGS.csv == 'kaggle':
              csv_raw['label'] = kaggle_labels[highest_score_id]
            elif FLAGS.csv == 'analysis':
              csv_raw['label'] = labels[highest_score_id]

          sorted_label = []
          for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            if FLAGS.csv == 'analysis':
              #csv_raw[human_string] = score
              csv_raw['fpath'] = dirpath
              sorted_label.append({human_string: float(score)})
            print('%s (score = %.5f)' % (human_string, score))

          if FLAGS.csv == 'analysis':
            csv_raw['sorted_label'] = json.dumps(pretty_floats(sorted_label))
          csv_writer.writerow(csv_raw)

    return 0


def label_wav(wav, labels, graph, input_name, output_name, how_many_labels):
  """Loads the model and labels, and runs the inference to print predictions."""
  if not wav or not tf.gfile.Exists(wav):
    tf.logging.fatal('Audio file does not exist %s', wav)

  if not labels or not tf.gfile.Exists(labels):
    tf.logging.fatal('Labels file does not exist %s', labels)

  if not graph or not tf.gfile.Exists(graph):
    tf.logging.fatal('Graph file does not exist %s', graph)

  labels_list = load_labels(labels)

  # load graph, which is stored in the default session
  ts = time.time()
  load_graph(graph)
  logging.debug('load_graph: %s', (time.time() - ts))

  wav_data=wav

  ts = time.time()
  run_graph(wav_data, labels_list, input_name, output_name, how_many_labels)
  logging.debug('run_graph: %s', (time.time() - ts))


def main(_):
  """Entry point for script, converts flags to arguments."""
  label_wav(FLAGS.wav, FLAGS.labels, FLAGS.graph, FLAGS.input_name,
            FLAGS.output_name, FLAGS.how_many_labels)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--wav', type=str, default='', help='Audio file to be identified.')
  parser.add_argument(
      '--graph', type=str, default='', help='Model to use for identification.')
  parser.add_argument(
      '--labels', type=str, default='', help='Path to file containing labels.')
  parser.add_argument(
      '--input_name',
      type=str,
      default='wav_data:0',
      help='Name of WAVE data input node in model.')
  parser.add_argument(
      '--output_name',
      type=str,
      default='labels_softmax:0',
      help='Name of node outputting a prediction in the model.')
  parser.add_argument(
      '--how_many_labels',
      type=int,
      default=3,
      help='Number of results to show.')

  parser.add_argument(
      '--csv', type=str, default='kaggle', help='output type.')

  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
