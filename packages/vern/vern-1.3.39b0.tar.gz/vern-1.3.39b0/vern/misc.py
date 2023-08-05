import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

def pd_read_csv(filename, encoding, sep, header_count, names_old=None, names_new=None, unit_conversion_coefficients=None, use_index=False, name_index=0, index_coefficient=0, rename_columns=True):
    df_old = pd.read_csv(filename, header=header_count, names=names_old, sep=sep, encoding=encoding, engine="python")
    df_new = pd.DataFrame()
    if use_index:
        df_new[name_index] = np.arange(df_old.shape[0])*index_coefficient
    if rename_columns: # rename the columns
        for name_old, name_new, unit_conversion_coefficient in zip(names_old, names_new, unit_conversion_coefficients):
            if "erase" not in name_new: # erase unnecessary columns
                df_new[name_new] = df_old[name_old]*unit_conversion_coefficient
    else: # reuse name of columns
        for name in df_old.columns:
            df_new[name] = df_old[name]
    return df_new

def set_min_0(df): # set minimum value of column to 0
    keys = df.keys()
    df[keys[1]] -= min(df[keys[1]])
    return df

def set_rcparams():
    plot_params = {
        "axes.labelsize": 16,
        "axes.titlesize": 16,    
        "lines.linestyle": "solid",
        "lines.linewidth": 1,
        "lines.marker": "o",
        "lines.markersize": 3,
        "xtick.major.size": 3.5,
        "xtick.minor.size": 2,
        "xtick.labelsize": 13,
        "ytick.major.size": 3.5,
        "ytick.minor.size": 2,
        "ytick.labelsize": 13,
    }
    plt.rcParams.update(plot_params)


def remove_outlier(df):
    keys = df.keys()
    qx_05 = df[keys[0]].quantile(0.05)
    qx_95 = df[keys[0]].quantile(0.95)
    qy_05 = df[keys[1]].quantile(0.05)
    qy_95 = df[keys[1]].quantile(0.95)
    df = df[(df[keys[0]] > qx_05) & (df[keys[0]] < qx_95)]
    df = df[(df[keys[1]] > qy_05) & (df[keys[1]] < qy_95)]
    return df

