import pymc3 as pm
import numpy as np
import pandas as pd
from datetime import datetime

def detect_change_points(prices, n_changepoints=5):
    """
    Detect change points in the oil price series using Bayesian methods
    """
    with pm.Model() as model:
        # Priors for the mean and standard deviation of returns
        mu = pm.Normal('mu', mu=0, sigma=10, shape=n_changepoints+1)
        sigma = pm.HalfNormal('sigma', sigma=10)
        
        # Uniform prior for change point locations
        tau = pm.DiscreteUniform('tau', lower=0, upper=len(prices)-1, shape=n_changepoints)
        tau_sorted = pm.math.sort(tau)
        
        # Create a switch function to select the appropriate mean
        def create_switch_points(tau_sorted, n_changepoints):
            switch_points = []
            for i in range(n_changepoints+1):
                if i == 0:
                    condition = (np.arange(len(prices)) < tau_sorted[0])
                elif i == n_changepoints:
                    condition = (np.arange(len(prices)) >= tau_sorted[-1])
                else:
                    condition = ((np.arange(len(prices)) >= tau_sorted[i-1]) & 
                                (np.arange(len(prices)) < tau_sorted[i]))
                switch_points.append(condition)
            return switch_points
        
        switch_points = create_switch_points(tau_sorted, n_changepoints)
        
        # Mean based on current regime
        mu_current = pm.math.switch(switch_points[0], mu[0],
                                   pm.math.switch(switch_points[1], mu[1],
                                   pm.math.switch(switch_points[2], mu[2],
                                   pm.math.switch(switch_points[3], mu[3],
                                   pm.math.switch(switch_points[4], mu[4], mu[5])))))
        
        # Likelihood
        returns_obs = pm.Normal('returns_obs', mu=mu_current, sigma=sigma, 
                              observed=prices['log_return'].values)
        
        # Inference
        trace = pm.sample(2000, tune=1000, cores=2, target_accept=0.9)
    
    # Process results
    tau_samples = trace['tau']
    tau_mean = tau_samples.mean(axis=0).astype(int)
    
    change_points = []
    for i, tau in enumerate(tau_mean):
        change_date = prices['Date'].iloc[tau]
        change_points.append({
            'date': change_date.strftime('%Y-%m-%d'),
            'index': int(tau),
            'mean_before': float(np.mean(prices['Price'].iloc[:tau])),
            'mean_after': float(np.mean(prices['Price'].iloc[tau:])),
            'pct_change': float((np.mean(prices['Price'].iloc[tau:]) - np.mean(prices['Price'].iloc[:tau])) / 
                              np.mean(prices['Price'].iloc[:tau]) * 100)
        })
    
    return sorted(change_points, key=lambda x: x['index'])