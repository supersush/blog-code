#!/usr/bin/env python  
#-*- coding:utf-8 -*-  
""" 
@author:shuai.su
@file: z_exam_with_binomial_dist.py 
@time: 2020-07-09 16:44
"""

"""
计算转化率类指标Z值的代码，用于得出试验是否显著的结论
"""
import math

def z_score(p_experiment,p_control,n_experiment,n_control):
    se_experiment=p_experiment*(1-p_experiment)/n_experiment
    se_control=p_control*(1-p_control)/n_control
    z=(p_experiment-p_control)/math.sqrt(se_experiment+se_control)
    return z
