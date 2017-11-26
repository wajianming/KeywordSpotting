* Inference:  

  ```  
python label_wav.py 	--graph=/home/home/tf/KeywordSpotting/speech_commands_train/conv_18000_graph/conv.ckpg-18000.pb --labels=conv_labels.txt --wav=/home/home/test/audio/
  ```

  ```
python label_wav.py 	--graph=/home/home/tf/KeywordSpotting/speech_commands_train/conv_18000_graph/conv.ckpg-18000.pb \
			--labels=conv_labels.txt \
			--wav=/home/home/test/audio/ \
			--csv=analysis
  ```
