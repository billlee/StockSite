# Documentation on Neural Network

To access necessary tools to run the neural network for stock predicting add the following to your header
```python
import nn
```
Make sure to have the following python packages installed 
```console
foo@bar:~$ pip3 install tensorflow
foo@bar:~$ pip3 install numpy
foo@bar:~$ pip3 install matplotlib
```
To start predicting, one must create a LongTermPredictor() object
```python
predictor = nn.LongTermPredictor(data)
```
The paramters to a LongTermPredictor(data), where 
data: array_like 
Define data such that each row is a data sample 

