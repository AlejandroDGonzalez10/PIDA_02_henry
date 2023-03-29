import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import yfinance as yf


def page_inicio():

    st.title('''Dashboard sobre el indice S&P500 ''')
    st.image('https://s.yimg.com/ny/api/res/1.2/NgGh9XXtdYa6yo4_Al2TpA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM2MA--/https://media.zenfs.com/en/gobankingrates_644/68d66d621e2a960154454e2caff2da12')
    st.subheader('Veremos un analisis sobre este indice bursatil y recomendaciones de inversiones.')

    st.subheader('INDICE S&P500 ')
    st.write('El S&P 500 es un índice bursátil que mide el rendimiento de 500 empresas líderes en los Estados Unidos, incluyendo algunas de las compañías más grandes y exitosas de EE.UU Como un indicador amplio del mercado de valores, fue creado en 1957.')
    st.write('El índice se calcula utilizando una metodología de capitalización de mercado, lo que significa que el valor de cada empresa en el índice se pondera en función de su capitalización bursátil total. Esto asegura que las empresas más grandes tengan un mayor impacto en el índice que las empresas más pequeñas.')
    st.write(' ** El S&P500 es uno de los mas importantes indices bursatiles pero no es el unico, tenemos tambien el NASDAQ 100, DOW JONES, entre otros. ** ')


    spx500=pd.read_csv('stock_price.csv')
    st.header('Este es un grafico lineal del indice donde podemos obsevar su comercio en los ultumos 23 años.')




    # Gráfico
    fig = px.line(spx500, x='Date', y='Adj Close',)
    # Personalizar el gráfico
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Cierre de Precio'
    )
    fig.update_traces(hovertemplate='Fecha: %{x} <br>Cierre de Precio: %{y}')
    fig.update_layout(title='Grafico del S&P 500')
    st.plotly_chart(fig)


    st.write('El S&P500 en su trayectoria en los 23 años tu tendencia alcista con un crecimiento del 865%, desde el 2000 a la actualidad.')
    #----------------------------------------------------------------------------------------------------------
    # Logica del codigo.
    st.header('Este es un grafico de barras donde vemos el retorno anual del indice a lo largo de los años.')
    st.write('Cada barra es el retorno de ese año, las barras por debajo del cero son negativas para ese año y las barras por arriba del cero son positivas para dicho año.')

    df=spx500
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    # Calcular los retornos diarios del S&P 500
    spx500['Daily Return'] = spx500['Adj Close'].pct_change()
    # Agrupar los retornos por año y calcular el retorno anual del S&P 500
    annual_returns = spx500['Daily Return'].groupby(pd.Grouper(freq='Y')).apply(lambda x: (1+x).prod()-1)


    # Grafico
    fig = px.bar(x=annual_returns.index.year, y=annual_returns, labels={'x': 'Año', 'y': 'Retorno Anual'})
    # Personalizar el gráfico de barras
    fig.update_layout(title='Retorno Anual del S&P 500', xaxis_tickangle=-45)
    # Mostrar el gráfico de barras en Streamlit
    st.plotly_chart(fig)


    #--------------------------------------------------------------------------------------------------------
    # Logica del codigo.
    st.header('Retornos por año positivos y negativos')

    df['daily_return'] = df['Adj Close'].pct_change()
    df = df.reset_index()
    negative_returns = df[df['daily_return'] < 0]['daily_return'].groupby(df['Date'].dt.year).mean() * 252
    positive_returns = df[df['daily_return'] >= 0]['daily_return'].groupby(df['Date'].dt.year).mean() * 252

    # Grafico
    fig = go.Figure()
    fig.add_trace(go.Bar(x=negative_returns.index, y=negative_returns, name='Retornos Negativos', marker_color='red'))
    fig.add_trace(go.Bar(x=positive_returns.index, y=positive_returns, name='Retornos Positivos', marker_color='green'))
    fig.update_layout(title='Retornos Diarios por año', xaxis_title='Año', yaxis_title='Retorno Anual')
    st.plotly_chart(fig)

    #----------------------------------------------------------------------------------------------------------- 
    # Logica del codigo.
    st.header('Suma de retornos positivos y negativos en los 23 años')

    spx500_df=pd.read_csv('stock_price.csv')
    spx500_df['Date'] = pd.to_datetime(spx500_df['Date'])
    spx500_df.set_index('Date', inplace=True)
    # Calcular el rendimiento diario
    spx500_df['Daily Return'] = spx500_df['Adj Close'].pct_change()
    # Agrupar los datos por año y calcular el rendimiento anual
    annual_returns = spx500_df['Daily Return']*100
    annual_returns = spx500_df['Daily Return'].groupby(pd.Grouper(freq='Y')).apply(lambda x: (1 + x).prod() - 1)
    # Convertir annual_returns en un DataFrame
    annual_returns_df = pd.DataFrame(annual_returns)
    # Agregar una columna con el año correspondiente a cada rendimiento anual
    annual_returns_df['Year'] = annual_returns.index.year
    annual_returns_df.rename(columns={'Daily Return': 'Anual Return'}, inplace=True)
    annual_returns = annual_returns_df['Anual Return'].groupby(annual_returns_df.index.year).sum()
    # Obtener la suma de los rendimientos anuales positivos y negativos
    positive_returns_sum = annual_returns[annual_returns > 0].sum()
    negative_returns_sum = annual_returns[annual_returns < 0].sum()


    st.subheader('Suma de los rendimientos anuales positivos:')
    st.header('286.863 %')
    st.subheader('Suma de los rendimientos anuales negativos:')
    st.header('-101.73%')
    #Grafico

    # Crear un DataFrame para los datos del gráfico de torta
    pie_data = pd.DataFrame({'Tipo de retorno': ['Retornos Positivos', 'Retornos Negativos'],
                            'Retorno acumulado': [positive_returns_sum, abs(negative_returns_sum)]})
    # Crear el gráfico de torta
    fig = go.Figure(data=[go.Pie(labels=pie_data['Tipo de retorno'], 
                                hole=0.4,
                                values=pie_data['Retorno acumulado'],
                                marker_colors=['green', 'red'])])
    # Personalizar la figura
    fig.update_layout(title={'text': 'Retornos Anuales del S&P500 desde el año 2000 calculado en un 100%','y': 0.95,'x': 0.5,'xanchor': 'center','yanchor': 'top'},
        width=800,
        height=600,
        template='simple_white')
    # Mostrar la figura en Streamlit
    st.plotly_chart(fig)

    st.header('Rendimiento promedio anualizado del S&P 500 desde el año 2000 hasta la actualidad: ')
    st.title('6.34% ')




