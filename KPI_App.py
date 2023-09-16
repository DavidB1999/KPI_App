# import necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly_express as px
import plotly.graph_objects as go
import plotly
import time
from Scrape_Player import Scrape_Player_via_Link_st1
from Scrape_Player import Scrape_Player_via_Link_st2
from Create_Radar import create_radar_plotly_st

# -----------------------------------
# relevant session states initialized
# -----------------------------------
# due to loss of variables between if clauses we heavily rely on sessions states
# (for all variables that are relevant across clauses)

# state indicating whether player URL was entered and is valid
if 'URL1' not in st.session_state:
    st.session_state['URL1'] = 'No'
if 'URL2' not in st.session_state:
    st.session_state['URL2'] = 'No'

# state indicating whether a player was scraped (no, 1 or 2)
if 'S1' not in st.session_state:
    st.session_state['S1'] = 'No'
if 'S2' not in st.session_state:
    st.session_state['S2'] = 'No'

# states to store names
if 'name1' not in st.session_state:
    st.session_state['name1'] = 'None'
if 'name2' not in st.session_state:
    st.session_state['name2'] = 'None'

# state to store soup in
if 'soup1' not in st.session_state:
    st.session_state['soup1'] = []
if 'soup2' not in st.session_state:
    st.session_state['soup2'] = []

# state to store data in
if 'data1' not in st.session_state:
    st.session_state['data1'] = []
if 'data2' not in st.session_state:
    st.session_state['data2'] = []

# state to store position_stats i.e. the number of positions:
if 'pos_stats1' not in st.session_state:
    st.session_state['pos_stats1'] = ''
if 'pos_stats2' not in st.session_state:
    st.session_state['pos_stats2'] = ''

# state to store unique positions (i.e. the position options) in
if 'up1' not in st.session_state:
    st.session_state['up1'] = []
if 'up2' not in st.session_state:
    st.session_state['up2'] = []

# state indicating whether selected player has multiple positions
if 'mul_pos1' not in st.session_state:
    st.session_state['mul_pos1'] = 'not_defined'  # one or multiple
if 'mul_pos2' not in st.session_state:
    st.session_state['mul_pos2'] = 'not_defined'  # one or multiple

# state to store the selected position
if 'position1' not in st.session_state:
    st.session_state['position1'] = 'not_defined'  # one or multiple
if 'position2' not in st.session_state:
    st.session_state['position2'] = 'not_defined'  # one or multiple

# state indicating whether variables have been selected
if 'radar_ready' not in st.session_state:
    st.session_state['radar_ready'] = 'No'  # one or multiple

# color for the players
if 'color1' not in st.session_state:
    st.session_state['color1'] = '#491CD0'
if 'color2' not in st.session_state:
    st.session_state['color2'] = '#FD1F2F'

# just some fun
if 'special_name1' not in st.session_state:
    st.session_state['special_name1'] = 'None'
if 'special_name2' not in st.session_state:
    st.session_state['special_name2'] = 'None'

special_names = {'Lionel Messi': 'Lionel Messi :goat:',
                 'Kylian Mbappé': 'Kylian Mbappé :racing_car:',
                 'Jamal Musiala': 'Jamal Musiala :magic_wand:',
                 'Alphonso Davies': 'Alphonso Davies :racing_car:',
                 'Thiago Alcántara': 'Thiago Alcántara :man_dancing:',
                 'Neymar': 'Neymar :magic_wand:',
                 'Cristiano Ronaldo': 'Cristiano Ronaldo :robot_face:'}

# -------------------------
# function to change states
# -------------------------

# Change to valid or invalid a URL has been picked
def valid_URL1():
    st.session_state['URL1'] = 'Yes'
    # st.session_state['S1'] = 'No'
def valid_URL2():
    st.session_state['URL2'] = 'Yes'
    # st.session_state['S2'] = 'No'
def invalid_URL1():
    st.session_state['URL1'] = 'invalid'
