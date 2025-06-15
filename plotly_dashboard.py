import pandas as pd
import matplotlib.colors as mcolors
from utils.data_transfer import import_sql_script, SQLiteDataObject
import dash
from dash import dcc, html, Output, Input
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# GLOBAL VARIABLES -------------------------------------------------------------------------

COLORS = 10 * list(mcolors.TABLEAU_COLORS.values())

NAV_BUTTONS = [{'nav'   : 'About',
                'id'    : 'nav-about',
                'value' : 'about'},
               {'nav'   : 'Historical Price Analysis',
                'id'    : 'nav-bar',
                'value' : 'bar'},
               {'nav'   : 'Odometer and Condition Insights',
                'id'    : 'nav-scatter',
                'value' : 'scatter'},
               {'nav'   : 'Price Analysis Subplots',
                'id'    : 'nav-multiline',
                'value' : 'multiline'}]

DATE_PICKER = [{'id'         : 'year',
                'start_date' : date(2000, 1, 1),
                'end_date'   : date(2015, 12, 31)},
               {'id'         : 'year2',
                'start_date' : date(2000, 1, 1),
                'end_date'   : date(2015, 12, 31)}]

DASHBOARD_QUERY = import_sql_script(sql_script_path = 'sql_scripts/dashboard_query.sql')

SQLITE_OBJECT = SQLiteDataObject(database_name = "tool_data")

DASHBOARD_DF = SQLITE_OBJECT.query_from_database(query = DASHBOARD_QUERY) 

FLOAT_COLS = [col for col, _dtype in DASHBOARD_DF.dtypes.items()
                  if (('float' in str(_dtype)) and
                      (_dtype != 'year'))]

YEAR_PLOT_DF = DASHBOARD_DF.groupby("year")[FLOAT_COLS].mean().reset_index()

YEAR_PLOT_DF['price_difference'] = YEAR_PLOT_DF["sellingprice"] - YEAR_PLOT_DF["mmr"]

# CLASS -------------------------------------------------------------------------------------

class PlotObject():

    def __init__(self, df):
        # from types import SimpleNamespace; self = SimpleNamespace()
        self.df = df
    
    def create_bar_plot(self):

        bar_plot = px.bar(self.df,
                          x = 'year',
                          y = 'sellingprice',
                          title = 'Average Selling Price For Cars Between 2000 and 2015',
                          color_discrete_sequence = ['#1d599e'])
        
        bar_plot.update_layout(xaxis_title = 'Years',
                               yaxis_title = 'Selling Price',
                               template = 'plotly_dark',
                               height = 700,
                               width = 1000,
                               title_x = 0.5)

        return bar_plot
    
    def create_scatter_plot(self):

        scatter_plot = px.scatter(self.df,
                                  x = 'sellingprice',
                                  y = 'odometer',
                                  title = 'Odometer and Condition Insights',
                                  color = 'condition',
                                  color_continuous_scale = 'viridis',
                                  opacity = 0.7,
                                  size_max = 45)
        
        scatter_plot.update_traces(marker = dict(size = 10,
                                                 line = dict(width = 1,
                                                             color = 'black')))
        
        scatter_plot.update_layout(xaxis_title = 'Selling Price',
                                   yaxis_title = 'Odometer',
                                   coloraxis_colorbar_title = 'Condition',
                                   template = 'plotly_dark',
                                   height = 700,
                                   width = 1000,
                                   title_x = 0.5)
        
        return scatter_plot
    
    def create_multiline_plot(self,
                              variable_name_dict = {'sellingprice'     : 'Selling Price',
                                                    'mmr'              : 'Manheim Market Report',
                                                    'odometer'         : 'Odometer',
                                                    'price_difference' : 'Price Difference',
                                                    'condition'        : 'Condition'}):

        fig = make_subplots(rows = len(variable_name_dict), 
                            cols = 1,
                            vertical_spacing = 0.1,
                            shared_xaxes = True)

        fig.update_layout(height = 1500,
                          width = 1000,
                          showlegend = True,
                          title_text = "Price Analysis Subplots",
                          title_x = 0.5,
                          template = 'plotly_dark')
        
        row_num = 1
        for y_col, cleaned_y_name in variable_name_dict.items():

            fig.add_trace(

                go.Scatter(x = self.df['year'],
                           y = self.df[y_col],
                           name = cleaned_y_name,
                           line = dict(color = COLORS[row_num]),
                           mode = 'lines',
                           opacity = 0.6,
                           legendgroup = cleaned_y_name,
                           showlegend = True),
                row = row_num,
                col = 1)
            
            fig.update_xaxes(title_text = "Years",
                             row = row_num,
                             col = 1,
                             gridcolor = 'DimGray',
                             zerolinecolor = 'DimGray')
            
            fig.update_yaxes(title_text = cleaned_y_name,
                             row = row_num,
                             col = 1,
                             gridcolor = 'DimGray',
                             zerolinecolor = 'DimGray')

            row_num += 1

        return fig


