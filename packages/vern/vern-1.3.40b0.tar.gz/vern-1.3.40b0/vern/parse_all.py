# profilometer
import os, sys
import mat73
import scipy.io
from .parse_autocad import *
from .parse_oscilloscope_electrical import *
from .parse_oscilloscope_optical_right import *
from .parse_oscilloscope_optical_left import *
from .parse_oscilloscope_optical_left_xy import *
from .parse_profilometer import *
from .parse_tabular import *
from .parse_vsm import *
from .parse_mat import *
from .misc import *
__all__ = ['vern']

def read_files(**kwargs):
    with open(kwargs["input_path"], "r") as f:
        try:
            lines = f.readlines()
        except:
            lines = None
    if "_w_" in kwargs["input_filename"] or "_w." in kwargs["input_filename"]:
        kwargs = dict(kwargs, wide=True)
    if "_ly_" in kwargs["input_filename"] or "_ly." in kwargs["input_filename"]:
        kwargs = dict(kwargs, logy=True)
    if "_s_" in kwargs["input_filename"] or "_s." in kwargs["input_filename"]:
        kwargs = dict(kwargs, subplots=True)
    if "_r_" in kwargs["input_filename"] or "_r." in kwargs["input_filename"]:
        kwargs = dict(kwargs, reference=True)
    if ".mat" in kwargs["input_filename"] or "_.MAT" in kwargs["input_filename"]: # convert .mat to tabular data
        keys = get_keys_mat(kwargs["input_filename"])
        if "ref" in keys: # oscilloscope_optical
            parse_oscilloscope_optical_right(**kwargs)
        elif "output" in keys: # oscilloscope_optical
            parse_oscilloscope_optical_left(**kwargs)
        elif "x" in keys and "y" in keys: # oscilloscope_optical with x y key pair
            parse_oscilloscope_optical_left_xy(**kwargs)
        else:
            parse_mat(**kwargs)
    elif "_m1.txt" in kwargs["input_filename"] or "_m1.TXT" in kwargs["input_filename"]: # manual plot with tabular data and linear regression
        parse_tabular(**kwargs, linear_regression=True)
    elif "_c.txt" in kwargs["input_filename"] or "_c.TXT" in kwargs["input_filename"]: # manual plot from comsol (remove headers and comment)
        parse_tabular(**kwargs, remove_header=True, remove_comment=True)
    elif "_m.txt" in kwargs["input_filename"] or "_m.TXT" in kwargs["input_filename"]: # manual plot with tabular data
        parse_tabular(**kwargs)
    elif "_mi.txt" in kwargs["input_filename"] or "_mi.TXT" in kwargs["input_filename"]: # manual plot with tabular data
        parse_tabular(**kwargs, interactive=True)
    elif "_i.txt" in kwargs["input_filename"] or "_i.TXT" in kwargs["input_filename"]: # profilometer
        parse_profilometer(**kwargs, interactive=True)
    elif ".txt" in kwargs["input_filename"] or ".TXT" in kwargs["input_filename"]: # profilometer
        parse_profilometer(**kwargs)
    elif "_i.Dat" in kwargs["input_filename"]: # VSM interactive
        parse_vsm(**kwargs, interactive=True)
    elif ".Dat" in kwargs["input_filename"]: # VSM
        parse_vsm(**kwargs)
    #elif ".pptx" in filename or ".PPTX" in filename: # pptx
    #    parse_pptx.main(**kwargs)
    elif ".dxf" in kwargs["input_filename"] or ".DXF" in kwargs["input_filename"]: # autocad DXF
        parse_autocad(**kwargs)
    elif "DL9000" in lines[1]: 
        parse_oscilloscope_electrical(**kwargs)

def get_keys_mat(input_path):
    try:
        mat = mat73.loadmat(input_path)
    except:
        mat = scipy.io.loadmat(input_path)
    return mat.keys()

def vern(argv=sys.argv):
    input_path = argv[1]
    input_directory = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    input_filename_wo_ext = os.path.splitext(input_filename)[0]

    txt_directory = input_directory
    txt_filename_wo_ext = input_filename_wo_ext
    txt_filename = txt_filename_wo_ext + ".txt"
    txt_path = os.path.join(txt_directory, txt_filename)

    smooth_txt_directory = input_directory
    smooth_txt_filename_wo_ext = input_filename_wo_ext + "_smooth"
    smooth_txt_filename = smooth_txt_filename_wo_ext + ".txt"
    smooth_txt_path = os.path.join(smooth_txt_directory, smooth_txt_filename)

    csv_directory = os.path.join(input_directory, "report")
    csv_filename_wo_ext = input_filename_wo_ext
    csv_filename = csv_filename_wo_ext + ".csv"
    csv_path = os.path.join(csv_directory, csv_filename)

    plot_directory = os.path.join(input_directory, "report")
    plot_filename_wo_ext = input_filename_wo_ext
    plot_filename = plot_filename_wo_ext + ".png"
    plot_path = os.path.join(plot_directory, plot_filename)

    hist_directory = os.path.join(input_directory, "report")
    hist_filename_wo_ext = input_filename_wo_ext + "_hist"
    hist_filename = hist_filename_wo_ext + ".png"
    hist_path = os.path.join(hist_directory, hist_filename)

    smooth_plot_directory = os.path.join(input_directory, "report")
    smooth_plot_filename_wo_ext = input_filename_wo_ext + "_smooth"
    smooth_plot_filename = smooth_plot_filename_wo_ext + ".png"
    smooth_plot_path = os.path.join(smooth_plot_directory, smooth_plot_filename)

    svg_directory = os.path.join(input_directory, "report")
    svg_filename_wo_ext = input_filename_wo_ext
    svg_filename = svg_filename_wo_ext + ".svg"
    svg_path = os.path.join(svg_directory, svg_filename)

    for directory in [csv_directory, plot_directory, svg_directory]:
        if not os.path.isdir(directory):
            os.mkdir(directory)
            
    read_files(**{
        "input_path":            input_path,
        "input_directory":       input_directory,
        "input_filename":        input_filename,
        "input_filename_wo_ext": input_filename_wo_ext,

        "txt_path":            txt_path,
        "txt_directory":       txt_directory,
        "txt_filename":        txt_filename,
        "txt_filename_wo_ext": txt_filename_wo_ext,

        "smooth_txt_path":            smooth_txt_path,
        "smooth_txt_directory":       smooth_txt_directory,
        "smooth_txt_filename":        smooth_txt_filename,
        "smooth_txt_filename_wo_ext": smooth_txt_filename_wo_ext,

        "csv_path":            csv_path,
        "csv_directory":       csv_directory,
        "csv_filename":        csv_filename,
        "csv_filename_wo_ext": csv_filename_wo_ext,

        "plot_path":            plot_path,
        "plot_directory":       plot_directory,
        "plot_filename":        plot_filename,
        "plot_filename_wo_ext": plot_filename_wo_ext,

        "hist_path":            hist_path,
        "hist_directory":       hist_directory,
        "hist_filename":        hist_filename,
        "hist_filename_wo_ext": hist_filename_wo_ext,

        "smooth_plot_path":            smooth_plot_path,
        "smooth_plot_directory":       smooth_plot_directory,
        "smooth_plot_filename":        smooth_plot_filename,
        "smooth_plot_filename_wo_ext": smooth_plot_filename_wo_ext,

        "svg_path":            svg_path,
        "svg_directory":       svg_directory,
        "svg_filename":        svg_filename,
        "svg_filename_wo_ext": svg_filename_wo_ext,
    })