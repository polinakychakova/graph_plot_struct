import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def create_random_matrix():
   n = random.randint(2, 20)
   P = np.random.randint(0, 30, (n, n))
   return P

def read_matrix_from_file(file_path):
   with open(file_path, 'r') as file:
       lines = file.readlines()
       matrix = []
       for line in lines:
           row = list(map(int, line.split()))
           matrix.append(row)
   return matrix