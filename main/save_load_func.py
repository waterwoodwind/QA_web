#coding=utf-8
import pandas as pd
import pickle

def list_all_data():
    file_1 = file('data_all.pkl', 'rb')
    updata = pickle.load(file_1)
    return updata