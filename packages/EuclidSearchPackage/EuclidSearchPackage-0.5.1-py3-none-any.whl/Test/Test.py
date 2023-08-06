# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 11:43
# @Author  : Euclid-Jie
# @File    : Test.py

# ----------0 import package
import pandas as pd
import src.EuclidSearchPackage as ESP

# ----------1 Weibo search demo
# ESP.Set_cookie('cookie.txt')
# res = ESP.Get_single_weibo_data(mblogid='MrOtA75Fd')
# print(res)

# ----------2 Mongo client
# _COL = ESP.MongoClient('Test', 'Test')
# _COL.insert_one({"Test": "Test"})

# ----------3 csv client
# _COL = ESP.CsvClient('Test', 'Test')
# _COL.insert_one({"Test": "Test"})

# ----------4 save df to csv
# df = pd.DataFrame({"Test": ["Test"]}, index=[0])
# ESP.EuclidCsvTools.writeDf2Csv(df, 'test.csv')
