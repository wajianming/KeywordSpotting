* Goal:  
  1. Implement a tool that can collect GPU loading, power usage and timestamp to a CSV file.  
  2. Combine with stastic data of model training and testing, it might be help for the measurement of efficiency to the model.  

* Sample Command:  

  ```
    nvidia-smi --format=csv --query-gpu=power.draw,utilization.gpu,fan.speed,temperature.gpu
  ```