def page_sectores():
    st.title('Sectores del S&P500')
    st.subheader('Sectores que integran el indice S&P500')
    st.subheader('S&P500 se divide en sectores:'
            '\n- XLC: Comunicaciones'
            '\n- XLY: Consumo discrecional'
            '\n- XLP: Bienes de consumo no cíclico'
            '\n- XLE: Energía'
            '\n- XLF: Financiero'
            '\n- XLV: Cuidado de la salud'
            '\n- XLI: Industrial'
            '\n- XLK: Tecnología'
            '\n- XLB: Materiales'
            '\n- XLU: Servicios públicos')

    st.header('Catidad de empresas por sector')
    sector=pd.read_csv('areas_sec.csv')
    sectores = sector['Sector'].value_counts()
    count_by_sector = sector.groupby('Sector')['Simbolo'].count()
    fig = px.bar(sectores, x=sectores.index, y=sectores.values)
    fig.update_traces(hovertemplate='<b>Sector: %{x}</b><br>Cantidad: %{y}')
    fig.update_layout(xaxis={'title': 'Sector'},
                    yaxis={'title': 'Frecuencia numero de empresas de cada sector'},
                    title='Distribución de sectores del SP500',
                    height=500, width=800)
    st.plotly_chart(fig)



    sectors_data=pd.read_csv('sectoresspy.csv')
    sectors_data.set_index('Date', inplace=True)
    sectors_names = {'XLY': 'Consumo discrecional', 
                 'XLP': 'Bienes de consumo básicos', 
                 'XLE': 'Energía', 
                 'XLF': 'Servicios financieros', 
                 'XLV': 'Salud', 
                 'XLI': 'Industriales', 
                 'XLB': 'Materiales', 
                 'XLRE': 'Inmobiliario', 
                 'XLK': 'Tecnología', 
                 'XLC': 'Comunicaciones',
                }
    sectors_data.columns = sectors_data.columns.map(sectors_names)
    sectors_data = sectors_data.dropna()

    st.header('Profit de sectores durante promedio desde el 2000 hasta la actualidad')
    
    # Calcular las ganancias de cada sector
    sector_gains = {}
    for sector in sectors_data.columns:
        start_value = sectors_data[sector][0]
        end_value = sectors_data[sector][-1]
        sector_gains[sector] = (end_value / start_value - 1) * 100

    gains_df = pd.DataFrame(sector_gains.items(), columns=['Sector', 'Profit'])
    # Ordenar los sectores por ganancia descendente
    gains_df = gains_df.sort_values('Profit', ascending=False)
    gains_df.set_index('Sector', inplace=True)
    st.table(gains_df)

    # Crear el gráfico de barras
    fig = px.bar(gains_df, y=gains_df.index, x='Profit', 
                color='Profit', color_continuous_scale='Blues',
                color_continuous_midpoint=45, text='Profit',
                category_orders={'Sector': gains_df.index})

    # Personalizar el gráfico
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='auto', 
                    hovertemplate='Ganancia: %{y:.2f}%<extra></extra>')
    fig.update_layout(xaxis={'title': 'Sector'},
                    yaxis={'title': 'Ganancia (%)'},
                    title='Ganancias de los sectores del SPY500 desde el año 2000',
                    height=500, width=900)

    st.header('Grafico Porcentual de las ganancias promedio por sector desde el 2000.')
    # Mostrar el gráfico
    st.plotly_chart(fig)




    # Obtener los nombres de los sectores
    sectors = sectors_data.columns.tolist()
    # Crear una lista de subplots con 6 filas y 2 columnas
    fig = make_subplots(rows=6, cols=2, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=sectors)
    # Iterar por los nombres de los sectores y agregar los trazados a los subplots
    for i, sector in enumerate(sectors):
        # Obtener los datos del sector
        sector_data = sectors_data[sector]
                # Agregar un trazado de líneas al subplot correspondiente
        fig.add_trace(go.Scatter(x=sector_data.index, y=sector_data, mode='lines', line=dict(color='blue')), row=i//2+1, col=i%2+1)
                # Establecer las etiquetas del eje X y el título del subplot
        fig.update_xaxes(title_text='Fecha', dtick='M12', row=i//2+1, col=i%2+1, tickformat='%Y')
        fig.update_yaxes(title_text='Precio (USD)', row=i//2+1, col=i%2+1)
        # Establecer el tamaño del gráfico y el título principal
    fig.update_layout(height=1300, width=950, title='Precios de los sectores del S&P500')
    # Mostrar el gráfico
    st.header('Grafico de los sectores durante los ultimos 23 años.')
    st.plotly_chart(fig)




def page_empresas():
    st.title('Empresas Recomendadas')
    st.header('Empresas elegidas para invertir')
    st.subheader('Top 10 Empresas del sector Tecnologico y S&P500 en general con mayor rendimientos en 23 años:')
    data_tec = {
    'Empresa': ['AAPL', 'ANSS', 'CTSH', 'APH', 'LRCX', 'ADBE', 'TYL', 'QCOM', 'FICO', 'ROP'],
    'Rendimiento': [51021.26, 11445.60, 10018.50, 9448.09, 8971.02, 5963.59, 5391.33, 5363.42, 5127.35, 5017.41]
    }
    df_tec = pd.DataFrame(data_tec)

    # Datos para la tabla de S&P500
    data_sp500 = {
        'Empresa': ['MNST', 'AAPL', 'ODFL', 'TSCO', 'POOL', 'CPRT', 'NVR', 'ANSS', 'ATVI', 'REGN'],
        'Rendimiento': [93939.42, 51021.26, 33322.46, 20070.57, 14525.65, 11672.15, 11447.73, 11445.60, 10403.36, 10230.71]
    }
    df_sp500 = pd.DataFrame(data_sp500)

    # Dividir la página en dos columnas
    col1, col2 = st.columns(2)

    # Mostrar la tabla de tecnología en la primera columna
    with col1:
        st.write('Empresas Tecnología')
        st.table(df_tec)

    # Mostrar la tabla de S&P500 en la segunda columna
    with col2:
        st.write('Empresas S&P500')
        st.table(df_sp500)


    df=pd.read_csv('adjcierrestoks.csv')
    df.set_index('Date', inplace=True)
    columnas=['AAPL', 'ACN', 'ADBE', 'ADI', 'ADSK', 'AKAM', 'AMAT', 'AMD', 'ANET', 'ANSS', 'APH', 'AVGO', 'CDAY', 'CDNS', 'CDW', 'CRM', 'CSCO', 'CTSH', 'DXC', 'ENPH', 'EPAM', 'FFIV', 'FICO', 'FSLR', 'FTNT', 'GEN', 'GLW', 'HPE', 'HPQ', 'IBM', 'INTC', 'INTU', 'IT', 'JNPR', 'KEYS', 'KLAC', 'LRCX', 'MCHP', 'MPWR', 'MSFT', 'MSI', 'MU', 'NOW', 'NTAP', 'NVDA', 'NXPI', 'ON', 'ORCL', 'PAYC', 'PTC', 'QCOM', 'QRVO', 'ROP', 'SEDG', 'SNPS', 'STX', 'SWKS', 'TDY', 'TEL', 'TER', 'TRMB', 'TXN', 'TYL', 'VRSN', 'WDC', 'ZBRA']
    colempresa=df.loc[:,columnas]
    gains = ((colempresa.iloc[-1] - colempresa.iloc[0]) / colempresa.iloc[0]) * 100
    top_10tec = gains.nlargest(10)

    st.header ('Retornos anuales de top 10 empresas tecnologica ')
    # Crear el gráfico de barras
    fig = px.bar(top_10tec, y=top_10tec.values, x=top_10tec.index, 
                color=top_10tec.values, color_continuous_scale='Blues',
                color_continuous_midpoint=top_10tec.values.mean(),
                )

    # Personalizar el gráfico
    fig.update_traces( textposition='auto', 
                    hovertemplate='Ganancia: %{y:.2f}%<extra></extra>')
    fig.update_layout(xaxis={'title': 'Empresa'},
                    yaxis={'title': 'Ganancia (%)', },
                    title='Retorno anual por empresa del sector tecnológico del SPY500',
                    height=500, width=900) 
    st.plotly_chart(fig)

    #SPY500
    gains = ((df.iloc[-1] - df.iloc[0]) / df.iloc[0]) * 100
    # Encontrar las 10 empresas con las mayores ganancias
    top_10indice = gains.nlargest(10)
    #grafico de barras empresas de SPY500
    fig = px.bar(top_10indice, y=top_10indice.values, x=top_10indice.index, 
                color=top_10indice.values, color_continuous_scale='Greens',
                color_continuous_midpoint=top_10indice.values.mean(),
                )

    st.header ('Retornos anuales de top 10 empresas en general del S&P500 ')

    # Personalizar el gráfico
    fig.update_traces( textposition='auto', 
                    hovertemplate='Ganancia: %{y:.2f}%<extra></extra>')
    fig.update_layout(xaxis={'title': 'Empresa'},
                    yaxis={'title': 'Ganancia (%)', },
                    title='Las 10 empresas con mayores ganancias',
                    height=500, width=900)
    st.plotly_chart(fig)


    st.title('Datos importantes de las empresas Selecionadas ')

    # Crear un DataFrame con los datos
    data = {
        'Empresa': ['AAPL', 'ANSS', 'CTSH', 'MNST'],
        'Capitalización bursátil': ['2.494 T', '27.658 B', '30.023 B', '63.913 B'],
        'Promedio Volumen': ['69,639,145', '510,711', '4,768,111', '4,046,628'],
        'Proyección de dividendo y rentabilidad': ['0.92 (0.58%)', '0.80 (0.58%)', '1.16 (1.97%)', '0.92 (1.58%)']
    }
    df_f = pd.DataFrame(data)

    # Mostrar la tabla en Streamlit
    st.table(df_f)

    datos_empresa = df[['AAPL', 'ANSS', 'CTSH', 'MNST']]
    sectors = datos_empresa.columns.tolist()
    # Crear una lista de subplots con 6 filas y 2 columnas
    fig = make_subplots(rows=6, cols=2, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=sectors)

    # Iterar por los nombres de los sectores y agregar los trazados a los subplots
    for i, sector in enumerate(sectors):
        # Obtener los datos del sector
        sector_data = datos_empresa[sector]
        
        # Agregar un trazado de líneas al subplot correspondiente
        fig.add_trace(go.Scatter(x=sector_data.index, y=sector_data, mode='lines', line=dict(color='blue')), row=i//2+1, col=i%2+1)
        
        # Establecer las etiquetas del eje X y el título del subplot
        fig.update_xaxes(title_text='Fecha', dtick='M12', row=i//2+1, col=i%2+1, tickformat='%Y')
        fig.update_yaxes(title_text='Precio (USD)', row=i//2+1, col=i%2+1)
    
    # Establecer el tamaño del gráfico y el título principal
    fig.update_layout(height=1300, width=900, title='Precios de las empresas recomendadas')

    st.title('Grafico de precios de los 23 años de las empresas seleccionadas')
    # Mostrar el gráfico
    st.plotly_chart(fig)




 #--------------------------------KPIS 1 AAPLE -----------------------------------------------   

def page_kpis():
    st.title('Analisis KPIS Margen de beneficio')
    st.header(' Este Kpis nos sirve para tener un concepto mas claro del margen que podemos obtener con estas empresas recomendadas')
    # Descargar datos históricos de precios de AAPL desde Yahoo Finance
    df = yf.download('AAPL', start='2010-01-01', end='2023-03-27')

   # Agregar una columna para el Margen de Beneficio
    df['Margen de Beneficio'] = (df['Adj Close'] - df['Low']) / df['Adj Close']

    # Crear el dashboard utilizando Streamlit
    st.title(' Margen de Beneficio para AAPL - ANSS - CTSH - MNST')
    st.subheader('Datos de Cotización AAPL')

    # Gráfico de cotización de AAPL
    st.line_chart(df['Adj Close'])

    # Estadísticas de Margen de Beneficio
    st.subheader('Estadísticas de Margen de Beneficio desde el 2010')
    st.write('Margen de Beneficio Promedio:', round(df['Margen de Beneficio'].mean(), 2))
    st.write('Margen de Beneficio Máximo:', round(df['Margen de Beneficio'].max(), 2))
    st.write('Margen de Beneficio Mínimo:', round(df['Margen de Beneficio'].min(), 2))

    # Gráfico de Margen de Beneficio
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Margen de Beneficio'], mode='lines', line=dict(color='green')))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)

#---------------------------------KPIS 1 ANSS----------------------------------------------
    df_a = yf.download('ANSS', start='2010-01-01', end='2023-03-27')

   # Agregar una columna para el Margen de Beneficio
    df_a['Margen de Beneficio'] = (df['Adj Close'] - df_a['Low']) / df_a['Adj Close']

    st.subheader('Datos de Cotización ANSS')
    # Gráfico de cotización de AAPL
    st.line_chart(df_a['Adj Close'])

    # Estadísticas de Margen de Beneficio
    st.subheader('Estadísticas de Margen de Beneficio desde el 2010')
    st.write('Margen de Beneficio Promedio:', round(df_a['Margen de Beneficio'].mean(), 2))
    st.write('Margen de Beneficio Máximo:', round(df_a['Margen de Beneficio'].max(), 2))
    st.write('Margen de Beneficio Mínimo:', round(df_a['Margen de Beneficio'].min(), 2))

    # Gráfico de Margen de Beneficio
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_a.index, y=df_a['Margen de Beneficio'], mode='lines', line=dict(color='green')))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)

#-----------------------------------KPIS 1 CTSH---------------------------------------------------------

    df_e = yf.download('CTSH', start='2010-01-01', end='2023-03-27')

   # Agregar una columna para el Margen de Beneficio
    df_e['Margen de Beneficio'] = (df_e['Adj Close'] - df_e['Low']) / df_e['Adj Close']

    st.subheader('Datos de Cotización CTSH')
    # Gráfico de cotización de AAPL
    st.line_chart(df_e['Adj Close'])

    # Estadísticas de Margen de Beneficio
    st.subheader('Estadísticas de Margen de Beneficio desde el 2010')
    st.write('Margen de Beneficio Promedio:', round(df_e['Margen de Beneficio'].mean(), 2))
    st.write('Margen de Beneficio Máximo:', round(df_e['Margen de Beneficio'].max(), 2))
    st.write('Margen de Beneficio Mínimo:', round(df_e['Margen de Beneficio'].min(), 2))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_e.index, y=df_e['Margen de Beneficio'], mode='lines', line=dict(color='green')))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)

