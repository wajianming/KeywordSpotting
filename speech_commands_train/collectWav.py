import os

import json
import csv
csv_report = '/home/home/tf/KeywordSpotting/speech_commands_train/conv_18000_graph/conv.ckpg-18000.pb.analysis.csv'
orgainized_wav = '/tmp/kaggle_test/'


def readCSV(csv_report_file = None):
  reader = None
  with open(csv_report_file) as csvfile:
    print('opened')
    reader = csv.DictReader(csvfile)

    for row in reader:
      sorted_label = row['sorted_label']
      labels = json.loads(sorted_label)
      top1_score = labels[0]
      for label_name, label_score in top1_score.iteritems():
        score_class = 'Unknown'
        if label_score > 0.8:
          score_class = '100_80'
        elif label_score > 0.6: 
          score_class = '80_60'
        elif label_score > 0.4: 
          score_class = '60_40'
        elif label_score > 0.2: 
          score_class = '40_20'
        else:
          score_class = '20_00'

        target_wav_dir = '%s/%s/%s/' % (orgainized_wav, score_class, label_name) 

        if not os.path.exists(target_wav_dir):
          os.makedirs(target_wav_dir)

        src_file = '%s/%s' % (row['fpath'], row['fname'])
        dst_file = '%s/%s' % (target_wav_dir, row['fname'])
        os.symlink(src_file, dst_file)

        save_file_list = '%s/file_list.txt' % (target_wav_dir)
        with open(save_file_list, "a") as myfile:
          myfile.write('%s/%s\n' % (label_name, row['fname']))



readCSV(csv_report)
