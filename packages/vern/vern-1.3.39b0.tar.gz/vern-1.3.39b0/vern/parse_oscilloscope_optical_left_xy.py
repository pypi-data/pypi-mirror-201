# profilometer
import numpy as np
import pandas as pd
from .misc import *
import mat73
import scipy.io
__all__ = ['parse_oscilloscope_optical_left_xy']

def read_files(input_path, txt_path, smooth_txt_path, plot_path, hist_path, smooth_plot_path, interactive=False, wide=False):
    try:
        mat = mat73.loadmat(input_path)
    except:
        mat = scipy.io.loadmat(input_path)
    data = {
        "Time (ns)": mat["x"][0,:]*1e9,
        "Voltage (mV)": mat["y"][0,:]*1e3,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(txt_path, index=False)
    p = Plot(df, interactive=interactive, wide=wide)
    p.plot(plot_path)
    p.hist(hist_path)
    smooth_df = df.copy()
    smooth_df["Voltage (mV)"] = smooth_df["Voltage (mV)"].rolling(20).mean()
    smooth_df.to_csv(smooth_txt_path, index=False)
    p = Plot(smooth_df, interactive=interactive)
    p.plot(smooth_plot_path)

def parse_oscilloscope_optical_left_xy(**kwargs):
    wide = kwargs["wide"] if "wide" in kwargs.keys() else False
    read_files(kwargs["input_path"], kwargs["txt_path"], kwargs["smooth_txt_path"], kwargs["plot_path"], kwargs["hist_path"], kwargs["smooth_plot_path"], wide=wide)
