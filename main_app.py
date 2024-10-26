# ====== IMPORTS ====== #
import tkinter as tk
from tkinter import ttk

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import json

import requests
from bs4 import BeautifulSoup
import os
import time

from tkcalendar import Calendar

def exec_downloading_data_code():
    import downloading_data

exec_downloading_data_code()

# Create the main application window
root = tk.Tk()

# ====== GUI SETUP ====== #
root.title("US Bond Yield Curve")
root.geometry('1400x750+0+0')
root.resizable(True, True)
root.minsize(400, 400)
plt.style.use('dark_background')

notebook = ttk.Notebook(root)

# Reading the CSV file
df = pd.read_csv("Data/_US Bond Yield Data from 1990 to date.csv", sep=",")

# ====== DATE SELECTION ====== #
class TkLabel:
    def __init__(self, text, column, row, font='Microsoft Sans Serif', fontsize=15, width=22, anchor='center', bg='black', fg='white'):
        self.label = tk.Label(root, text=text, font=(font, fontsize), width=width, anchor=anchor, bg=bg, fg=fg)
        self.label.grid(column=column, row=row, columnspan=1)

start_date_label = TkLabel('Animation start date', 1, 1)
end_date_label = TkLabel('Animation end date', 1, 3)

# First label and calendar
l1 = tk.Label(root, bg='black', fg='white', text='Select a date')  # Label to display date
l1.grid(row=1, column=2)
cal1 = Calendar(root, selectmode='day')
cal1.grid(row=2, column=2, padx=20)

# Function to update first label
def update_label(event=None):
    date_str = cal1.get_date()  
    date_obj = datetime.strptime(date_str, '%m/%d/%y')  
    l1.config(text=date_obj.strftime('%B %d, %Y'))

cal1.bind("<<CalendarSelected>>", update_label)

# Second label and calendar
l2 = tk.Label(root, bg='black', fg='white', text='Select a date')  # Label to display date
l2.grid(row=3, column=2)
cal2 = Calendar(root, selectmode='day')
cal2.grid(row=4, column=2, padx=20)

# Function to update second label
def update_label2(event=None):
    date_str = cal2.get_date()  
    date_obj = datetime.strptime(date_str, '%m/%d/%y') 
    l2.config(text=date_obj.strftime('%B %d, %Y')) 

cal2.bind("<<CalendarSelected>>", update_label2)

# ====== GRAPHING AND ANIMATING ====== #
fig, ax = plt.subplots(figsize=(5, 3))
count = 0
x = df.columns.to_list()[1:]
ani = None

def plot_presets(date):
    ax.set_title(f'United States Bond Yield Curve\n{date.strftime("%b %d, %Y")}', fontname='Microsoft Sans Serif', fontsize=6)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x, fontname='Microsoft Sans Serif', fontsize=5)
    ax.set_xlabel('Tenor', fontname='Microsoft Sans Serif', fontsize=6)

    ax.tick_params(axis='y', labelsize=5)
    ax.set_ylabel('Yield Percentage', fontname='Microsoft Sans Serif', fontsize=6)
    ax.set_ylim(0, 10)
    
def start_graph_today():
    global canvas_start, ax, date, x_pos
    ax.cla()
    ax.text(16, 5, 'Loading', fontname='Microsoft Sans Serif')
    'exec_downloading_data_code()'
    
    ax.cla()
    date = datetime.today()
    count = len(df)-1
    x_pos = [1, 2.5, 4, 6, 8, 11, 14, 17, 20, 24, 28, 32]
    y = df.loc[count, '1 Mo':'30 Yr'].to_list()
    ax.plot(x_pos, y, '.-', markersize=2, linewidth=1)
    
    plot_presets(date)
    
    
    canvas_start = FigureCanvasTkAgg(fig, master=root)
    canvas_start.get_tk_widget().grid(column=4, row=1, rowspan=100)
    canvas_start.draw()

