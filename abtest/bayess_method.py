#!/usr/bin/env python  
#-*- coding:utf-8 -*-  
""" 
@file: bayess_method.py
@time: 2020-07-10 14:53
"""

import scipy.stats as stats
import pymc3 as pm

def ab_sample():
    #真实概率
    p_A=0.05
    p_B=0.04

    #用户流量
    n_user=13500
    n_A=stats.binom.rvs(n=n_user,p=0.5,size=1)[0]
    n_B= n_user - n_A

    conversions_A=stats.bernoulli.rvs(p_A,size=n_A)
    conversions_B=stats.bernoulli.rvs(p_B,size=n_B)

    print("creative A was observed {} times and led to {} conversions".format(n_A,sum(conversions_A)))
    print("creative B was observed {} times and led to {} conversions".format(n_B,sum(conversions_B)))

def bayess_method():
    p_A,p_B=0.05,0.04
    with pm.Model() as model:
        n_users=10000

        #定义随机和确定性变量（构建网络）
        #用户的数量
        n_A=pm.Binomial("n_A",n_users,0.5)
        n_B=pm.Deterministic("n_B",n_users-n_A)

        conversions_A=pm.Binomial("conversions_A",n_A,p_A)
        conversions_B=pm.Binomial("conversions_B",n_B,p_B)

        observed_conversions_A=pm.Deterministic("observerd_conversions_A",conversions_A)
        observed_conversions_B=pm.Deterministic("observerd_conversions_B",conversions_B)

        p_estimates=pm.Uniform("p_estimates",0,1,shape=2)
        delta=pm.Deterministic("delta",p_estimates[1]-p_estimates[0])

        #向网络提供观测数据
        obs_A=pm.Binomial("obs_A",n_A,p_estimates[0],observed=observed_conversions_A)
        obs_B=pm.Binomial("obs_B",n_B,p_estimates[1],observed=observed_conversions_B)

        #运行MCMC算法
        start = pm.find_MAP()
        step = pm.Metropolis()
        trace = pm.sample(100000, step=step)
        pm.traceplot(trace);


if __name__=="__main__":
    bayess_method()