#-----------------------------------KPIS 1 MSNT------------------------------------------------------

    df_i = yf.download('MNST', start='2010-01-01', end='2023-03-27')

   # Agregar una columna para el Margen de Beneficio
    df_i['Margen de Beneficio'] = (df_i['Adj Close'] - df_i['Low']) / df_i['Adj Close']

    st.subheader('Datos de Cotización MNST')
    # Gráfico de cotización de AAPL
    st.line_chart(df_i['Adj Close'])

    # Estadísticas de Margen de Beneficio
    st.subheader('Estadísticas de Margen de Beneficio desde el 2010')
    st.write('Margen de Beneficio Promedio:', round(df_i['Margen de Beneficio'].mean(), 2))
    st.write('Margen de Beneficio Máximo:', round(df_i['Margen de Beneficio'].max(), 2))
    st.write('Margen de Beneficio Mínimo:', round(df_i['Margen de Beneficio'].min(), 2))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_i.index, y=df_i['Margen de Beneficio'], mode='lines', line=dict(color='green')))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


#----------------------------------KPIS 2 AAPL ----------------------------------------------------------
    st.title('Analisis KPIS BETA')
    st.header(' Este Kpis nos sirve medir o ver mejor el nivel de riesgo que puede tener invertir en cada enpresa por su relacion con la volatilidad del mercado, en este caso las 4 son moderadas con riesgo bajos.')


   # Descargar datos históricos de AAPL
    aapl = yf.download('AAPL', start='2010-01-01')

    # Calcular Beta utilizando el S&P 500 como índice de referencia
    spy = yf.download('^GSPC', start='2010-01-01')
    aapl_beta = pd.DataFrame({'AAPL': aapl['Adj Close'], 'SPY': spy['Adj Close']})
    cov = aapl_beta.cov()
    beta = cov.iloc[0, 1] / cov.iloc[1, 1]

    # Crear un gráfico de la acción de AAPL con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=aapl.index, y=aapl['Adj Close'], name='Precio ajustado'))
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Precio ajustado')

    # Crear un dashboard en Streamlit
    st.title('Análisis de AAPL')
    st.write('Tenemos un BETA bajo es decir que su volatilidad en relacion con el S&P500 es moderada baja lo que es ideal para reducir el riesgo del portafolio recomendado.')
    st.header('Beta (mensual por 5 años)	1.30')
    st.header(f'Beta promedio 23 años: {beta:.2f}')
    st.plotly_chart(fig)

