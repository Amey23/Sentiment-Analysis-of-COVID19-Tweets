import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import nltk
import plotly.express as px
import plotly.graph_objects as go
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import string
from collections import Counter
#from nltk.corpus import stopwords
#stop = stopwords.words('english')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True
server = app.server

#df = pd.read_csv("geocode.csv")
df = pd.read_csv("IBM_show.csv", encoding='Latin1')
emt = pd.read_csv("Emotions_India_new.csv")
df['Clean_tweets'] = df['Clean_tweets'].str.replace('\d+','')
cnt = df['Sentiment'].value_counts()
cnt = pd.DataFrame({'cat':cnt.index, 'values':cnt.values})
sent = pd.DataFrame(df[['Tweets','Sentiment']])
sent = sent.sample(1)


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Dashboard", className="display-5"),
        html.Hr(),
        html.P(
            "Sentiment Analysis", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/page-1", id="page-1-link"),
                dbc.NavLink("Emotion Analysis", href="/page-2", id="page-2-link"),
                dbc.NavLink("Word Count", href="/page-3", id="page-3-link"),
				dbc.NavLink("Embedded Hashtags", href="/page-4", id="page-4-link"),
				dbc.NavLink("Date wise Analysis", href="/page-5", id="page-5-link"),
			],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}
		
		
page_1_layout = html.Div([
    html.H4("Sentiment Analysis of COVID-19 Tweets"),
	#html.Br(),
	
	
	dbc.Row(
            [
                dbc.Col(html.Div(dbc.Alert("Total Tweets: %s" %(df.shape[0]), color="info")), width=6, lg=3),
                dbc.Col(html.Div(dbc.Alert("Neutral Tweets: %s" %((df[df['Sentiment']=='Neutral']).shape[0]), color="info")), width=6, lg=3),
                dbc.Col(html.Div(dbc.Alert("Positive Tweets: %s" %((df[df['Sentiment']=='Positive']).shape[0]), color="info")), width=6, lg=3),
                dbc.Col(html.Div(dbc.Alert("Negative Tweets: %s" %((df[df['Sentiment']=='Negative']).shape[0]), color="info")), width=6, lg=3),
            ]
        ),html.Br(),
		
		
	html.H6('Show Random Tweet:', style={'textAlign': 'left'}),
	dbc.Col(html.Div(dash_table.DataTable(
    data=sent.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in sent.columns],
	
	
	style_cell={'textAlign': 'left', 'whiteSpace':'normal','height':'auto','overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0},

    style_cell_conditional=[
	{
            'if': {'column_id': c},
			'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
))),

html.Br(),
	
    dbc.Row([dbc.Col(html.Div([
                        #html.H6('Age', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='example-graph-10',
                            figure={
                                'data': [
								{'x': cnt['cat'], 'y': cnt['values'], 'type': 'bar','labels': ['Negative','Positive','Neutral'],
								'name': 'Sentiment', 'marker':{'color': ['#4682B4','#ff7b00','#009d00']}}

                                ],
                                'layout': {
								'plot_bgcolor': colors['background'],
								'paper_bgcolor': colors['background'],
								'font': {
									'color': colors['text']
									},
									'title': 'Count of Tweets by Sentiment: Barplot',
									'xaxis':{
                                         'title':'Sentiment Category'
                                       },
                                     'yaxis':{
                                        'title':'Count of Tweets'
                                       }
										}
                            }
                        )
                    ], className="four columns"))
					
	
            ,dbc.Col(html.Div([
                        #html.H6('Age', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='example-graph-1',
                            figure={
                                'data': [
								{
								'values': cnt['values'],'type':'pie', 'labels': ['Neutral','Positive','Negative'],
								}

                                ],
                                'layout': {
                                    'title': 'Count of Tweets by Sentiment: Pie chart'
                                }
                            }
                        )
                    ], className="four columns"))
		])
			
	])		
 

 
page_4_layout = html.Div([

html.H4("Sentiment Analysis of COVID-19 Tweets"),
	html.Br(),html.H6('Choose the sentiment category', style={'textAlign': 'left'}),
	
	html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Positive', 'value': 'Positive'},
            {'label': 'Negative', 'value': 'Negative'},
            {'label': 'Neutral', 'value': 'Neutral'}
        ],
        value='Positive'
    ),
	html.Div(id='dd-output-container')
]) 

])



page_3_layout = html.Div([

html.H4("Sentiment Analysis of COVID-19 Tweets"),
	html.Br(),html.H6('Choose the sentiment category', style={'textAlign': 'left'}),
	
	html.Div([
    dcc.Dropdown(
        id='dm-dropdown',
        options=[
            {'label': 'Positive', 'value': 'Positive'},
            {'label': 'Negative', 'value': 'Negative'},
            {'label': 'Neutral', 'value': 'Neutral'}
        ],
        value='Positive'
    ),
	html.Div(id='dm-output-container')
]) 

])



