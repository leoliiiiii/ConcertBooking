#The UI file, also the main file for the project that integrates all other part code files.
#Author: Zhihan Li (zhihanli)

from tkinter import *
from tkinter import ttk
import pandas as pd
from pandastable import Table  #plz install pandastable package
import weather
import health_data_prototype
from ConcertScrapingTest1 import refreshData
from raw_data_clean import cleaning_data

#command for artist combobox
def pick_artist(event):
    this_artist = artist_box.get()
    match_loc = df[df['Artists'] == this_artist]['Zip'].tolist()
    location_box.configure(values=match_loc)

#autocomplete functionality for artist combobox
def artist_check_input(event):
    value = event.widget.get()
    if value == '':
        artist_box['values'] = all_artists
    else:
        filtered = []
        for item in all_artists:
            if value.lower() in item.lower():
                filtered.append(item)
        artist_box['values'] = filtered

#enable weather button
def click_weather():
    location = location_box.get()
    if location == '':
        return None
    lat, long = weather.getGeo(location)
    weather_df = weather.getWeather(lat, long)
    window = Toplevel(master=root)
    window.title("Weather")
    window.geometry("600x600")
    Label(window, text="a new window")
    table = Table(window, dataframe=weather_df, showtoolbar=True, showstatusbar=True)
    table.show()

#enable covid button
def click_covid():
    location = location_box.get()
    if location == '':
        return
    location = int(location_box.get())
    results_df, mapping = health_data_prototype.getdataframe()
    covid_df = health_data_prototype.getdata(results_df, location, mapping)
    window = Toplevel(master=root)
    window.title("COVID")
    window.geometry("600x600")
    Label(window, text="a new window")
    table = Table(window, dataframe=covid_df, showtoolbar=True, showstatusbar=True)
    table.show()

#enable select button
def select():
    this_artist = artist_box.get()
    if this_artist == '':
        return
    data = df[df['Artists'] == this_artist]
    if location_box.get() != '':
        loc = int(location_box.get())
        data = data[data['Zip'] == loc]
    window = Toplevel(master=root)
    window.title("Concerts")
    window.geometry("600x600")
    Label(window, text="a new window")
    table = Table(window, dataframe=data, showtoolbar=True, showstatusbar=True)
    table.show()

#load previously scraped data
def click_saved():
    global df
    df = pd.read_excel('clean_data.xlsx')
    global all_artists
    all_artists = df['Artists'].unique().tolist()
    artist_box['values'] = all_artists
    global all_locations
    all_locations = df['Zip'].unique().tolist()
    location_box['values'] = all_locations

#scrape and load new data
def click_new():
    global df
    print('Warning: scraping take about 2 hours!')
    refreshData()  # scraping the data
    df = cleaning_data()  # cleaning the scraped data
    # df = pd.DataFrame([[1, 2, 3, 4],
    #                   [5, 6, 7, 8]],
    #                   columns = ['Artists', 'Zip', 'a', 'b'])
    global all_artists
    all_artists = df['Artists'].unique().tolist()
    artist_box['values'] = all_artists
    global all_locations
    all_locations = df['Zip'].unique().tolist()
    location_box['values'] = all_locations

#main window
root = Tk();
root.title("Concert All-in-One")
root.geometry('800x600')

#dropdown box by artist
artist_label = ttk.Label(text="select an artist")
artist_label.pack()
artist_box = ttk.Combobox(root)
artist_box.pack(pady=20)
artist_box.bind("<<ComboboxSelected>>", pick_artist)
artist_box.bind("<KeyRelease>", artist_check_input)

#dopdown box by location
loc_label = ttk.Label(text="select a location")
loc_label.pack()
location_box = ttk.Combobox(root)
# location_box['state'] = 'readonly'
location_box.pack(pady=20)

#button for concerts
button = Button(root, text="Select", command=select)
button.pack(pady=20)
#button for weather
weather_btn = Button(root, text="Weather", command=click_weather)
weather_btn.pack(pady=20)
#button for covid
covid_btn = Button(root, text="COVID", command=click_covid)
covid_btn.pack(pady=20)

#button for using previously scraped data
saved_label = ttk.Label(text='click this button to use previously scraped data')
saved_label.pack()
button_saved = Button(root, text='load saved', command=click_saved)
button_saved.pack(pady=20)

#button for scraping new data
new_label = ttk.Label(text='click this button to scrape new data. \n Warning: scraping takes 2 hours!')
new_label.pack()
button_new = Button(root, text='load new', command=click_new)
button_new.pack(pady=20)

root.mainloop()