#-------------------------------------KPIS 2 ANSS--------------------------------------------------------
      
    anss = yf.download('ANSS', start='2010-01-01')
    # Calcular Beta utilizando el S&P 500 como índice de referencia
    aapl_beta = pd.DataFrame({'ANSS': anss['Adj Close'], 'SPY': spy['Adj Close']})
    cov = aapl_beta.cov()
    beta = cov.iloc[0, 1] / cov.iloc[1, 1]

    # Crear un gráfico de la acción de AAPL con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=anss.index, y=anss['Adj Close'], name='Precio ajustado'))
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Precio ajustado')

    # Crear un dashboard en Streamlit
    st.title('Análisis de ANSS')
    st.write('Tenemos un BETA bajo es decir que su volatilidad en relacion con el S&P500 en moderada baja lo que es ideal para reducir el riesgo del portafolio recomendado.')
    st.header('Beta (mensual por 5 años)	1.24')
    st.header(f'Beta promedio 23 años: {beta:.2f}')
    st.plotly_chart(fig)


#-----------------------------------------KPIS 2 CTSH-------------------------------------------------
    ctsh = yf.download('CTSH', start='2010-01-01')
    # Calcular Beta utilizando el S&P 500 como índice de referencia
    aapl_beta = pd.DataFrame({'CTSH': ctsh['Adj Close'], 'SPY': spy['Adj Close']})
    cov = aapl_beta.cov()
    beta = cov.iloc[0, 1] / cov.iloc[1, 1]

    # Crear un gráfico de la acción de AAPL con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ctsh.index, y=ctsh['Adj Close'], name='Precio ajustado'))
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Precio ajustado')

    # Crear un dashboard en Streamlit
    st.title('Análisis de CTSH')
    st.write('Tenemos un BETA bajo es decir que su volatilidad en relacion con el S&P500 en moderada baja lo que es ideal para reducir el riesgo del portafolio recomendado.')
    st.header('Beta (mensual por 5 años)	1.11')
    st.header(f'Beta promedio 23 años: {beta:.2f}')
    st.plotly_chart(fig)


