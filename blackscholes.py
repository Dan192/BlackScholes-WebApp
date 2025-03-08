import numpy as np
import pandas as pd
import streamlit as st
import matplotlib as plt
import seaborn as sns
from scipy.stats import norm

class BlackScholes:
    def __init__(self, 
                 stock_price: float, 
                 exercise_price: float, 
                 risk_free_rate: float, 
                 time: float, 
                 volatility: float):
        self.stock_price = stock_price
        self.exercise_price = exercise_price
        self.risk_free_rate = risk_free_rate
        self.time = time
        self.volatility = volatility

    def d1(self) -> float:
        numerator: float = np.log(self.stock_price / self.exercise_price) + (self.risk_free_rate + (self.volatility ** 2) / 2) * self.time
        denominator: float = self.volatility * np.sqrt(self.time)
        return numerator / denominator

    def d2(self) -> float:
        return self.d1() - self.volatility * np.sqrt(self.time)

    def call_price(self) -> float:
        d1: float = self.d1()
        d2: float = self.d2()
        return (norm.cdf(d1) * self.stock_price) - (norm.cdf(d2) * self.exercise_price * np.exp(-self.risk_free_rate * self.time))

    def put_price(self) -> float:
        d1: float = self.d1()
        d2: float = self.d2()
        return (norm.cdf(-d2) * self.exercise_price * np.exp(-self.risk_free_rate * self.time)) - (norm.cdf(-d1) * self.stock_price)

    def delta(self, option_type: str) -> float:
        d1: float = self.d1()
        if option_type == 'call':
            return norm.cdf(d1)
        elif option_type == 'put':
            return norm.cdf(d1) - 1
        else:
            raise ValueError("Invalid option type. Please choose 'call' or 'put'.")

    def gamma(self) -> float:
        d1: float = self.d1()
        return norm.pdf(d1) / (self.stock_price * self.volatility * np.sqrt(self.time))

    def theta(self, option_type: str) -> float:
        d1: float = self.d1()
        d2: float = self.d2()
        term1: float = -(self.stock_price * norm.pdf(d1) * self.volatility) / (2 * np.sqrt(self.time))
        if option_type == 'call':
            return term1 - (self.risk_free_rate * self.exercise_price * np.exp(-self.risk_free_rate * self.time) * norm.cdf(d2))
        elif option_type == 'put':
            return term1 + (self.risk_free_rate * self.exercise_price * np.exp(-self.risk_free_rate * self.time) * norm.cdf(-d2))
        else:
            raise ValueError("Invalid option type. Please choose 'call' or 'put'.")

    def rho(self, option_type: str) -> float:
        d2: float = self.d2()
        if option_type == 'call':
            return self.exercise_price * self.time * np.exp(-self.risk_free_rate * self.time) * norm.cdf(d2) * 0.01
        elif option_type == 'put':
            return -self.exercise_price * self.time * np.exp(-self.risk_free_rate * self.time) * norm.cdf(-d2) * 0.01
        else:
            raise ValueError("Invalid option type. Please choose 'call' or 'put'.")

    def vega(self) -> float:
        d1: float = self.d1()
        return (self.stock_price * norm.pdf(d1) * np.sqrt(self.time)) * 0.01