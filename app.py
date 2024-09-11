import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import data_analysis as da


database = da.Database()

#Inicializando la app de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME])

database_response = {
    'all_clients':database.clientes(), #Todos los clientes 
    'active_clients': database.active_clients(), #Todos los clientes activos
    'active_aquirers': database.aquierers_activos(), #Todos los aquirers activos
    'vol_transaccional':database.volumen_transaccional(), #Regresa un float del volumen transaccional
    'transacciones':database.transacciones_merchant_id(), #Regresa un dataframe del total transaccionado por merchant
    'zona':database.zone(), #regresa un dataframe del numero de clientes por zona
    'issuer':database.card_issuers(), #regresa un dataframe del numero de transacciones procesadas por banco
    'tipo_tarjeta':database.debito_credito(), #regresa un dataframe del número de tarjetas por tipo (crédito, debito)
    'transacciones_tiempo':database.transacciones_en_tiempo(), #regresa un dataframe con el total transaccionado durante las semanas en el tiempo transcurrido desde el inicio de la BD
    'clientes_churn':database.cliente_churn(), #regresa un dataframe con
    'churn_rate':database.churn_rate(), #regresa el churn rate desde el inicio del periodo hasta hoy
    'vol_transaccional_mcc':database.vol_transaccional_MCC(), #regresa un dataframe con el volumen transaccional por MCC
}

all_clients = database_response['all_clients']
all_clients = database.clientes()
active_clients = database_response['active_clients']
active_aquirers = database_response['active_aquirers']
vol_transaccional = database_response['vol_transaccional']
transacciones = database_response['transacciones']
zona = database_response['zona']
issuer = database_response['issuer']
tipo_tarjeta = database_response['tipo_tarjeta']
transacciones_en_tiempo = database_response['transacciones_tiempo']
clientes_churn = database_response['clientes_churn']
vol_transaccional_mcc = database_response['vol_transaccional_mcc']
churn_rate = database_response['churn_rate']


#Colores
colores = {
    'background': '#FFFFA',
    'text': '#333333',
    'primary': '#0F7BFF',
    'secondary': '#6C757D',
    'success': '#28A745',
    'info': '#17B2B8',
    'warning': '#FFC107',
    'danger': '#DC3545',
}

# CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title id="title_color">PayCode</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #F8F9FA;
            }
            #title_color {
                color: #DC3545;
            }
            .card {
                border: none;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            .nav-link {
                color: #333333 !important;
                font-weight: 500;
            }
            .nav-link.active {
                background-color: #007BFF !important;
                color: white !important;
            }
            .tab-content {
                background-color: white;
                border-radius: 0 0 10px 10px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Definiendo el layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Paycode", className="my-4 text-center display-4 fw-bold text-primary"), width=12)
    ]),
    
    # Información clave
    dbc.Row([
        dbc.Col(dbc.Card([
            html.I(className="fas fa-users fa-3x mb-3 mt-3 text-primary"),
            html.H4("Clientes Activos", className="card-title"),
            html.H2(f"{active_clients:,}", className="card-text text-primary")
        ], className="text-center shadow"), md=3),
        dbc.Col(dbc.Card([
            html.I(className="fa-solid fa-building-columns fa-3x mb-3 mt-3 text-success"),
            html.H4("Adquirentes Activos", className="card-title"),
            html.H2(f"{active_aquirers:,}", className="card-text text-success")
        ], className="text-center shadow"), md=3),
        dbc.Col(dbc.Card([
            html.I(className="fa-solid fa-user-minus fa-3x mb-3 mt-3 text-info"),
            html.H4("Tasa de Churn", className="card-title"),
            html.H2(f"{churn_rate.iloc[0,2]/100:.2%}", className="card-text text-info")
        ], className="text-center shadow"), md=3),
        dbc.Col(dbc.Card([
            html.I(className="fa-solid fa-money-bill fa-3x mb-3 mt-3 text-warning"),
            html.H4("Volumen Transaccional", className="card-title"),
            html.H2(f"${vol_transaccional[0]:,.2f}")
        ], className="text-center shadow"), md=3),
    ], className="mb-4"),
    
    # Tabs
    dbc.Card([
        dbc.CardHeader(
            dbc.Tabs([
                dbc.Tab(label="General", tab_id="general",label_style={"color": colores['text']}),
                dbc.Tab(label="Clientes", tab_id="clients", label_style={"color": colores['text']}),
            ],
            id="tabs",
            active_tab="general",
            )
        ),
        dbc.CardBody(html.Div(id="tab-content", className="p-4"))
    ], className="shadow"),
    
], fluid=True, className="py-4", style={'backgroundColor': colores['background']})

