# This script allows us to access the full scouting report via the player base page
# and then scrape the entire scouting report

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import streamlit as st



def Scrape_Player_via_Link(URL):
    base_url = 'https://fbref.com/'

    # get the page via requests
    page_link = URL
    # page_link = 'https://fbref.com/en/players/b66315ae/Gabriel-Jesus'
    page = requests.get(page_link)
    # parse it via BeautifoulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    # find player name
    script = (soup.find_all(type="application/ld+json"))
    data = [json.loads(x.string) for x in script]
    for d in data:
        name = (d['name'])

    # get the link to the full scouting report from the players base page
    for li in soup.find_all('li'):
        # print(li.a)
        if li.a is not None:
            if li.a.string == 'View Complete Scouting Report':
                full_url = base_url + li.a.get('href')

    # get the page via requests
    page = requests.get(full_url)
    # parse it via BeautifoulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # find the players position according to
    positions = soup.find_all("a", class_='sr_preset')

    unique_positions = []  # position groups
    position_stats = []  # stats compared to that group (the id we need to search for in html)

    # only care about the two positions and the related ids (scout_full_xy) of the html element
    for pos in positions:
        ps = pos.get('data-show')
        if 'scout_full' in ps:
            # cut the .assoc_ part
            ps = ps.replace('.assoc_', '')
            position_stats.append(ps)  # scout_full_xy
            unique_positions.append(pos.string)  # position name

    # here we will include the chance to decide to which position to compare
    if len(position_stats) > 1:
        options = list(range(len(position_stats)))
        selected_position = input(f'Select a position group out of {unique_positions} as {options} for {name}:')
        if int(selected_position) not in options:
            print(f'Select option {selected_position} not in the available option: {options}; defaulted to 0')
            selected_position = 0
    else:
        selected_position = 0

    ID = position_stats[int(selected_position)]
    position = unique_positions[int(selected_position)]
    summary = soup.find(id=ID)

    # the tds of class right contain the csk with per90 value
    rights = summary.find_all("td", class_='right')
    # the tds of class left endpoint [...] contain the csk with percentile values
    tooltips = summary.find_all("td", class_='left endpoint endpoint tooltip')
    # the th of class right poptip endpoint endpoint contains variable names under data-tip
    poptips = summary.find_all("th", class_='right poptip endpoint endpoint')

    # for each element in that td get me the csk
    values = []
    for ele in rights:
        csk = ele.get('csk')
        values.append(csk)

    percentiles = []
    for ele in tooltips:
        csk = ele.get('csk')
        percentiles.append(csk)

    variables = []
    for ele in poptips:
        variables.append(ele.string)

    while None in values:
        # removing None from list using remove method
        values.remove(None)

    # remove duplicate variables
    parameters = []
    duplicate_index = []
    for var_number, var in enumerate(variables):
        if var not in parameters:
            parameters.append(var)
        else:
            duplicate_index.append(var_number)

    par_values = []
    for v_num, v in enumerate(values):
        if v_num not in duplicate_index:
            par_values.append(v)

    par_percentiles = []
    for p_num, p in enumerate(percentiles):
        if p_num not in duplicate_index:
            par_percentiles.append(p)

    df = pd.DataFrame(zip(parameters, par_values, par_percentiles), columns=['Variables', 'Values', 'Percentiles'])
    return df, name, position


# same function adapted for streamlit i.e split in two
def Scrape_Player_via_Link_st1(URL):
    base_url = 'https://fbref.com/'

    # get the page via requests
    page_link = URL
    # page_link = 'https://fbref.com/en/players/b66315ae/Gabriel-Jesus'
    page = requests.get(page_link)
    # parse it via BeautifoulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # find player name
    script = (soup.find_all(type="application/ld+json"))
    data = [json.loads(x.string) for x in script]
    for d in data:
        name = (d['name'])

    # get the link to the full scouting report from the players base page
    for li in soup.find_all('li'):
        # print(li.a)
        if li.a is not None:
            if li.a.string == 'View Complete Scouting Report':
                full_url = base_url + li.a.get('href')

    # get the page via requests
    page = requests.get(full_url)
    # parse it via BeautifoulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # find the players position according to
    positions = soup.find_all("a", class_='sr_preset')

    unique_positions = []  # position groups
    position_stats = []  # stats compared to that group (the id we need to search for in html)

    # only care about the two positions and the related ids (scout_full_xy) of the html element
    for pos in positions:
        ps = pos.get('data-show')
        if 'scout_full' in ps:
            # cut the .assoc_ part
            ps = ps.replace('.assoc_', '')
            position_stats.append(ps)  # scout_full_xy
            unique_positions.append(pos.string)  # position name


    return soup, unique_positions, position_stats, name


def Scrape_Player_via_Link_st2(soup, selected_position, unique_positions, position_stats):
    ID = position_stats[int(selected_position)]
    position = unique_positions[int(selected_position)]
    summary = soup.find(id=ID)

    # the tds of class right contain the csk with per90 value
    rights = summary.find_all("td", class_='right')
    # the tds of class left endpoint [...] contain the csk with percentile values
    tooltips = summary.find_all("td", class_='left endpoint endpoint tooltip')
    # the th of class right poptip endpoint endpoint contains variable names under data-tip
    poptips = summary.find_all("th", class_='right poptip endpoint endpoint')

    # for each element in that td get me the csk
    values = []
    for ele in rights:
        csk = ele.get('csk')
        values.append(csk)

    percentiles = []
    for ele in tooltips:
        csk = ele.get('csk')
        percentiles.append(csk)

    variables = []
    for ele in poptips:
        variables.append(ele.string)

    while None in values:
        # removing None from list using remove method
        values.remove(None)

    # remove duplicate variables
    parameters = []
    duplicate_index = []
    for var_number, var in enumerate(variables):
        if var not in parameters:
            parameters.append(var)
        else:
            duplicate_index.append(var_number)

    par_values = []
    for v_num, v in enumerate(values):
        if v_num not in duplicate_index:
            par_values.append(v)

    par_percentiles = []
    for p_num, p in enumerate(percentiles):
        if p_num not in duplicate_index:
            par_percentiles.append(p)

    df = pd.DataFrame(zip(parameters, par_values, par_percentiles), columns=['Variables', 'Values', 'Percentiles'])
    return df, position


def Scrape_Player_via_Search(searchterm):
    # this might be included later
    print('Not yet available!')
