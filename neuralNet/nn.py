import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

class LongTermPredictor:
    def __init__(self, data):
        '''
        Our model is a sequential model, data should be a numpy array
        with each row being a datapoint, input_dim matches dimension of each sample
        # of rows is the amount of samples (column length)
        '''
        self.model = tf.keras.Sequential()
        # Input Layer
        self.model.add(layers.Dense(128, kernel_initializer='normal',input_dim=data.shape[1], activation='relu'))

        # Hidden Layers
        self.model.add(layers.Dense(256, kernel_initializer='normal',activation='relu'))
        self.model.add(layers.Dense(256, kernel_initializer='normal',activation='relu'))
        self.model.add(layers.Dense(256, kernel_initializer='normal',activation='relu'))
        # self.model.add(layers.Dense(256, kernel_initializer='normal',activation='relu'))

        # Output Layer
        self.model.add(layers.Dense(1, kernel_initializer='normal',activation='linear'))

        # Compile model
        self.model.compile(optimizer=tf.train.GradientDescentOptimizer(0.1),loss='mse',metrics=['mean_absolute_error'])

    def __str__(self):
        self.model.summary()
        return ""


    def trainModel(self, data, labels):
        '''
        trainModel(data, labels) trains the model with requisite data and labels
        batch size is predetermined by the number of datapoints

        '''
        self.model.fit(data, labels, epochs=1000, batch_size=2*data.shape[1])

    def predictPoint(self, test):
        '''
        returns the values at test array
        '''
        return self.model.predict(test)




def main():
    data = np.asarray([[0,0],[0,1],[1,0],[1,1]])
    test = np.asarray([[0,0],[0,1],[1,1]])
    labels = np.asarray([[0],[1],[1],[0]])
    # data = np.random.random((1000, 64))
    # labels = np.random.random((1000, 1))
    predic = LongTermPredictor(data)
    print(predic)
    # print(predic)
    # predic.trainModel(data,labels)
    # print(predic.predictPoint(test))
    # output = predic.model.fit(data, labels, epochs=2000, batch_size=4)

if __name__=="__main__":
    main()