def invalid_URL2():
    st.session_state['URL2'] = 'invalid'

# Change to yes the data has been scraped
def Scraped1_1():
    st.session_state['S1'] = 1
def Scraped2_1():
    st.session_state['S2'] = 1
def Scraped1_2():
    st.session_state['S1'] = 2
def Scraped2_2():
    st.session_state['S2'] = 2

# Change to indicate that parameters have been picked and the radar chart can be plotted
def Ready_Radar():
    st.session_state['radar_ready'] = 'ready'


# -------------
# App structure
# -------------

# title for the app
st.title('Welcome! Wanna compare some players based on a large list of KPIs? Here you go :+1:')

# two columns
# col1, col2 = st.columns([1, 3], gap='large')

# -----------
# Left column
# -----------

# --------------------------------------------------------
# Player1 selection - via url in text field
# no condition for appearance | reseting session states only when r
# causes URL1-state to change to 'Yes' and scraped to 'No'
# --------------------------------------------------------

P1 = st.sidebar.text_input("Enter a valid URL to a player's FBref page, so I can get you your data :ok_hand:",
                     max_chars=150, help='Example: https://fbref.com/en/players/d70ce98e/Lionel-Messi',
                     on_change=valid_URL1)

# ----------------------------------------
# Step one of the scraping process
# condition: A URL must have been selected
# causes URL1-state to go back to default
# ----------------------------------------

if st.session_state['URL1'] == 'Yes':
    P1 = str(P1)        # make sure URL is a string
    soup1, unique_positions1, position_stats1, name1 = Scrape_Player_via_Link_st1(P1) # actual scraping using function
    # store everything in session states for accessibility
    st.session_state['name1'] = name1
    if name1 in special_names.keys():
        st.session_state['special_name1'] = special_names[name1]
    else:
        st.session_state['special_name1'] = name1
    st.session_state['pos_stats1'] = position_stats1
    st.session_state['up1'] = unique_positions1
    st.session_state['soup1'] = soup1

    # more than one position?
    if len(st.session_state['pos_stats1']) > 1:
        st.session_state['mul_pos1'] = 'multiple'
    else:
        st.session_state['mul_pos1'] = 'one'

    # set scraping state to 1
    Scraped1_1()

# ----------------------------------------------
# Include position selectbox
# condition: more than one position
# otherwise selected_position = first option = 0
# ----------------------------------------------

selected_position1 = 0
# store selected position in state
st.session_state['position1'] = selected_position1

# ----------------------------------------
# Step two of the scraping process
# condition: Scrape state = 1 and position1 state =! 'not defined'
# changes scrape state to 2
# ----------------------------------------

if st.session_state['S1'] == 1 and st.session_state['position1'] != 'not_defined':

    df1, position1 = Scrape_Player_via_Link_st2(st.session_state['soup1'], st.session_state['position1'],
                                                st.session_state['up1'], st.session_state['pos_stats1'])
    st.session_state['data1'] = df1
    # show a progress bar to slow down constant scraping
    progress_bar1 = st.sidebar.progress(0)
    for per_com in range(100):
        time.sleep(0.05)
        progress_bar1.progress(per_com + 1)
    Scraped1_2()

if st.session_state['S1'] == 2:
    success1 = st.sidebar.success('Data for player 1!', icon="✅")

# -------------------------------------------------
# Player2 selection - via url in text field
# Player1 fully scraped as condition for appearance
# causes URL2-state to change to 'Yes'
# -------------------------------------------------

if st.session_state['S1'] == 2:
    st.sidebar.divider()
    P2 = st.sidebar.text_input('And a URL for a second player:',
                         max_chars=150, help='Example: https://fbref.com/en/players/b66315ae/Gabriel-Jesus',
                         on_change=valid_URL2)

# --------------------------------------------------------------------
# Step one of the scraping process
# condition: A URL must have been selected and player 1 fully scraped
# causes URL1-state to go back to default
# --------------------------------------------------------------------

