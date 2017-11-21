https://www.tensorflow.org/get_started/get_started

https://www.tensorflow.org/tutorials/audio_recognition 



* single_fc 

    ```  
  (fingerprint_input)
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
    ```
* conv 
    http://www.isca-speech.org/archive/interspeech_2015/papers/i15_1478.pdf 

    ```  
  (fingerprint_input)
          v
      [Conv2D]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
        [Relu]
          v
      [MaxPool]
          v
      [Conv2D]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
        [Relu]
          v
      [MaxPool]
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v 
    ``` 

* low_latency_conv 
    http://www.isca-speech.org/archive/interspeech_2015/papers/i15_1478.pdf 

    ``` 
  (fingerprint_input)
          v
      [Conv2D]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
        [Relu]
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
    ``` 

* low_latency_svdf 
    https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43813.pdf 

    ``` 
  (fingerprint_input)
          v
        [SVDF]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
        [Relu]
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
      [MatMul]<-(weights)
          v
      [BiasAdd]<-(bias)
          v
    ``` 
