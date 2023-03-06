import json
import os
import time
from ResearchUtils.MathUtil import isFloat
from typing import List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import SubplotBase, Axes
from matplotlib.text import Text
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame, Series
import pandas
import numpy as np
import keyboard

class Grapher:
    menu_file = ".\\config_menu.json"
    save_file = ".\\configs_savedata.json"
    files = []
    data = []
    x_label = ""
    y_label = ""
    legend_names = [["", "", ""], ["", "", ""]]
    line_markers = [[None], [None]]
    line_colors = [["k", "k", "k"]]
    line_kinds = [["dotted", "--", "-"], ["dotted", "--", "-"]]

    irregular_legends = True
    irregular_line_names = [""]
    irregular_line_markers = [None, None, None, None, None]
    irregular_line_colors = ["k", "k", "k"]
    irregular_line_kinds = ["dotted", "--", "-"]

    contains_text = True
    texts = [""]
    text_coords = [[0, 0], [0.8, 0.8]]
    text_fontsizes = [15, 15]
    text_colors = ["k", "k"]
    text_instances: List[Text] = []

    xdigit = 0
    ydigit = 1

    xlabel_pad = 8
    ylabel_pad = 8

    legend_loc_index = 0
    legend_loc = ["best", "upper left", "upper right", "center left", "center", "center right", "lower left", "lower center", "lower right"]
    legend_anchor = (0, 0)

    x_boundary = [0, 0]
    y_boundary = [0, 0]
    xtick_step = 0
    ytick_step = 0


    fig_size = (8, 5)
    fig: Figure
    ax: Axes

    font_family = "Arial"
    mathtext_fontset = "stix"
    mathtext_default = "default"
    font_size = 16 #メモリの数値のフォントサイズ
    xlabel_fontsize = 22
    ylabel_fontsize = 22
    xtick_direction = "in"
    ytick_direction = "in"
    xtick_minor_visible = True
    ytick_minor_visible = True
    xtick_major_width = 1.5
    ytick_major_width = 1.5
    xtick_minor_width = 1
    ytick_minor_width = 1
    xtick_major_size = 10
    ytick_major_size = 10
    xtick_minor_size = 6
    ytick_minor_size = 6
    xtick_top = False #上部x軸の目盛り
    ytick_right = False #右側y軸の目盛り
    xtick_major_pad = 10
    ytick_major_pad = 10
    axes_linewidth = 1.4 #囲みの太さ
    axes_xmargin = 0.01
    axes_ymargin = 0.01

    def __init__(self, tsv=True):
        self.setConfigFromMenu()
        self.rcParamsConfigure()
        self.fig, self.ax = plt.subplots(figsize=self.fig_size)
        #log scale
        # self.ax.set_yscale("log")
        plt.subplots_adjust(left=0.2, bottom=0.2)
        for f in self.files:
            if(tsv):
                self.data.append(pandas.read_csv(f, sep="\t"))
            else:
                self.data.append(pandas.read_csv(f))
        self.plot()
        # Reflect Menu Configs
        self.legendConfigure()
        self.setBoundary()
        self.setTicks()

    def updateConfigMenu(self):
        cur_config: dict
        with open(menu_file, "r") as fp:
            cur_config = json.load(fp)
        self.updatePrePlotConfigDict(cur_config)
        self.updatePostPlotConfigDict(cur_config)
        with open(menu_file, "w") as fp:
            json.dump(cur_config, fp, indent=4)

    def saveConfig(self, save_name: str):
        save_data: dict
        with open(save_file, "r") as fp:
            save_data = json.load(fp)
        config = {}
        config = self.updatePrePlotConfigDict(config)
        config = self.updatePostPlotConfigDict(config)
        save_data[save_name] = config
        with open(save_file, "w") as fp:
            json.dump(save_data, fp, indent=4)

    def setConfigFromMenu(self):
        with open(menu_file, "r") as fp:
            imported_config = json.load(fp)
        self.assimilatePrePlotConfig(imported_config)
        self.assimilatePostPlotConfig(imported_config)

    def updatePostPlotConfigDict(self, config):
        config["legend_loc_index"] = self.legend_loc_index
        config["legend_anchor"] = self.legend_anchor
        config["x_boundary"] = self.x_boundary
        config["y_boundary"] = self.y_boundary
        config["xtick_step"] = self.xtick_step
        config["ytick_step"] = self.ytick_step
        config["text_coords"] = self.text_coords
        return config

    def assimilatePostPlotConfig(self, config: dict):
        self.legend_loc_index = config["legend_loc_index"]
        self.legend_anchor = config["legend_anchor"]
        self.x_boundary = config["x_boundary"]
        self.y_boundary = config["y_boundary"]
        self.xtick_step = config["xtick_step"]
        self.ytick_step = config["ytick_step"]
        self.text_coords = config["text_coords"]

    def updatePrePlotConfigDict(self, config):
        config["files"] = self.files
        config["x_label"] = self.x_label
        config["y_label"] = self.y_label
        config["label_names"] = self.legend_names
        config["line_markers"] = self.line_markers
        config["line_colors"] = self.line_colors
        config["line_kinds"] = self.line_kinds
        config["irregular_legends"] = self.irregular_legends
        config["irregular_line_names"] = self.irregular_line_names
        config["irregular_line_markers"] = self.irregular_line_markers
        config["irregular_line_colors"] = self.irregular_line_colors
        config["irregular_line_kinds"] = self.irregular_line_kinds
        config["contains_text"] = self.contains_text
        config["texts"] = self.texts
        config["text_fontsizes"] = self.text_fontsizes
        config["text_colors"] = self.text_colors
        config["xlabel_pad"] = self.xlabel_pad
        config["ylabel_pad"] = self.ylabel_pad
        return config

    def assimilatePrePlotConfig(self, config: dict):
        self.files = config["files"]
        self.x_label = config["x_label"]
        self.y_label = config["y_label"]
        self.legend_names = config["label_names"]
        self.line_markers = config["line_markers"]
        self.line_colors = config["line_colors"]
        self.line_kinds = config["line_kinds"]
        self.irregular_legends = config["irregular_legends"]
        self.irregular_line_names = config["irregular_line_names"]
        self.irregular_line_markers = config["irregular_line_markers"]
        self.irregular_line_colors = config["irregular_line_colors"]
        self.irregular_line_kinds = config["irregular_line_kinds"]
        self.contains_text = config["contains_text"]
        self.texts = config["texts"]
        self.text_fontsizes = config["text_fontsizes"]
        self.text_colors = config["text_colors"]
        self.xlabel_pad = config["xlabel_pad"]
        self.ylabel_pad = config["ylabel_pad"]


    def plot(self):
        for i, dframe in enumerate(self.data):
            x: Series = dframe.iloc[:, 0]
            print(x)
            y_data: DataFrame = dframe.drop(columns=dframe.columns[0])
            print(y_data.columns)
            for j, y_col_name in enumerate(y_data):
                if(self.irregular_legends):
                    label = None
                else:
                    label = self.legend_names[i][j]
                self.ax.plot(x, y_data[y_col_name], label=label, linestyle=self.line_kinds[i][j], color=self.line_colors[i][j], marker=self.line_markers[i][j], clip_on=(self.line_markers[i][j] is None), linewidth=2)
        if(self.irregular_legends):
            self.drawIrregularLegends()
        self.ax.set_xlabel(self.x_label, fontsize=self.xlabel_fontsize, labelpad=self.xlabel_pad)
        self.ax.set_ylabel(self.y_label, fontsize=self.ylabel_fontsize, labelpad=self.ylabel_pad)
        self.drawTexts()
        self.legendConfigure()
        #self.setMaxDigits()
        self.setTicks()

    def drawIrregularLegends(self):
        for i in range(len(self.irregular_line_names)):
            self.ax.plot([], [], label=self.irregular_line_names[i], linestyle=self.irregular_line_kinds[i], color=self.irregular_line_colors[i], marker=self.irregular_line_markers[i])

    def drawTexts(self):
        if(self.contains_text):
            for i in range(len(self.texts)):
                text = self.ax.text(self.text_coords[i][0], self.text_coords[i][1], self.texts[i], fontsize=self.text_fontsizes[i], color=self.text_colors[i], transform=self.ax.transAxes)
                self.text_instances.append(text)

    def legendConfigure(self, manual=False):
        if(self.legend_anchor == (0, 0)):
            self.ax.legend(loc=self.legend_loc[self.legend_loc_index], frameon=False, framealpha=0)
        else:
            self.ax.legend(loc="upper left", bbox_to_anchor=self.legend_anchor, frameon=False, framealpha=0)

    def incrementLegendLocIndex(self):
        self.legend_loc_index += 1
        if(self.legend_loc_index > len(self.legend_loc) - 1):
            self.legend_loc_index = 0

    def decrementLegendLocIndex(self):
        self.legend_loc_index -= 1
        if(self.legend_loc_index < 0):
            self.legend_loc_index = len(self.legend_loc) - 1

    def setMaxDigits(self):
        self.ax.xaxis.set_major_formatter(plt.FormatStrFormatter("%." + str(self.xdigit) + "f"))
        self.ax.xaxis.set_major_formatter(plt.FormatStrFormatter("%." + str(self.ydigit) + "f"))

    def rcParamsConfigure(self):
        plt.rcParams["font.family"] = self.font_family
        plt.rcParams["font.size"] = self.font_size
        plt.rcParams["xtick.direction"] = self.xtick_direction
        plt.rcParams["ytick.direction"] = self.ytick_direction
        plt.rcParams["xtick.minor.visible"] = self.xtick_minor_visible
        plt.rcParams["ytick.minor.visible"] = self.ytick_minor_visible
        plt.rcParams["xtick.major.width"] = self.xtick_major_width
        plt.rcParams["ytick.major.width"] = self.ytick_major_width
        plt.rcParams["xtick.minor.width"] = self.xtick_minor_width
        plt.rcParams["ytick.minor.width"] = self.ytick_minor_width
        plt.rcParams["xtick.major.size"] = self.xtick_major_size
        plt.rcParams["ytick.major.size"] = self.ytick_major_size
        plt.rcParams["xtick.minor.size"] = self.xtick_minor_size
        plt.rcParams["ytick.minor.size"] = self.ytick_minor_size
        plt.rcParams["xtick.top"] = self.xtick_top
        plt.rcParams["ytick.right"] = self.ytick_right
        plt.rcParams["axes.linewidth"] = self.axes_linewidth
        plt.rcParams["axes.xmargin"] = self.axes_xmargin
        plt.rcParams["axes.ymargin"] = self.axes_ymargin
        plt.rcParams["mathtext.fontset"] = self.mathtext_fontset
        plt.rcParams["mathtext.default"] = "regular"
        plt.rcParams["xtick.major.pad"] = self.xtick_major_pad
        plt.rcParams["ytick.major.pad"] = self.ytick_major_pad

    def setBoundary(self):
        if self.x_boundary != [0, 0]:
            self.ax.set_xlim(self.x_boundary[0], self.x_boundary[1])
        if self.y_boundary != [0, 0]:
            self.ax.set_ylim(self.y_boundary[0], self.y_boundary[1])

    def setTicks(self):
        if self.xtick_step != 0:
            self.ax.xaxis.set_major_locator(MultipleLocator(self.xtick_step))
            self.ax.xaxis.set_minor_locator(MultipleLocator(self.xtick_step / 2))
        if self.ytick_step != 0:
            self.ax.yaxis.set_major_locator(MultipleLocator(self.ytick_step))
            self.ax.yaxis.set_minor_locator(MultipleLocator(self.ytick_step / 2))

    def turnFigSize(self):
        if(self.fig_size == (7, 7)):
            print("hi")
            self.fig_size = (8, 5)
            self.fig.set_figwidth(8)
            self.fig.set_figheight(5)
        if(self.fig_size == (8, 5)):
            self.fig_size = (7, 7)
            self.fig.set_size_inches(7, 7)

    def modify(self):
        command = True
        value: float
        plt.pause(0.5)
        while(command):
            plt.pause(0.5)
            command = input("変更対象:")
            value: str = input("変更後の数値:")
            if(isFloat(value)):
                value = float(value)
                if(command == "xstep"):
                    self.xtick_step = value
                    self.setTicks()
                if(command == "ystep"):
                    self.ytick_step = value
                    print(value)
                    print(self.ytick_step)
                    self.setTicks()
                if(command == "xmin"):
                    self.x_boundary[0] = value
                    self.x_boundary[1] = self.ax.get_xlim()[1]
                    self.setBoundary()
                if(command == "xmax"):
                    self.x_boundary[1] = value
                    self.x_boundary[0] = self.ax.get_xlim()[0]
                    self.setBoundary()
                if(command == "ymin"):
                    self.y_boundary[0] = value
                    self.y_boundary[1] = self.ax.get_ylim()[1]
                    self.setBoundary()
                if(command == "ymax"):
                    self.y_boundary[1] = value
                    self.y_boundary[0] = self.ax.get_ylim()[0]
                    self.setBoundary()
                if(command == "legend"):
                    if(value == 0):
                        print("Legend setting mode")
                        while True:
                            plt.pause(0.1)
                            event = keyboard.read_event()
                            if(event.name == "ctrl"):
                                self.incrementLegendLocIndex()
                                self.legendConfigure()
                            if(event.name == "alt"):
                                self.decrementLegendLocIndex()
                                self.legendConfigure()
                            if(event.name == "esc"):
                                break
                    if(value == 1):
                        print("Legend manual setting mode")
                        while True:
                            plt.pause(0.3)
                            event = keyboard.read_event()
                            anchor_x = self.legend_anchor[0]
                            anchor_y = self.legend_anchor[1]
                            if(event.name == "alt"):
                                self.legend_anchor = (anchor_x + 0.025, anchor_y)
                                self.legendConfigure()
                            if(event.name == "ctrl"):
                                self.legend_anchor = (anchor_x - 0.025, anchor_y)
                                self.legendConfigure()
                            if(event.name == "delete"):
                                self.legend_anchor = (anchor_x, anchor_y + 0.025)
                                self.legendConfigure()
                            if(event.name == "space"):
                                self.legend_anchor = (anchor_x, anchor_y - 0.025)
                                self.legendConfigure()
                            if(event.name == "esc"):
                                break
                if(command=="text"):
                    value = int(value) - 1
                    while True:
                        plt.pause(0.3)
                        event = keyboard.read_event()
                        x = self.text_coords[value][0]
                        y = self.text_coords[value][1]
                        if (event.name == "alt"):
                            self.text_coords[value][0] = x + 0.025
                        if (event.name == "ctrl"):
                            self.text_coords[value][0] = x - 0.025
                        if (event.name == "delete"):
                            self.text_coords[value][1] = y + 0.025
                        if (event.name == "space"):
                            self.text_coords[value][1] = y - 0.025
                        if (event.name == "esc"):
                            break
                        self.text_instances[value].set_position(self.text_coords[int(value)])
                if(command == "size"):
                    self.turnFigSize()
                    plt.pause(0.1)
                if(command == "save"):
                    file_stem_name = input("tell file name >>")
                    self.saveConfig(file_stem_name)
                    file_name = os.path.join("C:\\Users\\genko\\Documents\\Lab\\new_graph_images", file_stem_name)
                    dir = "C:\\Users\\genko\\Documents\\Lab\\new_graph_images"
                    plt.rcParams["figure.dpi"] = 300
                    plt.savefig(file_name + ".png", bbox_inches="tight")
                    # plt.savefig(file_name + ".pdf", bbox_inches="tight")
                    plt.savefig(dir + "\\eps\\" + file_stem_name + ".eps", bbox_inches="tight")

            if(command == "q"):
                self.updateConfigMenu()
                break

k = Grapher()
k.modify()