plot_object = PlotObject(df = YEAR_PLOT_DF.copy(deep=True))

# DASH -------------------------------------------------------------------------------------

app = dash.Dash(__name__,
                external_stylesheets = [
                    '/assets/style.css',
                    'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap'
                                        ], 
                external_scripts = ['/assets/script.js'])

server = app.server

app.layout = html.Div([
    html.Img(src = "https://www.ford.com/content/dam/brand_ford/en_us/brand/performance/gt/gallery/3_2/FRD_GT_000005.jpg/jcr:content/renditions/cq5dam.web.1440.1440.jpeg",
             style = {'width'      : '100vw',
                      'height'     : '100vh',
                      'object-fit' : 'cover'}),
    html.I('AutoPrice Insights',
            className = 'APInsights-style'),
    html.Nav([
        html.Button(btn['nav'],
                    id = btn['id'],
                    value = btn['value'],
                    className = 'nav-style')
        for btn in NAV_BUTTONS                          
    ], className = 'nav-location'),
    dcc.Store(id = 'plot-selection',
              data = 'none'),
    *[dcc.DatePickerRange(id = dp['id'],
                          start_date = dp['start_date'],
                          end_date = dp['end_date'],
                          style = {'display' : 'none'})
    for dp in DATE_PICKER
    ],
    html.Div(id = 'plot-container',
             className = 'plot-container-style'),
    dcc.Graph(id = 'bar-plot',
              style = {'display' : 'none'}),
    dcc.Graph(id = 'multiline-plot',
              style = {'display' : 'none'})
])

@app.callback(
    Output('plot-selection', 'data'),
    [Input('nav-about', 'n_clicks'),
     Input('nav-bar', 'n_clicks'),
     Input('nav-scatter', 'n_clicks'),
     Input('nav-multiline', 'n_clicks')],
    prevent_initial_call = True
)

def update_selection(about_clicks,
                      bar_clicks,
                      scatter_clicks,
                      multiline_clicks
                     ):

    ctx = dash.callback_context

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'nav-about':
        return 'about'
    elif triggered_id == 'nav-bar':
        return 'bar'
    elif triggered_id == 'nav-scatter':
        return 'scatter'
    elif triggered_id == 'nav-multiline':
        return 'multiline'

@app.callback(
    Output('plot-container', 'children'),
    Input('plot-selection', 'data')
)

