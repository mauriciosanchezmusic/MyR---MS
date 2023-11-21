import sys
from statistics import *

def media(data):
    resp = mean(data)
    return resp

def mediana(data):
    resp = median(data)
    return resp

def moda(data):
    resp = mode(data)
    return resp

def varianza(data):
    resp = variance(data)
    return resp

def desviacion_standar(data):
    resp = stdev(data)
    return resp

def regresion_lineal(vector1, vector2):
    resp = linear_regression(vector1, vector2)
    return resp
