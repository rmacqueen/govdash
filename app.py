import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import csv, os

TOTAL_ELECTORAL_VOTES = 538

app = dash.Dash()

non_voters_map = {}
with open('turnouts.csv') as csvfile, open('vote_counts.csv') as f:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        if len(row[-1]) != 2:
            continue
        non_voters = int(row[8].replace(',', '')) - int(row[7].replace(',', ''))
        state_code = row[-1]
        non_voters_map[state_code] = non_voters
    voter_opp_map = {}
    for line in [string.split(',') for string in f.read().split('\n')]:
        sc = line[0]
        if len(sc) != 2:
            continue
        electoral_votes = int(line[1])
        margin = abs(int(line[2]) - int(line[3]))
        voter_opp = (non_voters_map[sc] / float(margin)) * (electoral_votes / TOTAL_ELECTORAL_VOTES)
        voter_opp_map[sc] = voter_opp

with open('voter_opp.csv', 'w') as voter_opp_file:
    voter_opp_file.write('State, Voter Turnout Opportunity\n')
    voter_opp_file.write('string, number\n')
    for k,v in sorted(voter_opp_map.items(), key=lambda x: x[1], reverse=True):
        voter_opp_file.write(k + "," + ("%.3f" % v) + '\n')


app.layout = html.Div([
    html.Title("Voting opportunity"),
    dcc.Graph(
        id='voting-opportunity',
        figure={
            'data': [
                go.Bar(
                    x=list(voter_opp_map.keys()),
                    y=list(voter_opp_map.values()),
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
        html.P("turnout_opportunity = (eligible_non_voters / margin_of_victory) * (state_electoral_votes / 538)"),
        html.P('''The top five 'turnout opportunity' states are perhaps unsurprising: Michigan, Pennsylvania,
            Florida, Wisconsin, and New Hampshire are among the known 'swing states' in US elections. After that, however,
            we see some not so obvious candidates for targeted GOTV strategies. Texas comes in at number 6. A very interesting
            result from the 2016 election that got sort of drowned out amidst the Trump-mania was that Texas saw a rather
            substantial shift in favor of the Democrats. Although the state still went red, the margin of victory dropped from
            16% to 9%. Moreover, with a turnout rate of 43.2%, Texas had the second lowest voter participation of all 50 states
            (only Hawaii is lower). For every 10 eligible voters who did not vote, Democrats needed only convince one of them
            to show up to vote Democrat, and Texas would have gone blue. Given the sheer size of the state, and the number of
            people who did not vote, Texas should be under serious consideration as a potential target for voter turnout opportunity in future campaigns. Arizon comes next, and it
            too exhibited a sizeable shift towards being Democratic in 2016 - it's margin dropped from 9% to 3.5% making it
            a bona fide swing state. For comparison the margins of victory in both Ohio and North Carolina were larger that
            Arizona's. '''),
        html.P(["Code and data for this project available ", html.A("here", href='http://github.com/rmacqueen/govdash')])
    ]),

])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