if st.session_state['URL2'] == 'Yes' and st.session_state['S1'] == 2:
    P2 = str(P2)        # make sure URL is a string
    soup2, unique_positions2, position_stats2, name2 = Scrape_Player_via_Link_st1(P2) # actual scraping using function
    # store everything in session states for accessibility
    st.session_state['name2'] = name2
    if name2 in special_names.keys():
        st.session_state['special_name2'] = special_names[name2]
    else:
        st.session_state['special_name2'] = name2
    st.session_state['pos_stats2'] = position_stats2
    st.session_state['up2'] = unique_positions2
    st.session_state['soup2'] = soup2

    # more than one position?
    if len(st.session_state['pos_stats2']) > 1:
        st.session_state['mul_pos2'] = 'multiple'
    else:
        st.session_state['mul_pos2'] = 'one'

    # set scraping state to 1
    Scraped2_1()
    # reset URL state to 'No'
    st.session_state['URL2'] = 'No'

# ----------------------------------------------
# Include position selectbox
# condition: more than one position
# otherwise selected_position = first option = 0
# ----------------------------------------------

selected_position2 = 0
# store selected position in state
st.session_state['position2'] = selected_position2

# ----------------------------------------
# Step two of the scraping process
# condition: Scrape state = 1 and position1 state =! 'not defined'
# changes scrape state to 2
# ----------------------------------------

if st.session_state['S2'] == 1 and st.session_state['position2'] != 'not_defined':

    df2, position2 = Scrape_Player_via_Link_st2(st.session_state['soup2'], st.session_state['position2'],
                                                st.session_state['up2'], st.session_state['pos_stats2'])
    st.session_state['data2'] = df2
    # show a progress bar to slow down constant scraping
    progress_bar2 = st.sidebar.progress(0)
    for per_com in range(100):
        time.sleep(0.05)
        progress_bar2.progress(per_com + 1)
    Scraped2_2()

if st.session_state['S2'] == 2:
    success2 = st.sidebar.success('Data for player 2!', icon="✅")


# --------
# Column 2
# --------

# ---------------------------------------------------------------
# Parameter picker
# Appears under the condition that both players are fully scraped
# ---------------------------------------------------------------

# return states into the variables
df1 = st.session_state['data1']
df2 = st.session_state['data2']
name1 = st.session_state['name1']
name2 = st.session_state['name2']


if st.session_state['S1'] == 2 and st.session_state['S2'] ==2:
    pos1 = st.session_state['up1'][st.session_state['position1']]
    pos2 = st.session_state['up2'][st.session_state['position2']]
    params = st.multiselect('Pick the KPIs of interest to your analysis.',
                              options=df1.Variables, help='I recommend picking between 6 and 10 KPIs',
                              on_change=Ready_Radar)

    st.divider()

# -----------------------------------------------
# Radar chart creation
# Condition: Parameters have to be selected first
# -----------------------------------------------


if st.session_state['radar_ready'] == 'ready':

    # save space for the plot!
    figure_container = st.container()

    st.divider()

    # color picker for plot
    col1, col2 = st.columns([1, 1], gap='large')

    st.session_state['color1'] = col1.color_picker(f'Color for {st.session_state["special_name1"]}',
                                                   value='#491CD0')
    st.session_state['color2'] = col2.color_picker(f'Color for {st.session_state["special_name2"]}',
                                                   value='#FD1F2F')

    header = st.text_input('You can edit the title', value = f'Player comparison between {name1} and {name2}')
    fig = create_radar_plotly_st(df1, df2, name1, name2, pos1, pos2, params,
                                 st.session_state['color1'], st.session_state['color2'],
                                 header)

    figure_container.plotly_chart(fig)



# ---------------------------
# Footnote for credits and co
# ---------------------------

st.divider()
st.caption('Webapp by David Brinkjans (https://github.com/DavidB1999). Data from FBref - https://fbref.com/en/')
