import pandas as pd
from .humidity.humidity import create_humidity_model
from .wind_speed.wind_speed import create_wind_speed_model
from .pressure.pressure import create_pressure_model
from .temp.temp import create_temp_min_model
from .temp.temp import create_temp_max_model
from .temp.temp import create_temp_model

PRODUCTS = ['humidity', 'pressure', 'temp', 'temp_min', 'temp_max', 'wind_speed']

def create_products_models(city_name, test_size):
    df = pd.read_csv(f'city_weather_datasets/{city_name}/{city_name}.csv')

    for product in PRODUCTS:

        df = df.rename(columns={'timestamp': 'ds', product: 'y'})
        df['ds'] = pd.to_datetime(df['ds'], unit='s')

        filename = f'city_weather_models/{city_name}/{product}.pkl'

        match product:
            case 'humidity':
                create_humidity_model(df, test_size, filename)
            case 'wind_speed':
                create_wind_speed_model(df, test_size, filename)
            case 'pressure':
                create_pressure_model(df, test_size, filename)
            case 'temp_min':
                create_temp_min_model(df, test_size, filename)
            case 'temp_max':
                create_temp_max_model(df, test_size, filename)
            case 'temp':
                create_temp_model(df, test_size, filename)
        
        df = df.rename(columns={'timestamp': 'ds', 'y': product})


