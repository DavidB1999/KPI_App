import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly
from Scrape_Player import Scrape_Player_via_Link

# a function to create a plotly radar chart based on data scraped from FBref
def create_radar_plotly(URL1, URL2, params):
    df1, player1, pos1 = Scrape_Player_via_Link(URL1)
    df2, player2, pos2 = Scrape_Player_via_Link(URL2)

    if pos1 != pos2:
        print(f'You selected {pos1} for {player1} and {pos2} for {player2}. A mismatch of position groups'
              f'makes the percentiles values incomparable, as these are derived from within a position group.'
              f'Consider selecting matching positions / player with matching positions')

    data1 = df1[df1['Variables'].isin(params)]
    data2 = df2[df2['Variables'].isin(params)]
    # ensure data is sorted by the order of parameters selected!
    dummy = pd.Series(params, name='Variables').to_frame()
    data1 = pd.merge(dummy, data1, on='Variables', how='left')
    data2 = pd.merge(dummy, data2, on='Variables', how='left')

    # duplicate the first element for closing line (only relevant if lines are drawn!)
    r1 = [int(x) for x in data1.Percentiles]
    r1.append(r1[0])
    r2 = [int(x) for x in data2.Percentiles]
    r2.append(r2[0])
    Values1 = [float(x) for x in data1.Values]
    Values1.append(Values1[0])
    Values2 = [float(x) for x in data2.Values]
    Values2.append(Values2[0])

    parameters = params
    parameters.append(parameters[0])

    fig = go.Figure()
    # player 1
    fig.add_trace(go.Scatterpolar(
        r=r1,
        theta=parameters,
        fill='toself',
        name= player1,
        mode='markers',
        customdata=Values1,
        hovertemplate=(
                'Percentile: %{r} <br>' +
                'Value: %{customdata}'
        )

    ))
    # player 2
    fig.add_trace(go.Scatterpolar(
        r=r2,
        theta=parameters,
        fill='toself',
        name=player2,
        customdata=Values2,
        mode='markers',
        hovertemplate=(
                'Percentile: %{r} <br>' +
                'Value: %{customdata}'
        )

    ))

    fig.update_layout(
        # general visual
        paper_bgcolor='#333333',
        # 333333, #d9c4b6
        # polar area
        polar=dict(
            hole=0,
            bgcolor='#f5f5f5',
            gridshape='circular',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='black',
                gridcolor='#333333',
                showline=False,
                tickfont=dict(
                    color='black',
                    size=10)),
            angularaxis=dict(
                color='#f5f5f5',
                gridcolor='#333333',
                layer='below traces'
            )),

        showlegend=True,
        colorway=['#491CD0', '#FD1F2F'],  # colors for the traces

        # hoverlabel
        hoverlabel=dict(
            # bgcolor='pink',
            bordercolor='black',
            font=dict(
                color='white'
            )),

        # title
        title=dict(
            text=f'Player comparison between {player1} and {player2} \n'
                 f'{pos1}',
            font=dict(
                size=20,
                color='#f5f5f5'),
            x=0.5, xanchor='center',
            y=.975, yanchor='top'
        ),

        # legend
        legend=dict(
            bgcolor='#f5f5f5',
            bordercolor='#333333',
            font=dict(
                size=12),
            title=dict(
                text='Players',
                font=dict(
                    size=15)
            )
        )
    )

    plotly.offline.plot(fig)

# create_radar_plotly adpated for the specific use in streamlit
def create_radar_plotly_st(df1, df2, player1, player2, pos1, pos2, params, col1, col2, header):

    data1 = df1[df1['Variables'].isin(params)]
    data2 = df2[df2['Variables'].isin(params)]
    # ensure data is sorted by the order of parameters selected!
    dummy = pd.Series(params, name='Variables').to_frame()
    data1 = pd.merge(dummy, data1, on='Variables', how='left')
    data2 = pd.merge(dummy, data2, on='Variables', how='left')

    # duplicate the first element for closing line (only relevant if lines are drawn!)
    r1 = [int(x) for x in data1.Percentiles]
    # r1.append(r1[0])
    r2 = [int(x) for x in data2.Percentiles]
    # r2.append(r2[0])
    Values1 = [float(x) for x in data1.Values]
    # Values1.append(Values1[0])
    Values2 = [float(x) for x in data2.Values]
    # Values2.append(Values2[0])

    parameters = params
    # parameters.append(parameters[0])
    fig = go.Figure()
    # player 1
    fig.add_trace(go.Scatterpolar(
        r=r1,
        theta=parameters,
        fill='toself',
        name=f'{player1} ({pos1})',
        mode='markers',
        customdata=Values1,
        hovertemplate=(
                'Percentile: %{r} <br>' +
                'Value: %{customdata}'
        )

    ))
    # player 2
    fig.add_trace(go.Scatterpolar(
        r=r2,
        theta=parameters,
        fill='toself',
        name=f'{player2} ({pos2})',
        customdata=Values2,
        mode='markers',
        hovertemplate=(
                'Percentile: %{r} <br>' +
                'Value: %{customdata}'
        )

    ))

    fig.update_layout(
        # general visual
        paper_bgcolor='#333333',
        # 333333, #d9c4b6
        # polar area
        polar=dict(
            hole=0,
            bgcolor='#f5f5f5',
            gridshape='circular',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='black',
                gridcolor='#333333',
                showline=False,
                tickfont=dict(
                    color='black',
                    size=10)),
            angularaxis=dict(
                color='#f5f5f5',
                gridcolor='#333333',
                layer='below traces'
            )),

        showlegend=True,
        colorway=[col1, col2],  # colors for the traces '#491CD0', '#FD1F2F'

        # hoverlabel
        hoverlabel=dict(
            # bgcolor='pink',
            bordercolor='black',
            font=dict(
                color='white'
            )),

        # title
        title=dict(
            text=header,
            font=dict(
                size=20,
                color='#f5f5f5'),
            x=0.5, xanchor='center',
            y=.975, yanchor='top'
        ),

        # legend
        legend=dict(
            bgcolor='#f5f5f5',
            bordercolor='#333333',
            font=dict(
                size=12,
                color='#333333'),
            title=dict(
                text='Players',
                font=dict(
                    size=15,
                    color='#333333')
            )
        )
    )
    fig.add_annotation(xref="paper", yref="paper", x=0.475, y=- 0.3,
                       text="Radar chart by David Brinkjans (https://github.com/DavidB1999) | Data from FBref - https://fbref.com/en/",
                       showarrow=False,
                       font=dict(
                           color='white',
                           size=10
                       ))

    return fig




