"""
Package Import
"""
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quantstats as qs
import gurobipy as gp
import warnings
import argparse

"""
Project Setup
"""
warnings.simplefilter(action="ignore", category=FutureWarning)

assets = [
    "SPY",
    "XLB",
    "XLC",
    "XLE",
    "XLF",
    "XLI",
    "XLK",
    "XLP",
    "XLRE",
    "XLU",
    "XLV",
    "XLY",
]
data = pd.DataFrame()

# Fetch the data for each stock and concatenate it to the `data` DataFrame
for asset in assets:
    raw = yf.download(asset, start="2012-01-01", end="2024-04-01")
    raw["Symbol"] = asset
    data = pd.concat([data, raw], axis=0)

# Initialize df and df_returns
Bdf = portfolio_data = data.pivot_table(
    index="Date", columns="Symbol", values="Adj Close"
)
df = Bdf.loc["2019-01-01":"2024-04-01"]

"""
Strategy Creation

Create your own strategy, you can add parameter but please remain "price" and "exclude" unchanged
"""


def mv_opt(R_n, gamma):
    Sigma = R_n.cov().values
    mu = R_n.mean().values
    n = len(R_n.columns)

    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.setParam("DualReductions", 0)
        env.start()
        with gp.Model(env=env, name="portfolio") as model:
            # long only
            w = model.addMVar(n, name="w", lb=0, ub=1)

            exp_return = w @ mu
            variance = (w @ Sigma) @ w

            model.setObjective(exp_return - gamma / 2 * variance, gp.GRB.MAXIMIZE)
            constr = model.addConstr(w @ np.ones(n) == 1, name="constr")
            model.optimize()

            # Check if the status is INF_OR_UNBD (code 4)
            if model.status == gp.GRB.INF_OR_UNBD:
                print(
                    "Model status is INF_OR_UNBD. Reoptimizing with DualReductions set to 0."
                )
            elif model.status == gp.GRB.INFEASIBLE:
                # Handle infeasible model
                print("Model is infeasible.")
            elif model.status == gp.GRB.INF_OR_UNBD:
                # Handle infeasible or unbounded model
                print("Model is infeasible or unbounded.")

            if model.status == gp.GRB.OPTIMAL or model.status == gp.GRB.SUBOPTIMAL:
                # Extract the solution
                solution = []
                for i in range(n):
                    var = model.getVarByName(f"w[{i}]")
                    # print(f"w {i} = {var.X}")
                    solution.append(var.X)

    return solution


class MyPortfolio:
    def __init__(self, price, exclude, lookback=50, gamma=0):
        self.price = price
        self.returns = price.pct_change().fillna(0)
        self.exclude = exclude
        self.lookback = lookback
        self.gamma = gamma

    def calculate_weights(self):
        # Get the assets by excluding the specified column
        assets = self.price.columns[self.price.columns != self.exclude]

        # Calculate the portfolio weights
        self.portfolio_weights = pd.DataFrame(
            index=self.price.index, columns=self.price.columns
        )

        for i in range(self.lookback + 1, len(self.price)):
            R_n = self.returns.copy()[assets].iloc[i - self.lookback : i]
            self.portfolio_weights.loc[self.price.index[i], assets] = mv_opt(
                R_n, self.gamma
            )

        self.portfolio_weights.ffill(inplace=True)
        self.portfolio_weights.fillna(0, inplace=True)

    def calculate_portfolio_returns(self):
        # Ensure weights are calculated
        if not hasattr(self, "portfolio_weights"):
            self.calculate_weights()

        # Calculate the portfolio returns
        self.portfolio_returns = self.returns.copy()
        assets = self.price.columns[self.price.columns != self.exclude]
        self.portfolio_returns["Portfolio"] = (
            self.portfolio_returns[assets]
            .mul(self.portfolio_weights[assets])
            .sum(axis=1)
        )

    def get_results(self):
        # Ensure portfolio returns are calculated
        if not hasattr(self, "portfolio_returns"):
            self.calculate_portfolio_returns()

        return self.portfolio_weights, self.portfolio_returns