#--------------------------------------KPIS 2 MSNT--------------------------------------------------
    mnst = yf.download('MNST', start='2010-01-01')
    # Calcular Beta utilizando el S&P 500 como índice de referencia
    aapl_beta = pd.DataFrame({'MNST': mnst['Adj Close'], 'SPY': spy['Adj Close']})
    cov = aapl_beta.cov()
    beta = cov.iloc[0, 1] / cov.iloc[1, 1]

    # Crear un gráfico de la acción de AAPL con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mnst.index, y=mnst['Adj Close'], name='Precio ajustado'))
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Precio ajustado')

    # Crear un dashboard en Streamlit
    st.title('Análisis de MNST')
    st.write('Tenemos un BETA bajo es decir que su volatilidad en relacion con el S&P500 en moderada baja lo que es ideal para reducir el riesgo del portafolio recomendado.')
    st.header('Beta (mensual por 5 años)	0.87')
    st.header(f'Beta promedio 23 años: {beta:.2f}')
    st.plotly_chart(fig)

#----------------------------- kPIS 3 AAPL--------------------------------------------------
    
    st.title('Analisis KPIS Dividendo pagados')
    st.header(' Este Kpis nos muestra los dividendo pagados por las empresas en un calculo por cierres de precios de los activos')
    # Calcular el dividendo pagado
    aapl["Dividend Paid"] = aapl["Close"].diff() + aapl["Adj Close"].diff()
    aapl["Dividend Paid"] = aapl["Dividend Paid"].apply(lambda x: x if x > 0 else 0)
    # Crear una tabla de resumen con los KPIs de Dividendos pagados
    dividend_summary = pd.DataFrame({
        "Total Dividends Paid": aapl["Dividend Paid"].sum(),
        "Average Dividend Per Share": aapl["Dividend Paid"].sum() / len(aapl),
        "Dividend Yield": aapl["Dividend Paid"].sum() / aapl["Close"].mean(),
        "Dividend Payout Ratio": aapl["Dividend Paid"].sum() / aapl["Adj Close"].sum()
    }, index=[0])

    # Mostrar la tabla de resumen en el dashboard
    st.write("## Dividendos pagados (KPIs) de AAPL")
    st.write("Última rentabilidad de dividendos anuales 0.57%")
    st.write('Proyección de dividendo y rentabilidad	0.92 (0.58%)')
    st.write(dividend_summary)

    # Crear una gráfica de línea para visualizar los dividendos pagados
    dividend_chart = go.Figure()
    dividend_chart.add_trace(go.Scatter(x=aapl.index, y=aapl["Dividend Paid"], name="Dividendos pagados"))
    dividend_chart.update_layout(title="Dividendos pagados", xaxis_title="Fecha", yaxis_title="Dividendos (USD)")
    st.plotly_chart(dividend_chart)


