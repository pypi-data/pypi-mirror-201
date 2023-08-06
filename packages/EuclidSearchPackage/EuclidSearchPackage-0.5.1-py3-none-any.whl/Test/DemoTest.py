# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 16:39
# @Author  : Euclid-Jie
# @File    : DemoTest.py
import src.EuclidSearchPackage as ESP
ESP.Set_cookie('cookie.txt')
ESP.WeiboClassV3('量化实习', Mongo=False).main('2023-03-01-00', '2023-03-27-21')
