# profilometer
import numpy as np
import pandas as pd
from .misc import *
import mat73
import scipy.io
__all__ = ['parse_oscilloscope_optical_left']

def read_files(input_path, txt_path, plot_path, hist_path, interactive=False):
    try:
        mat = mat73.loadmat(input_path)
    except:
        mat = scipy.io.loadmat(input_path)
    data = {
        "Wavelength (nm)": mat["output"][:,0],
        "Transmittance (dB)": mat["output"][:,1],
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(txt_path, index=False)
    p = Plot(df, interactive=interactive)
    p.plot(plot_path)
    p.hist(hist_path)

def parse_oscilloscope_optical_left(**kwargs):
    read_files(kwargs["input_path"], kwargs["txt_path"], kwargs["plot_path"], kwargs["hist_path"])