#----------------------------- kPIS 3 ANSS--------------------------------------------------
  # Calcular el dividendo pagado
    aapl["Dividend Paid"] = aapl["Close"].diff() + aapl["Adj Close"].diff()
    aapl["Dividend Paid"] = aapl["Dividend Paid"].apply(lambda x: x if x > 0 else 0)
    # Crear una tabla de resumen con los KPIs de Dividendos pagados
    dividend_summary = pd.DataFrame({
        "Total Dividends Paid": aapl["Dividend Paid"].sum(),
        "Average Dividend Per Share": aapl["Dividend Paid"].sum() / len(aapl),
        "Dividend Yield": aapl["Dividend Paid"].sum() / aapl["Close"].mean(),
        "Dividend Payout Ratio": aapl["Dividend Paid"].sum() / aapl["Adj Close"].sum()
    }, index=[0])

    # Mostrar la tabla de resumen en el dashboard
    st.write("## Dividendos pagados (KPIs) de ANSS")
    st.write(dividend_summary)

    # Crear una gráfica de línea para visualizar los dividendos pagados
    dividend_chart = go.Figure()
    dividend_chart.add_trace(go.Scatter(x=aapl.index, y=aapl["Dividend Paid"], name="Dividendos pagados"))
    dividend_chart.update_layout(title="Dividendos pagados", xaxis_title="Fecha", yaxis_title="Dividendos (USD)")
    st.plotly_chart(dividend_chart)
    
    