def create_zone_business_treemap():
    # Create treemap
    fig = px.treemap(
        zona,
        path=['nombre_zona'],
        values='num_comercios',
        title='Numero de comercios por zona',
        hover_data=['id_zona']
    )
    fig.update_traces(textinfo="label+value")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return dcc.Graph(figure=fig)

def treemap_issuers():
    fig = px.treemap(
        issuer,
        path=['Banco'],
        values='Numero de Transacciones',
        title='Numero de Transacciones por banco',
        hover_data=[None]
    )
    fig.update_traces(textinfo="label+value")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return dcc.Graph(figure=fig)

def treemap_transacciones_merchant():
    fig = px.treemap(
        transacciones,
        path = ['Nombre de Comercio'],
        values = 'Monto Transaccionado',
        title = 'Monto Total Transaccionado por Comercio',
        hover_data=[None],
        color='Nombre de Comercio',
        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    )
    fig.update_traces(textinfo="label+value")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return dcc.Graph(figure=fig)

def pie_chart_debito_credito():
    fig = px.pie(
        tipo_tarjeta,
        values='Cantidad',
        names='Tipo de Tarjeta',
        hole=0,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title='Tipo de Tarjeta (Débito/Crédito)'
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        legend_title_text='Tipo de Trajeta',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return dcc.Graph(figure=fig)

def transacciones_en_el_tiempo():
    fig = px.line(
        transacciones_en_tiempo,
        x='Inicio de Semana', y='Total',
        title='Transacciones en el Tiempo',
        labels={'Inicio de Semana':'Semana','Total':'Total Transaccionado'},
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    return dcc.Graph(figure=fig)

def bar_chart_churn():
    fig = px.bar(
        clientes_churn,
        x='Nombre de Comercio', y='Dias desde última transacción',
        hover_data=['Nombre de Comercio', 'Fecha de última transacción'],
        labels={'Dias desde última transacción': 'Dias desde última transacción','Nombre de Comercio': 'Nombre de Comercio'},
        title='Días desde la última transacción por cliente'
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return dcc.Graph(figure=fig)

    
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "general":
        return(dbc.Row([
            dbc.Row([
                dbc.Col(create_zone_business_treemap(), width=12)
            ]),
            dbc.Row([
                dbc.Col(transacciones_en_el_tiempo(),width=12)
            ]),
            dbc.Row([
                dbc.Col(treemap_issuers(),width=12)
            ]),
        ]))
    elif active_tab == "clients":
        return dbc.Row([
            dbc.Row([
                dbc.Col(treemap_transacciones_merchant(),width=12)
            ]),
            dbc.Row([
                dbc.Col(bar_chart_churn(),width=12)
            ]),
            dbc.Row([
                dbc.Col(pie_chart_debito_credito(),width=12)
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Monto Total Transaccionado", className="card-title"),
                    html.H3(id="total-amount", className="card-text")
                    ])], className="mt-3"),
            dbc.Row([
                html.H3("Filtros", className="card-title")
            ]),
            dbc.Col(dcc.Dropdown(
                id='name-filter',
                options=[],
                value='',
                placeholder='Nombre del cliente',
                multi=False,
                searchable=True,
                clearable=True,
                style={'width': '100%'}
            ), md=12),
            dbc.Col(dcc.Dropdown(
                id='active-filter',
                placeholder='Estatus',
                options=[{'label':'Activo','value':'1'},
                         {'label':'Inactivo','value':'0'},],
                value='all',
                style={'width': '100%'}
            ), md=12),
            dbc.Col(dcc.Dropdown(
                id='year-filter',
                options=[{'label': year, 'value': year} for year in all_clients['Creado'].dt.year.unique()],
                value=None,
                placeholder='Año',
                clearable=True
            ), md=6),
            dbc.Col(dcc.Dropdown(
                id='mcc-filter',
                placeholder='MCC',
                options=[{'label':mcc, 'value':mcc} for mcc in all_clients['Familia MCC'].unique()],
                value='all',
                style={'width': '100%'}
            ), md=6),
            dbc.Col(dash_table.DataTable(id='filtered-table',style_cell={'textAlign': 'left'},style_header={'backgroundColor': 'rgb(143, 149, 139)','fontWeight': 'bold'}, style_data={'color': 'black','backgroundColor': 'rgb(222,220,220)'}), width=12),
        ])
    
# Callback para actualizar el search box del filtor de clientes
@app.callback(
    Output('name-filter', 'options'),
    Input('name-filter', 'search_value'),
    State('name-filter', 'value')
)
def update_name_options(search_value, current_value):
    if not search_value and not current_value:
        return []
    if current_value:
        filtered_names = all_clients[all_clients['Nombre de comercio'].str.contains(current_value, case=False)]['Nombre de comercio'].unique()
        options = [{'label': name, 'value': name} for name in filtered_names]
        if {'label': current_value, 'value': current_value} not in options:
            options.append({'label': current_value, 'value': current_value})
        return options
    filtered_names = all_clients[all_clients['Nombre de comercio'].str.contains(search_value, case=False)]['Nombre de comercio'].unique()
    return [{'label': name, 'value': name} for name in filtered_names]

#Callback para actualizar la datatable de los clientes
@app.callback(
    Output('filtered-table', 'data'),
    Input('name-filter', 'value'),
    Input('mcc-filter', 'value'),
    Input('active-filter', 'value'),
    Input('year-filter', 'value'),
)
def update_table(name, mcc, active, year):
    filtered_df = all_clients.copy()
    
    if name:
        filtered_df = filtered_df[filtered_df['Nombre de comercio'] == name]

    if mcc:
        filtered_df = filtered_df[filtered_df['Familia MCC'] == mcc]

    if active and active != 'all':
        filtered_df = filtered_df[filtered_df['Activo'] == int(active)]

    if year:
        filtered_df = filtered_df[
            (filtered_df['Creado'].dt.year == year) | (filtered_df['Creado'].dt.year == year)
        ]
    
    columnas_en_tabla = ['Nombre de comercio', 'Familia MCC']
    filtered_df = filtered_df[columnas_en_tabla]

    return filtered_df.to_dict('records')


@app.callback(
    Output("total-amount", "children"),
    [Input('name-filter', 'value'),
     Input('mcc-filter', 'value'),
     Input('active-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_total_amount(name, mcc, active, year):
    filtered_df = transacciones.copy()

    if name:
        filtered_df = filtered_df[filtered_df['Nombre de Comercio'] == name]
    if mcc:
        filtered_df = vol_transaccional_mcc.copy()
        filtered_df = filtered_df[filtered_df['MCC'] == mcc]
    if active and active != 'all':
        filtered_df = filtered_df[filtered_df['Activo'] == int(active)]
    if year:
        filtered_df = filtered_df[filtered_df['Creado'].dt.year == year]

    total_amount = filtered_df['Monto Transaccionado'].sum()
    return f"${total_amount:,.2f}"


if __name__ == '__main__':
    app.run_server(debug=False)