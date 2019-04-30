import tensorflow as tf
from tensorflow.keras import layers
import numpy as np


# data=[]
# labels=[]

def main():
    data = np.asarray([[0,0],[0,1],[1,0],[1,1]])
    labels = np.asarray([[0],[1],[1],[0]])
    # data = np.random.random((1000, 64))
    # labels = np.random.random((1000, 1))
    model = tf.keras.Sequential()
    model.add(layers.Dense(2, activation='sigmoid',kernel_regularizer=tf.keras.regularizers.l1(0.01)))
    model.add(layers.Dense(2, activation='sigmoid',kernel_regularizer=tf.keras.regularizers.l1(0.01)))
    model.add(layers.Dense(1,activation='sigmoid'))
    print(data)
    model.compile(optimizer=tf.train.GradientDescentOptimizer(0.01),loss='mse',metrics=[tf.keras.metrics.Precision()])
    output = model.fit(data, labels, epochs=100, batch_size=2)
    print(output)

if __name__=="__main__":
    main()