class Plot():
    def __init__(self, df, interactive=False, linear_regression=False, wide=False, subplots=False, reference=False, logy=False):
        self.df = df
        keys = self.df.keys()
        self.interactive = interactive
        self.linear_regression = linear_regression
        self.wide = wide
        self.subplots = subplots
        self.reference = reference
        self.logy = logy
        if self.wide:
            self.figsize = [8,3]
        else:
            self.figsize = plt.rcParamsDefault["figure.figsize"]
        if self.subplots:
            self.figsize = [7,3]
            self.subplot_x = int((len(keys)-1)**0.5)
            self.subplot_y = int(np.ceil((len(keys)-1)/self.subplot_x))
            self.figsize[0] = int(self.figsize[0] * (self.subplot_x))
            self.figsize[1] = int(self.figsize[1] * (self.subplot_y))
            plt.rcParams["legend.fontsize"] = 15
        else:
            self.subplot_x = 1
            self.subplot_y = 1
        plt.rcParams["figure.figsize"] = self.figsize
        plt.clf()
        plt.figure(figsize=self.figsize)

    def plot_(self, plot_path):
        set_rcparams()
        self.ax = plt.gca()
        keys = self.df.keys()
        xmin, ymax = min(self.df[keys[0]]), max(self.df[keys[1]])
        if len(keys) == 2: # dont need legend for two axis
            if self.linear_regression:
                self.df.plot.scatter(x=keys[0], y=keys[1], legend=None, ax=self.ax)
                params, r2 = self.fit_linear_regression()
                self.df.plot(kind="line", x=keys[0], y="fit_y", legend=None, ax=self.ax, style="-")
                self.ax.text(xmin, ymax, f"{params[0]:.3f}x+{params[1]:.3f}, r2={r2:.3f}", horizontalalignment="left", verticalalignment="top")
            else:
                self.df.plot(logy=self.logy, kind="line", x=keys[0], y=keys[1], legend=None, ax=self.ax)
            self.ax.set(ylabel=keys[1])
        else:
            if self.linear_regression:
                if self.subplots:
                    self.df.scatter(x=keys[0], ax=self.ax, fit_reg=True, subplots=self.subplots, layout=(self.subplot_x,self.subplot_y), sharex=False, sharey=True, xlabel=keys[0].split("\t")[0], ylabel=keys[0].split("\t")[1], style=["b"]*(len(keys)-1))
                else:
                    self.df.scatter(x=keys[0], ax=self.ax, fit_reg=True)
            else:
                if self.subplots:
                    if self.reference:
                        reference_df = pd.DataFrame()
                        reference_df[keys[0]] = self.df[keys[0]]
                        for i in range(len(keys)-2):
                            reference_df[keys[1]+"\u200b"*i] = self.df[keys[1]]
                        for i in range(len(keys)-2):
                            reference_df[keys[2+i]] = self.df[keys[2+i]]
                        reference_df.plot(logy=self.logy, kind="line", x=keys[0], ax=self.ax, subplots=[[reference_df.keys()[1+i], reference_df.keys()[1+(len(keys)-2)+i]] for i in range(len(keys)-2)], layout=(self.subplot_x,self.subplot_y), sharex=False, sharey=True, xlabel=keys[0].split("\t")[0], ylabel=keys[0].split("\t")[1], style=["orange"]*(len(keys)-2)+["b"]*(len(keys)-2))
                    else:
                        self.df.plot(logy=self.logy, kind="line", x=keys[0], ax=self.ax, subplots=self.subplots, layout=(self.subplot_x,self.subplot_y), sharex=False, sharey=True, xlabel=keys[0].split("\t")[0], ylabel=keys[0].split("\t")[1], style=["b"]*(len(keys)-1))
                else:
                    self.df.plot(logy=self.logy, kind="line", x=keys[0], ax=self.ax)
            self.ax.set(xlabel=keys[0].split("\t")[0])
            self.ax.set(ylabel=keys[0].split("\t")[1])
            plt.tight_layout()
        plt.savefig(plot_path, bbox_inches="tight")
 
    def on_xlims_change(self, event_ax):
        self.xlim = event_ax.get_xlim()
    def on_ylims_change(self, event_ax):
        self.ylim = event_ax.get_ylim()

    def fit_linear_regression(self):
        keys = self.df.keys()
        x, y = self.df[keys[0]].to_numpy().reshape(-1, 1), self.df[keys[1]].to_numpy().reshape(-1, 1)
        model = LinearRegression()
        model.fit(x, y)
        r2 = model.score(x, y)
        params = [model.coef_[0][0], model.intercept_[0]]
        self.df["fit_y"] = model.predict(x)
        return params, r2

    def crop_data(self):
        keys = self.df.keys()
        mask = [i for i in range(len(self.df[keys[0]]))]
        for i in range(len(keys)):
            if i == 0:
                mask = mask & (self.df[keys[i]] > self.xlim[0]) & (self.df[keys[i]] < self.xlim[1])
            else:
                mask = mask & (self.df[keys[i]] > self.ylim[0]) & (self.df[keys[i]] < self.ylim[1])
        self.df = self.df[mask]

    def plot(self, plot_path):
        self.plot_(plot_path)
        if self.interactive:
            self.xlim=None
            self.ylim=None
            self.ax.callbacks.connect("xlim_changed", self.on_xlims_change)
            self.ax.callbacks.connect("ylim_changed", self.on_ylims_change)
            plt.show()
            if self.xlim is not None and self.ylim is not None:
                self.crop_data()
            self.plot_(plot_path)
        plt.cla()

    def hist(self, hist_path):
        set_rcparams()
        self.ax = plt.gca()
        keys = self.df.keys()
        if len(keys) == 2: # dont need legend for two axis
            self.df.hist(column=keys[1], bins=100, alpha=0.5, legend=None, ax=self.ax)
            self.ax.set(xlabel=keys[1])
            self.ax.set(ylabel="Frequency")
            self.ax.set_title("")
        else:
            self.df.hist(column=keys[1:], bins=100, alpha=1, ax=self.ax)

        annotate_top_n(self.df, self.ax, top_n=5)
        plt.savefig(hist_path, bbox_inches="tight")
        plt.cla()

# https://stackoverflow.com/questions/43374920/how-to-automatically-annotate-maximum-value-in-pyplot
def annotate_top_n(df, ax, top_n=1):
    keys = df.keys()
    for key in keys[1:]:
        hist, bins = np.histogram(df[key], bins=100)
        top_n_indices = np.argpartition(hist, -1*top_n)[-1*top_n:]
        for i in range(top_n):
            index_ = top_n_indices[i]
            x_max = bins[index_]
            y_max = hist[index_]
            text = f"{x_max:.3f}"
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            arrow_props = dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
            kw = dict(xycoords='data', textcoords="offset points", arrowprops=arrow_props, bbox=bbox_props, ha="left", va="top")
            ax.annotate(text, xy=(x_max, y_max), xytext=(max(bins)/20, max(hist)/20), **kw)