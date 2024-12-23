from flask import Flask, request, render_template, redirect, url_for
import requests
import csv
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Инициализация Flask и Dash приложений
app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')
dash_app.layout = html.Div()

# Конфигурация API
API_KEY = 'tl8vGNpMX0PmF29tIarSDJJwCseg0bZ8'
BASE_URL = 'http://dataservice.accuweather.com'


# Сохранение данных о погоде в CSV файл
def save_weather_data_to_csv(data_list, file_path, cities, coords):
    headers = ['City', 'Latitude', 'Longitude', 'Date', 'Avg Temp (C)', 'Wind Speed', 'Precipitation Probability']
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for i, data in enumerate(data_list):
            if not data['DailyForecasts']:
                continue
            for forecast in data['DailyForecasts']:  # Проходим по всем дням прогноза
                avg_temp_celsius = ((forecast['Temperature']['Minimum']['Value'] - 32) * 5 / 9 +
                                    (forecast['Temperature']['Maximum']['Value'] - 32) * 5 / 9) / 2
                writer.writerow({
                    'City': cities[i],
                    'Latitude': coords[i][0],
                    'Longitude': coords[i][1],
                    'Date': forecast['Date'],
                    'Avg Temp (C)': round(avg_temp_celsius, 1),
                    'Wind Speed': forecast['Day']['Wind']['Speed']['Value'],
                    'Precipitation Probability': forecast['Day']['PrecipitationProbability']
                })


# Получение ключа и координат города через API AccuWeather
def get_city_key_and_coords(city_name):
    response = requests.get(f"{BASE_URL}/locations/v1/cities/search", params={'q': city_name, 'apikey': API_KEY})
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["Key"], data[0]["GeoPosition"]["Latitude"], data[0]["GeoPosition"]["Longitude"]
    return None, None, None


# Получение данных о погоде
def get_weather_data(city, days):
    city_key, _, _ = get_city_key_and_coords(city)
    response = requests.get(f'{BASE_URL}/forecasts/v1/daily/{days}day/{city_key}',
                            params={'apikey': API_KEY, 'details': 'true'})
    return response.json() if response.status_code == 200 else None


# Обработка данных о погоде
def process_weather_data(start, end, intermediates, days):
    cities = [start] + intermediates + [end] if intermediates else [start, end]
    data_list, coords = [], []
    for city in cities:
        key, lat, lon = get_city_key_and_coords(city.strip())
        if key:
            data = get_weather_data(city.strip(), days)
            if data:
                data_list.append(data)
                coords.append((lat, lon))
    save_weather_data_to_csv(data_list, 'weather_forecast.csv', cities, coords)
    return data_list, cities, coords


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_city = request.form['start_city']
        end_city = request.form['end_city']
        intermediate_cities = request.form.getlist('intermediate_city')
        days = int(request.form['days'])

        # Обрабатываем данные о погоде
        data, cities, coords = process_weather_data(start_city, end_city, intermediate_cities, days)
        if data:
            return redirect('/dashboard/')
        return render_template('error.html', message="Ошибка получения данных о погоде.")
    return render_template('index.html')


# Интерфейс Dash для графиков и карты
dash_app.layout = html.Div([
    html.H1("Прогноз погоды по маршруту"),
    html.Div([
        html.Label("Выберите параметр для отображения графика:"),
        dcc.Dropdown(
            id='parameter-dropdown',
            options=[
                {'label': 'Средняя температура (°C)', 'value': 'Avg Temp (C)'},
                {'label': 'Скорость ветра (км/ч)', 'value': 'Wind Speed'},
                {'label': 'Вероятность осадков (%)', 'value': 'Precipitation Probability'}
            ],
            value='Avg Temp (C)'
        )
    ]),
    dcc.Graph(id='weather-graph'),
    dcc.Graph(id='route-map')
])


@dash_app.callback(
    [Output('route-map', 'figure'), Output('weather-graph', 'figure')],
    [Input('parameter-dropdown', 'value')]
)
def update_map_and_graph(selected_param):
    try:
        # Загружаем данные
        df = pd.read_csv('weather_forecast.csv')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)

        if df.empty:
            print("CSV файл пустой.")
            return {}, {}

        # Убираем дубликаты городов для карты
        df_unique = df.drop_duplicates(subset=['City'], keep='first')

        # Создаем карту
        route_fig = px.scatter_mapbox(
            df_unique,
            lat='Latitude',
            lon='Longitude',
            text=df_unique['City'] + '<br>Температура: ' + df_unique['Avg Temp (C)'].astype(str) + '°C',
            title='Маршрут с прогнозом погоды',
            mapbox_style="open-street-map"
        )

        # Добавляем линию маршрута
        route_fig.add_trace(go.Scattermapbox(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='lines',
            line=dict(width=2, color='blue'),
            name='Маршрут'
        ))

        # Центрирование карты
        route_fig.update_layout(
            mapbox=dict(
                zoom=3,
                center=dict(
                    lat=df_unique['Latitude'].mean(),
                    lon=df_unique['Longitude'].mean()
                )
            )
        )

        # Создаем график выбранного параметра
        weather_fig = go.Figure()
        for city in df['City'].unique():
            city_data = df[df['City'] == city]
            weather_fig.add_trace(go.Scatter(
                x=city_data['Date'],
                y=city_data[selected_param],
                mode='lines+markers',
                name=city
            ))
        weather_fig.update_layout(
            title=f'{selected_param} по маршруту',
            xaxis_title='Дата',
            yaxis_title=selected_param
        )

        return route_fig, weather_fig

    except Exception as e:
        print(f"Ошибка: {e}")
        return {}, {}


if __name__ == '__main__':
    app.run(debug=True)