page_5_layout = html.Div([
html.H4("Sentiment Analysis of COVID-19 Tweets"),
	html.Br(),html.H6('Choose the Date:', style={'textAlign': 'left'}),
	
	html.Div([
    dcc.Dropdown(
        id='date-dropdown',
        options=[
			{'label': '05-06-2020', 'value': '05-06-2020'},
			{'label': '04-06-2020', 'value': '04-06-2020'},
			{'label': '03-06-2020', 'value': '03-06-2020'},
			{'label': '02-06-2020', 'value': '02-06-2020'},
			{'label': '01-06-2020', 'value': '01-06-2020'},
			{'label': '31-05-2020', 'value': '31-05-2020'},
			{'label': '30-05-2020', 'value': '30-05-2020'},
			{'label': '29-05-2020', 'value': '29-05-2020'},
			{'label': '28-05-2020', 'value': '28-05-2020'},
            {'label': '27-05-2020', 'value': '27-05-2020'},
			{'label': '26-05-2020', 'value': '26-05-2020'},
			{'label': '25-05-2020', 'value': '25-05-2020'},
            {'label': '24-05-2020', 'value': '24-05-2020'},
			{'label': '23-05-2020', 'value': '23-05-2020'}           
			
            
        ],
        value='05-06-2020'
    ),
	html.Div(id='date-output-container')
])
])


page_2_layout = html.Div([
html.H4("Sentiment Analysis of COVID-19 Tweets"),
	html.Br(),html.Br(), 
                        html.H5('Emotion Analysis', style={'textAlign': 'left'}),
						dbc.Col(html.Div(dbc.Alert("Emotion analysis of tweets help us to analyse the psychological state of people during the pandemic.", color="info"))),html.Br(),
                       						
						dbc.Row([dbc.Col(html.Div([
                        #html.H6('Age', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='example-graph-101',
                            figure={
                                'data': [
								{'x': emt['Emotion'], 'y': emt['Emotion_score'], 'type': 'bar', 'name': 'Emotion Analysis', 'marker':{'color': ['#4682B4','#ff7b00','#009d00','#be0000','#845cd6']}}

                                ],
                                'layout': {
								'plot_bgcolor': colors['background'],
								'paper_bgcolor': colors['background'],
								'font': {
									'color': colors['text']},
									'title': 'Emotion vs Emotion_score',
									'xaxis':{
                                         'title':'Emotions Category'
                                       },
                                     'yaxis':{
                                        'title':'Emotion_score'
                                       }
										}
                            }
                        )
                    ], className="four columns"))
					
	
            ,dbc.Col(html.Div([
                        #html.H6('Age', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='example-graph-101',
                            figure={
                                'data': [
								{'values': emt['Emotion_score'], 'type': 'pie', 'labels': ['Happy','Angry','Sad','Fear','Surprise'], 'name': 'Sentiment_Day'}

                                ],
                                'layout': {
								'plot_bgcolor': colors['background'],
								'paper_bgcolor': colors['background'],
								'font': {
									'color': colors['text']},
									'title': 'Percentage of Emotions Scores'
										}
                            }
                        )
                    ], className="four columns"))
		])
		
                    ])
					
					
					

@app.callback(
    dash.dependencies.Output('date-output-container', 'children'),
    [dash.dependencies.Input('date-dropdown', 'value')])
def updt(value):
    #img = BytesIO()
    #df['Clean_tweets'] = df['Clean_tweets'].str.replace('\d+','')
    dfdt = df[df['date']==value]
    dnt = dfdt['Sentiment'].value_counts()
    dnt = pd.DataFrame({'cat':dnt.index, 'values':dnt.values})
    dnht = dfdt['hours'].value_counts()
    dnht = pd.DataFrame({'hour':dnht.index, 'values':dnht.values})
    dcd = html.Div([
	
	dbc.Row([dbc.Col(html.Div([
                        #html.H6('Age', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='example-graph-101',
                            figure={
                                'data': [
								{'x': dnt['cat'], 'y': dnt['values'], 'type': 'bar',  'name': 'Sentiment_Day', 'marker':{'color': ['#4682B4','#ff7b00','#009d00']}}

                                ],
                                'layout': {
								'plot_bgcolor': colors['background'],
								'paper_bgcolor': colors['background'],
								'font': {
									'color': colors['text']},
									'title': 'Date wise sentiment analysis',
									'xaxis':{
                                         'title':'Sentiment Category'
                                       },
                                     'yaxis':{
                                        'title':'Count of Tweets'
                                       }
										}
                            }
                        )
                    ], className="four columns"))
					
	
            ,dbc.Col(html.Div([
                        #html.H6('Age', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='example-graph-101',
                            figure={
                                'data': [
								{'values': dnt['values'], 'type': 'pie', 'labels': ['Neutral','Positive','Negative'], 'name': 'Sentiment_Day'}

                                ],
                                'layout': {
								'plot_bgcolor': colors['background'],
								'paper_bgcolor': colors['background'],
								'font': {
									'color': colors['text']},
									'title': 'Percentage of Sentiments'
										}
                            }
                        )
                    ], className="four columns"))
		]),
	
	    html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': dnht['hour'],
                    'y': dnht['values'],
                    'mode': 'markers',
                    'marker': {'size': 12}
                }
                
            ],
            'layout':{
			'plot_bgcolor': colors['background'],
								'paper_bgcolor': colors['background'],
								'font': {
									'color': colors['text']
									},
									'title': 'Hour (24 hour format) vs Tweets Count',
									'xaxis':{
                                         'title':'Hour (24 hour format)'
                                       },
                                     'yaxis':{
                                        'title':'Count of Tweets'
                                       }
				}
				}
        
    )])
	])
	
    return html.Div([dcd])
	
	
	
                             
