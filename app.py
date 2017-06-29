#My first Dash app, displaying the US States by 'Voting Opportunity'.
#This will include how many eligible voters didn't vote, and other relevant slices.

# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.Title('''Voting Opportunity'''),

    html.H1(children=[
        '''Intro'''
    ]),

    html.P(children=[
        '''100 million americans did not vote in the 2016 presidential election.
        The election was decided by a collective 78,000 votes.
        This elections displays the opportunity for increased voter turnout, by voting district, in the United States.
        '''
    ]),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Los Angeles'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'},
                {'x': [1, 2, 3], 'y': [2, 2, 8], 'type': 'bar', 'name': 'Austin'},
                {'x': [1, 2, 3], 'y': [3, 2, 1], 'type': 'bar', 'name': 'Chicago'},
                {'x': [1, 2, 3], 'y': [4, 2, 4], 'type': 'bar', 'name': 'Detroit'},
            ],
            'layout': {
                'title': 'Top 5 Voting Opportunity Cities'
            }
        }
    )
])

"""
@app.server.before_first_request
def doStuff():
    global stuff
    stuff = initialize()
"""

if __name__ == '__main__':
    app.run_server(debug=True)