def update_plot(plot_selection):

    
    if plot_selection == 'none':
        return ([])
    elif plot_selection == 'about':
        return (
            [html.Div([
                html.H2("About This Dashboard",
                        className = 'fade-in'),
                html.P("Welcome to AutoPrice Insights - an interactive, data-driven dashboard designed to illuminate the intricate dynamics of vehicle pricing over time. This platform empowers car enthusiasts, buyers, sellers, and analysts to explore how various factors - such as year, odometer readings, and vehicle condition - shape the market value of automobiles. Harnessing the power of Python, Dash, and Plotly, this site transforms complex automotive datasets into intuitive, visually compelling insights.",
                       className = 'fade-in'),
                html.Br(),
                html.B("Key Features:",
                       className = 'fade-in'),
                html.Div([
                    html.P("- Historical Price Analysis: Track average car prices from 2000 to 2015 and spot emerging market trends.",
                           className = 'fade-in'),
                    html.P("- Odometer & Condition Insights: Discover how usage and condition influence vehicle value, with an interactive scatter plot.",
                           className = 'fade-in'),
                    html.P("- Price Analysis Subplots: Dive deep into price analysis with multi-line plots, enabling side-by-side model or year comparisons.",
                           className = 'fade-in'),
                    html.P("- User-Friendly Interface: Seamlessly switch between views and filter data by date to tailor your exploration.",
                           className = 'fade-in'),
                ], style = {'padding'    : '20px',
                            'margin'     : 'auto',
                            'text-align' : 'left'}),
                html.I("Crafted by Scott Kordzi, this dashboard aims to make automotive data accessible, actionable, and engaging for everyone. Whether you're researching your next car, analyzing the market, or simply curious about vehicle price dynamics, AutoPrice Insights is your go-to resource for automotive price intelligence.",
                       className = 'fade-in')
            ], className = 'about-text-container')]
    )
    elif plot_selection == 'bar':
        return [
            dcc.DatePickerRange(id = 'year',
                                start_date = date(2000, 1, 1),
                                end_date = date(2015, 12, 31),
                                className = 'date-style'),
            html.Div([
                html.H2("Historical Price Analysis",
                       className = 'fade-in'),
                       html.P("This plot shows the average difference between a vehicle's selling price and its estimated market value (Manheim Market Report). Positive values indicate sales above market value, while negative values show sales below. Use this to assess market dynamics and pricing trends.",
                              className = 'fade-in')
            ], className = 'bar-text-container'),
            dcc.Graph(id = 'bar-plot',
                      figure = plot_object.create_bar_plot(),
                      style = {'margin' : '-423px 399px'}),
        ]
    elif plot_selection == 'scatter':
        return [
            html.Div([
                html.Div([
                    html.H2("Usage and Condition Influence Vehicle Value",
                            className = 'fade-in'),
                    html.P("This scatter plot maps average vehicle selling prices against mileage (odometer), with colors indicating condition scores. Each point represents a year's data. Lower mileage and higher condition (brighter colors) typically yield higher prices. Use this to explore how usage and quality impact vehicle value.",
                        className = 'fade-in'),
                ], className = 'scatter-text-container'),
                html.Div([
                    dcc.Graph(figure = plot_object.create_scatter_plot(),
                            style = {'width'        : '1000px',
                                     'margin-right' : '100px'})
                ], style = {'background-color' : '#232323',
                            'margin'           : '-266px 399px'})
            ])
        ]
    elif plot_selection == 'multiline':
        return [
            dcc.DatePickerRange(id = 'year2',
                                start_date = date(2000, 1, 1),
                                end_date = date(2015, 12, 31),
                                className = 'date-style'),
            html.Div([
                html.B("Historical Price Analysis:",
                       className = 'fade-in'),
                html.P("Explore how average car prices have evolved from 2000 to 2015. This analysis highlights periods of price acceleration or stability, and provides context for understanding the broader automotive market landscape. Such insights could help users identify the impact of economic cycles, technological advances, and shifts in consumer preferences on vehicle pricing.",
                       className = 'fade-in'),
                html.Br(),
                html.B("Manheim Market Report Insights",
                       className = 'fade-in'),
                html.P("The Manheim Market Report (MMR) is a premier industry benchmark for used vehicle values, widely recognized by financial and economic analysts. By tracking weekly and monthly price movements, the MMR provides a real-time pulse on the health of the used car market, helping users gauge current market conditions and anticipate future trends. Provides real-time, data-driven wholesale vehicle valuations for industry professionals. Used by dealers, lenders, and remarketers for precise, up-to-date pricing and inventory decisions.",
                       className = 'fade-in'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.B("Odometer Impact:",
                       className = 'fade-in'),
                html.P("Mileage is a critical factor in determining a vehicle's value. Even small differences in odometer readings can lead to significant price changes, as buyers often 'round' mileage in their minds, causing sharp price drops at key thresholds (like 10,000-mile intervals). This section visualizes how incremental mileage affects resale value, empowering users to make informed decisions when buying or selling used vehicles.",
                       className = 'fade-in'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.B("Price Difference:",
                       className = 'fade-in'),
                html.P("This plot shows the average difference between a vehicle's selling price and its estimated market value (Manheim Market Report). Positive values indicate sales above market value, while negative values show sales below. Use this to assess market dynamics and pricing trends.",
                       className = 'fade-in'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.B("Condition Analysis:",
                       className = 'fade-in'),
                html.P("A vehicle's condition plays a pivotal role in its market value. This analysis delves into how factors such as wear, maintenance, and cosmetic appearance influence pricing, offering users a deeper understanding of the premium placed on well-maintained vehicles and the depreciation associated with various condition grades. The plot tracks how the average condition of sold vehicles changes over time (2000-2015, or the selected date range)",
                       className = 'fade-in')
            ], className = 'multiline-text-container'),
            dcc.Graph(id = 'multiline-plot',
                       figure = plot_object.create_multiline_plot(),
                       style = {'margin' : '-1492px 399px'}),
        ]

@app.callback(
    Output('bar-plot', 'figure'),
    [Input('year', 'start_date'),
     Input('year', 'end_date')]
)

def update_bar_plot(start_date, end_date):

    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    filtered_df = YEAR_PLOT_DF[(YEAR_PLOT_DF['year'] >= start_year) & (YEAR_PLOT_DF['year'] <= end_year)]
    plot_object = PlotObject(df = filtered_df)

    return plot_object.create_bar_plot()

@app.callback(
    Output('multiline-plot', 'figure'),
    [Input('year2', 'start_date'),
     Input('year2', 'end_date')]
)

def update_multiline_plot(start_date, end_date):

    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    filtered_df = YEAR_PLOT_DF[(YEAR_PLOT_DF['year'] >= start_year) & (YEAR_PLOT_DF['year'] <= end_year)]
    plot_object = PlotObject(df = filtered_df)

    return plot_object.create_multiline_plot()

if __name__ == '__main__':
    import os
    app.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 8000)), debug = False)