def hashtag_extract(x):
		hashtags = []
		
		#Loop over the words in tweets
		for i in x:
			ht = re.findall(r"#(\w+)",str(i))
			hashtags.append(ht)
		return hashtags

		
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
        dcc.Location(id="url", refresh=False), sidebar, content,
		
		])
		
#app.layout = html.Div([
#    html.Img(id="image_wc"),
#])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
	df['Tweets'] = df['Tweets'].str.replace('\d+','')
	HT = hashtag_extract(df['Tweets'][df['Sentiment'] == value])
	HT = sum(HT,[])
	pos = nltk.FreqDist(HT) 
	pos = pd.DataFrame({'Hashtag': list(pos.keys()), 'Count': list(pos.values())})
	pos = pos.nlargest(columns="Count", n = 15) 
	
	hst = html.Div([
		#html.H6('Age', style={'textAlign': 'center'}),
			dcc.Graph(
				id='example-graph-10',
            figure={
                'data': [
				{'x': pos['Hashtag'],'y':pos['Count'], 'type': 'bar', 'name': 'Sentiment'}
                ],
            'layout': {
				'plot_bgcolor': colors['background'],
				'paper_bgcolor': colors['background'],
				'height':500,
				'font': {
				'color': colors['text']},
				'title': 'Embedded Hashtags vs Count',
				'xaxis':{
                       'title':'Embedded Hashtags'
                        },
                'yaxis':{
                       'title':'Hashtags Count'
                       }
				}
                }
                )
			])
	
	return html.Div([hst])


	
@app.callback(
    dash.dependencies.Output('dm-output-container', 'children'),
    [dash.dependencies.Input('dm-dropdown', 'value')])
def upd(value):
    #img = BytesIO()
    #df['Clean_tweets'] = df['Clean_tweets'].str.replace('\d+','')
    dfw = df[df['Sentiment']==value]
    dfw['Clean_tweets'] = re.sub(r"http\s+","",str(dfw['Clean_tweets']))
    dfw['Clean_tweets'] = dfw['Clean_tweets'].str.replace('[^\w\s]','')
    dfw['Clean_tweets'] = dfw['Clean_tweets'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    dfw['Clean_tweets'] = dfw['Clean_tweets'].str.replace('\d+','')
    freq = pd.Series(' '.join(map(str,dfw['Clean_tweets'])).split()).value_counts().sort_values(ascending=False)[:40]
    freq.to_dict()
    freq = pd.DataFrame({'words':freq.index, 'count':freq.values})
    freq = freq.iloc[::-1]
    wcd = html.Div([
    dcc.Graph(id='a_graph',
              figure={
        'data': [{'x':freq['count'], 
                        'y':freq['words'], 'type':'bar',
                        'orientation':'h'}],
		'layout': {
				'plot_bgcolor': colors['background'],
				'paper_bgcolor': colors['background'],
				'height':600,
				'width':1200,
				'font': {
				'color': colors['text']},
				'title': 'Frequent Words vs Count',
				'xaxis':{
                       'title':'Count of Words'
                       },
                'yaxis':{
                      'title':'frequent Words'
                       }
				}
    })
	])
	
    return html.Div([wcd])
    
    
# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return html.Div([page_1_layout])
    elif pathname == "/page-2":
        return html.Div([page_2_layout])
    elif pathname == "/page-3":
        return html.Div([page_3_layout])
    elif pathname == "/page-4":
        return html.Div([page_4_layout])
    elif pathname == "/page-5":
        return html.Div([page_5_layout])
       # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug = True)
