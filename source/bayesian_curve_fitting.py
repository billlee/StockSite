# written by: Huafeng Fan
# assisted by: Anton Maliev
# debugged by: Bill Lee
import numpy as np
import csv

def bayesian_fit(x, x_vec, t_vec, M = 5, alpha = 10, beta = 10):
    """ Returns the mean and variance of the normal distribution corresponding to p(t|x, x_vec, t_vec) """
    def phi(val):
        result = np.array([val**i for i in range(M + 1)])
        return result[:, np.newaxis]
    def S_matrix():
        S_inv = alpha * np.identity(M + 1) + beta * sum([ phi(x_vec[n]) @ phi(x).T for n in range(len(x_vec)) ])
        return np.linalg.inv(S_inv)
    S = S_matrix()
    def mean():
        return beta * phi(x).T @ S @ sum([ phi(x_vec[n]) * t_vec[n] for n in range(len(x_vec)) ])
    def variance():
        return 1/beta * phi(x).T @ S @ phi(x)
    return mean()[0, 0], variance()[0, 0]
