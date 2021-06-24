#!/usr/env/bin python

"""
Convert the gapminder_all.py DataFrame from wide to long format.
"""
from os import path
import pandas as pd

df = pd.read_csv("../data/gapminder_all.csv", index_col="country")

gdp = df.filter(like="gdp")
life = df.filter(like="life")
pop = df.filter(like="pop")


def melt_df(df_):
    df_ = df_.melt(ignore_index=False)
    split = df_["variable"].str.split("_", expand=True)
    split.columns = "variable", "year"
    del df_["variable"]
    df_ = df_.merge(split, left_index=True, right_index=True)
    return df_


gdp = melt_df(gdp)
life = melt_df(life)
pop = melt_df(pop)

long = pd.concat((gdp, life, pop), axis=1)
long = long.merge(df["continent"], left_index=True, right_index=True)

outfile = "../data/gapminder_long.csv"
long.to_csv(outfile)

if path.isfile(outfile):
    print("Created long DataFrame at", outfile)