def update():
    global count, end_count, ani, ax, date, x_pos
    ax.cla()
    startdate = l1['text']
    while startdate not in df.iloc[:, 0].values:
        startdate = (datetime.strptime(startdate, '%B %d, %Y') + timedelta(days=1)).strftime('%m/%d/%Y')

    enddate = l2['text']
    if datetime.strptime(enddate, '%B %d, %Y') >= datetime.strptime(enddate, '%B %d, %Y'):
        while enddate not in df.iloc[:, 0].values:
            enddate = (datetime.strptime(enddate, '%B %d, %Y') - timedelta(days=1)).strftime('%m/%d/%Y')
        
        count = np.where(df['Date'] == startdate)[0][0]
        
        end_count = np.where(df['Date'] == enddate)[0][0]

        def update_frame(frame):
            global count, end_count
    
            ax.clear()
            x_pos = [1, 2.5, 4, 6, 8, 11, 14, 17, 20, 24, 28, 32]
            y = df.loc[count, '1 Mo':'30 Yr'].to_list()
    
            date_string = df.loc[count, 'Date']
            date = datetime.strptime(date_string, '%m/%d/%Y')
    
            ax.plot(x_pos, y, '.-', markersize=2, linewidth=1)
            plot_presets(date)
    
            count += 1
    
            if count > end_count:
                 ani.event_source.stop()
            
        if ani is not None:
            ani.event_source.stop()
        
        ani = FuncAnimation(fig, update_frame, frames=len(df) - count, interval=10)
        canvas.draw()
            
def stop():
    ani.pause()
    
def resume():
    ani.resume()

def compare():
    global canvas_compare, ax, date, x_pos
    ax.cla()
    startdate = l1['text']
    while startdate not in df.iloc[:, 0].values:
        startdate = (datetime.strptime(startdate, '%B %d, %Y') + timedelta(days=1)).strftime('%m/%d/%Y')

    enddate = l2['text']
    if datetime.strptime(enddate, '%B %d, %Y') >= datetime.strptime(enddate, '%B %d, %Y'):
        while enddate not in df.iloc[:, 0].values:
            enddate = (datetime.strptime(enddate, '%B %d, %Y') - timedelta(days=1)).strftime('%m/%d/%Y')
            
        count = np.where(df['Date'] == startdate)[0][0]
        
        end_count = np.where(df['Date'] == enddate)[0][0]
    ax.cla()
    x_pos = [1, 2.5, 4, 6, 8, 11, 14, 17, 20, 24, 28, 32]
    y_start = df.loc[count, '1 Mo':'30 Yr'].to_list()
    y_end =  df.loc[end_count, '1 Mo':'30 Yr'].to_list()
    date_string = df.loc[count, 'Date']
    date = datetime.strptime(date_string, '%m/%d/%Y')
    ax.plot(x_pos, y_start, '.-', label=l1['text'], markersize=2, linewidth=1)
    ax.plot(x_pos, y_end, '.-', label=l2['text'], markersize=2, linewidth=1)
    leg = plt.legend(loc='best')
    
    plot_presets(date)
    
    canvas_compare = FigureCanvasTkAgg(fig, master=root)
    canvas_compare.get_tk_widget().grid(column=4, row=1, rowspan=100)
    canvas_compare.draw()
        
    
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=4, row=1, rowspan=100)

graph_button = ttk.Button(root, text="⏵   Animate from/to", command=update)
graph_button.grid(column=1, row=5)

stop_button = ttk.Button(root, text="⏸   Pause", command=stop)
stop_button.grid(column=1, row=6)

resume_button = ttk.Button(root, text="⏵ Resume", command=resume)
resume_button.grid(column=1, row=7)

compare_button = ttk.Button(root, text="Compare", command=compare)
compare_button.grid(column=2, row=5)

def today_button_func():
    if ani == True: pause()
    start_graph_today()
today_button = ttk.Button(root, text="Today", command=today_button_func)
today_button.grid(column=4, row=101)


creditlabel = TkLabel('© 2024 Nicholas Tang\n(github: tang_lhnicholas)', 4, 102)

ax.set_title(f'United States Bond Yield Curve', fontname='Microsoft Sans Serif')
ax.set_xlabel('Tenor', fontname='Microsoft Sans Serif')
ax.set_ylabel('Yield Percentage', fontname='Microsoft Sans Serif')
ax.set_ylim(0, 10)

start_graph_today()
root.configure(background='black')
root.mainloop()
