#!/usr/bin/env python


# <plot_COG_profile.py, plot COG functional category profile accross samples>
# Copyright (C) <2016>  <Shengwei Hou> <housw2010@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import matplotlib.patches as mpatches
import argparse


# set up color code for each functional category
colorCode = dict({"A": '#CD8500',
                  "B": '#FF4500',
                  "C": '#DA78D6',
                  "D": '#EEE8AA',
                  "E": '#98FB98',
                  "F": '#00ff00',
                  "G": '#AFEEEE',
                  "H": '#668888',
                  "I": '#DB7093',
                  "J": '#BB475D',
                  "K": '#CDAF95',
                  "L": '#00FFCC',
                  "M": '#FF00FF',
                  "N": '#a020f0',
                  "O": '#551a88',
                  "P": '#bc8f8f',
                  "Q": '#4169e1',
                  "R": '#548854',
                  "S": '#2e8857',
                  "T": '#54ff9f',
                  "U": '#87ceeb',
                  "V": '#6a5acd',
                  "W": '#708090',
                  "X": '#ffffff',
                  "Y": '#ffff00',
                  "Z": '#ff6347'
                  })




def main():


    # parse arguments
    parser = argparse.ArgumentParser(description="Plot COG functional category profile accross samples")
    parser.add_argument("input", help="input COG functional category profile")

    args = parser.parse_args()

    # read in table
    df_table = pd.read_table(args.input)

    # split each library a dataframe
    df_dRNA_sum = df_table[['org', 'dRNA_sum', 'Func_Letter', "Func_Anno", "Func_Cat"]]
    df_rdm_sum = df_table[['org', 'rdm_sum', 'Func_Letter', "Func_Anno", "Func_Cat"]]


    # get all orgs, keep order
    orgs = []
    for org in df_dRNA_sum['org']:
        if org not in orgs:
            orgs.append(org)

    # pattern in bar for dRNA_FV, dRNA_RV and rdm_sum
    patterns = ['', 'o', 'o', '*', 'O', '.', '/', '\\']

    # get all function letters, keep order
    funcs = df_dRNA_sum[df_dRNA_sum['org']=="CC9605"]['Func_Letter']

    # index for each group
    ind = np.arange(0.2, len(orgs), 1)
    width = 0.2


    fig = plt.figure(figsize=(11.69,8.27), facecolor="white", edgecolor="black")

    # -----------------------
    #  main stacked barplot
    # -----------------------

    # left, bottom, width, height
    plot_rect = [ 0.1, 0.1, 0.6, 0.8]
    plot_ax = fig.add_axes(plot_rect, frameon=True)

    libNames = ["dRNA_sum", "rdm_sum"]
    for i, df in enumerate([df_dRNA_sum, df_rdm_sum]): # for each data frame
        bottom = [0]*len(orgs)
        for letter in funcs:

            value = df[df['Func_Letter']==letter][libNames[i]]
            color = colorCode.get(letter)
            bars = plot_ax.bar(ind+width*i, value, width=width, alpha=1, bottom = bottom, color = color)
            for bar in bars:
                bar.set_hatch(patterns[i])
            bottom = [x+y for x, y in zip(bottom, value)]

    # set xlim and ylim
    plot_ax.set_xlim(-0.3, ind[-1]+1)
    plot_ax.set_ylim(0,100)

    # set ylabel
    plot_ax.set_ylabel("Percentage", color="red")

    # set yticks and yticklabels
    plot_ax.yaxis.set_ticks(range(0, 101, 10))
    plot_ax.yaxis.set_ticklabels(range(0, 101, 10))

    # set xticks and xticklables
    plot_ax.xaxis.set_ticks([0.4,1.4,2.4,3.4,4.4])
    plot_ax.xaxis.set_ticklabels(["CC9605", "HTCC7211", "RCC299", "Eury_149", "Thaum_52"], size=12, style='normal')


    plot_ax.spines['left'].set_position(('data', -0.3))
    plot_ax.spines['left'].set_color('black')

    # turn off other spines except left
    plot_ax.spines['top'].set_visible(False)
    plot_ax.spines['bottom'].set_visible(True)
    plot_ax.spines['left'].set_visible(True)
    plot_ax.spines['right'].set_visible(False)


    # turn off ticks as well as ticklabels
    plot_ax.xaxis.set_ticks_position('bottom')
    plot_ax.yaxis.set_ticks_position("left")


    # -----------------------
    #  right legend plot
    # -----------------------

    # left, bottom, width, height
    legend_rect = [0.7, 0.1, 0.295, 0.8]
    legend_ax = fig.add_axes(legend_rect, frameon=True)
    legend_ax.set_xlim(0, 1)
    legend_ax.set_ylim(0, 1)

    # no labels
    legend_ax.xaxis.set_major_formatter(NullFormatter())
    legend_ax.yaxis.set_major_formatter(NullFormatter())

    # no spines
    legend_ax.spines['top'].set_visible(False)
    legend_ax.spines['bottom'].set_visible(False)
    legend_ax.spines['left'].set_visible(False)
    legend_ax.spines['right'].set_visible(False)

    # no ticks
    legend_ax.tick_params(axis = 'both', which = 'both', tick1On=False, tick2On=False, color="white",labelsize = 0, labelcolor="white", labeltop='off', labelright='off')


    # get all function letters, keep order
    func_cats = []
    df_dRNA_FV_CC9605=df_dRNA_sum[df_dRNA_sum['org']=="CC9605"]
    for func_cat in df_dRNA_FV_CC9605['Func_Cat']:
        if func_cat not in func_cats:
            func_cats.append(func_cat)

    # add rectangle legend
    for i, func_cat in enumerate(func_cats[::-1]):
        # add Function Category Title for each subgroup
        y_pos = 1-0.18*i
        legend_ax.text(x=0, y= y_pos, s=func_cat, size=10,style='italic', ha="left", va="center")
        funcs = df_dRNA_FV_CC9605[df_dRNA_FV_CC9605['Func_Cat']==func_cat]['Func_Letter']
        annos = df_dRNA_FV_CC9605[df_dRNA_FV_CC9605['Func_Cat']==func_cat]['Func_Anno']
        rev_annos = list(annos[::-1])

        # draw legend for each func
        for j, letter in enumerate(funcs[::-1]):
            # print letter
            color = colorCode.get(letter)
            letter_ypos = y_pos-0.03-0.015*j
            letter_rect =mpatches.Rectangle(xy=[0.05, letter_ypos], width=0.05, height=0.01, color=color, alpha=1, fill=True, ec="black", transform=legend_ax.transData,clip_on=False)
            legend_ax.add_patch(letter_rect)
            legend_ax.text(x=0.12, y= letter_ypos, s=rev_annos[j], size=8, style='normal', ha="left", va="bottom")

    # add pattern legend
    libraries = ["mdRNA-Seq", "RNA-Seq"]
    y_pos = y_pos - 0.18
    legend_ax.text(x=0, y= y_pos, s="Libraries", size=10,style='italic', ha="left", va="center")
    for m, lib in enumerate(libraries):
        lib_ypos = y_pos-0.06-0.04*m
        lib_rect =mpatches.Rectangle(xy=[0.05, lib_ypos], width=0.05, height=0.03, color="gray", alpha=1, fill=True, ec="black", transform=legend_ax.transData,clip_on=False, hatch=patterns[m])
        legend_ax.add_patch(lib_rect)
        legend_ax.text(x=0.12, y= lib_ypos, s=libraries[m], size=8, style='normal', ha="left", va="bottom")

    plt.show()



if __name__ == "__main__":
    main()
