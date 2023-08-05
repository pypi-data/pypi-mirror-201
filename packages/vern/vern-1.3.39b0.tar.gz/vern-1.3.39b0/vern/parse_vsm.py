# profilometer
import numpy as np
import pandas as pd
from .misc import *
__all__ = ['parse_vsm']

def read_files(input_path, csv_path, plot_path, hist_path, interactive=False):
    with open(input_path, "r") as f:
        lines = f.readlines()
        
    df = pd_read_csv(
        filename=input_path, encoding="cp932", sep=",", header_count=28, 
        names_old=["magnetic field (Oe)", r"magnetization ($\mathrm{erg}/\mathrm{cm}^{3}$)"], names_new=["magnetic field (Oe)", r"magnetization ($\mathrm{erg}/\mathrm{cm}^{3}$)"], unit_conversion_coefficients=[1, 1]
    )
    df.to_csv(csv_path, index=False)
    p = Plot(df, interactive)
    p.plot(plot_path)
    p.hist(hist_path)

def parse_vsm(**kwargs):
    if "interactive" in kwargs.keys():
        interactive = kwargs["interactive"]
    else:
        interactive = False
    read_files(kwargs["input_path"], kwargs["csv_path"], kwargs["plot_path"], kwargs["hist_path"], interactive=interactive)