#----------------------------- kPIS 3 CTSH--------------------------------------------------

# Calcular el dividendo pagado
    aapl["Dividend Paid"] = aapl["Close"].diff() + aapl["Adj Close"].diff()
    aapl["Dividend Paid"] = aapl["Dividend Paid"].apply(lambda x: x if x > 0 else 0)
    # Crear una tabla de resumen con los KPIs de Dividendos pagados
    dividend_summary = pd.DataFrame({
        "Total Dividends Paid": aapl["Dividend Paid"].sum(),
        "Average Dividend Per Share": aapl["Dividend Paid"].sum() / len(aapl),
        "Dividend Yield": aapl["Dividend Paid"].sum() / aapl["Close"].mean(),
        "Dividend Payout Ratio": aapl["Dividend Paid"].sum() / aapl["Adj Close"].sum()
    }, index=[0])

    # Mostrar la tabla de resumen en el dashboard
    st.write("## Dividendos pagados (KPIs) de CTSH")
    st.write(dividend_summary)

    # Crear una gráfica de línea para visualizar los dividendos pagados
    dividend_chart = go.Figure()
    dividend_chart.add_trace(go.Scatter(x=aapl.index, y=aapl["Dividend Paid"], name="Dividendos pagados"))
    dividend_chart.update_layout(title="Dividendos pagados", xaxis_title="Fecha", yaxis_title="Dividendos (USD)")
    st.plotly_chart(dividend_chart)
    

