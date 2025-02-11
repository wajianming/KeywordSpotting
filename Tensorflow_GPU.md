Assume your host PC is using Ubuntu 16.04.

* Install GPU Drivers: (Assume using Nvidia CUDA infrastructure.)  
  - **Tensorflow 1.4 and below**: (CUDA 8.0) 
    1. Install **CUDA 8.0**: [LINK](https://developer.nvidia.com/cuda-80-ga2-download-archive)  

      The default link is for CUDA 9.0. You could download CUDA 8.0 GA2 thru the link.

    2. Install **cuDNN v6.0**: [LINK](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v6/prod/8.0_20170307/Ubuntu16_04_x64/libcudnn6_6.0.20-1+cuda8.0_amd64-deb)  

  - **Tensorflow 1.4 above**: (CUDA 9.0) 

    1. Install **CUDA 9.0**: [LINK](https://developer.nvidia.com/cuda-downloads) 

    2. Install **cuDNN v7.0.4**: [LINK](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.0.4/prod/9.0_20171031/Ubuntu16_04-x64/libcudnn7_7.0.4.31-1+cuda9.0_amd64) 

  - Latest release: 

    1. CUDA: 
      Use the latest version when you confirmed your Tensorflow support that. 
      [LINK](https://developer.nvidia.com/cuda-downloads) 

    2. cuDNN: 
      Make sure your are using compatible version with CUDA.
      [LINK](https://developer.nvidia.com/rdp/cudnn-download) 
        
  - Lagacy releases: 
    1. CUDA: [LINK](https://developer.nvidia.com/cuda-toolkit-archive) 
    2. cuDNN: [LINK](https://developer.nvidia.com/rdp/cudnn-download) 

* Install Tensorflow (Using VirtualEnv): 

  - **Python 2.7** 

    ``` 
            sudo apt-get install libcupti-dev
            
            sudo apt-get install python-pip python-dev python-virtualenv
            # (You may change "~/tensorflow" to any folder you preferred.)
            virtualenv --system-site-packages ~/tensorflow

            # (Switch into virtual env)
            source ~/tensorflow/bin/activate

            # Install package into virtual env.
            easy_install -U pip
            pip install --upgrade tensorflow-gpu  # for Python 2.7 and GPU
    ```

* Reference:  
  1. [Install Tensorflow](https://www.tensorflow.org/install/)  

