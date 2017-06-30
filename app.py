import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import csv, os

TOTAL_ELECTORAL_VOTES = 538

app = dash.Dash()

state_map = {}
with open('turnouts.csv') as csvfile, open('vote_counts.csv') as f:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        if len(row[-1]) != 2:
            continue
        non_voters = int(row[8].replace(',', '')) - int(row[7].replace(',', ''))
        state_code = row[-1]
        state_map[state_code] = non_voters
    for line in [string.split(',') for string in f.read().split('\n')]:
        sc = line[0]
        if len(sc) != 2:
            continue
        electoral_votes = int(line[1])
        margin = abs(int(line[2]) - int(line[3]))
        state_map[sc] = (state_map[sc] / float(margin)) * (electoral_votes / TOTAL_ELECTORAL_VOTES)

app.layout = html.Div([
    html.Title("Voting opportunity"),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Bar(
                    x=list(state_map.keys()),
                    y=list(state_map.values()),
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'State'},
                yaxis={'title': 'Turnout opportunity'},
                title="Voter turnout opportunity by state for the 2016 presidential election"
            )
        }
    ),
    html.Div([
        html.P('''A state's turnout opportunity is calculated by taking the ratio of non-voters to the margin of victory,
            and then scaling that value by the proportion of total electoral votes granted to that state. It is designed
            to capture how worthwhile it would be to focus energies to GOTV strategies in that state.'''),
        html.P("(eligible_non_voters / margin_of_victory) * (state_electoral_votes / 538)"),
        html.P(["Code and data for this project available ", html.A("here", href='http://github.com/rmacqueen/govdash')])
    ]),

])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