#----------------------------- kPIS 3 MNST--------------------------------------------------

# Calcular el dividendo pagado
    aapl["Dividend Paid"] = aapl["Close"].diff() + aapl["Adj Close"].diff()
    aapl["Dividend Paid"] = aapl["Dividend Paid"].apply(lambda x: x if x > 0 else 0)
    # Crear una tabla de resumen con los KPIs de Dividendos pagados
    dividend_summary = pd.DataFrame({
        "Total Dividends Paid": aapl["Dividend Paid"].sum(),
        "Average Dividend Per Share": aapl["Dividend Paid"].sum() / len(aapl),
        "Dividend Yield": aapl["Dividend Paid"].sum() / aapl["Close"].mean(),
        "Dividend Payout Ratio": aapl["Dividend Paid"].sum() / aapl["Adj Close"].sum()
    }, index=[0])

    # Mostrar la tabla de resumen en el dashboard
    st.write("## Dividendos pagados (KPIs) de MNST")
    st.write(dividend_summary)

    # Crear una gráfica de línea para visualizar los dividendos pagados
    dividend_chart = go.Figure()
    dividend_chart.add_trace(go.Scatter(x=aapl.index, y=aapl["Dividend Paid"], name="Dividendos pagados"))
    dividend_chart.update_layout(title="Dividendos pagados", xaxis_title="Fecha", yaxis_title="Dividendos (USD)")
    st.plotly_chart(dividend_chart)

def page_conclusion():
    st.header('El equipo de analisis y finanza concluyo que lo  mejor para la empresa es recomendar diversificar su portafolio de inversiones en 5 activos siendo el principal el indice S&P500 con un rendimiento anual promedio del 8%, segun los ultimos años, y en 4 empresas que mas alla que corresponden tambien al S&P500 se analizo que son de alto rendimiento con bajo nivel de riesgo esto hace un equilibrio perfecto para el crecimiento de capital invertido sin tanta especulacion de sus rendimientos anuales y poder calcular y proyectar un ibjetivo de retorno o ganancias.')
    
    
    st.header ('La recomendacion del equipo es que la inversion sea de minimo 5 año para poder obetner un total del 15%, anual promediando todos los activos juntos')

 
# Crear un cuadro de selección con varias opciones
opciones = ["S&P500", "Sectores del S&P500", "Empresas recomendadas", "Kpis"]

# Crea una lista de páginas
pages = {
    "S&P500": page_inicio,
    "Sectores del S&P500": page_sectores,
    "Empresas recomendadas": page_empresas,
    'KPIS': page_kpis,
}

# Crea un panel de opciones para navegar por las páginas
st.sidebar.title("Seleccion para Analisis")
selection = st.sidebar.radio("Seleccione page", list(pages.keys()))

# Muestra la página seleccionada
page = pages[selection]
page()