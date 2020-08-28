import pgeocode
import numpy as np
import sqlalchemy
import getpass
import pandas as pd
import os
import pickle
import shutil
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from argparse import ArgumentParser


DEFAULT_RANDOM_STATE = 312
DEFAULT_N_TREES = 30


def _create_model(train_x, train_y, test_x, test_y, random_state, n_trees=DEFAULT_N_TREES):
    # Fit random forest.
    rf = RandomForestRegressor(n_estimators=n_trees).fit(train_x, train_y)
    rf_prd = rf.predict(test_x)

    # Evaluate.
    metrics = {
        'rmse': -1,
        'mae': -1
    }

    metrics['rmse'] = np.sqrt(np.mean(test_y - rf_prd)**2)
    metrics['mae'] = np.mean(np.abs(test_y - rf_prd))

    return rf, metrics


def main(path, test_size=0.2, random_state=DEFAULT_RANDOM_STATE, n_trees=DEFAULT_N_TREES):
    # Configure DB
    config = {
        'host':'localhost',
        'user': 'root',
        'password': getpass.getpass('Enter the password: '),
        'db': 'livethere'
    }

    mysql_db_uri = f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["db"]}'
    engine = sqlalchemy.create_engine(mysql_db_uri)

    # Read Rentals table from sql server.
    print('Retrieving data from SQL Server...')
    df = pd.read_sql('SELECT * FROM Rental', con=engine)
    print(df.dtypes)

    print('Processing data...')
    # Format data type.     
    df['postalCode'] = df['postalCode'].apply(lambda a: a[:3] + " " + a[-3:]).astype(str)
    df['propertyType'] = df['propertyType'].astype(str)
    df['longitude'] = df['longitude'].astype(float)
    df['latitude'] = df['latitude'].astype(float)
    df['rentalPrice'] = df['rentalPrice'].astype(float)

    # Transform data.
    scaler = MinMaxScaler()
    property_one_hot = OneHotEncoder()
    county_one_hot = OneHotEncoder()
    
    # Normalize.
    x = scaler.fit_transform(df[['bathroomCount', 'bedroomCount']])

    # One-Hot encode property type.
    p = df['propertyType'].to_numpy().astype(str).reshape(-1, 1)
    p = property_one_hot.fit_transform(p).toarray()

    x = np.concatenate([x, p], axis=1)

    # Get counties
    nomi = pgeocode.Nominatim('ca')
    counties = nomi.query_postal_code(list(df['postalCode']))['county_name']

    # One-hot encode counties(location).
    c = counties.to_numpy().astype(str).reshape(-1, 1)
    c = county_one_hot.fit_transform(c).toarray()

    x = np.concatenate([x, c], axis=1)

    # Y = Rental Price
    y = df['rentalPrice']
    y = y.to_numpy()

    # Train-Test split.
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=test_size, shuffle=True, random_state=random_state)
    print('Data Shape: ', {
        'train_x': train_x.shape,
        'test_x': test_x.shape,
        'train_y': train_y.shape,
        'test_y': test_y.shape
    })

    # Log hyperparameters and settings.
    print(f'N trees: {n_trees}')
    print(f'Random State: {random_state}')

    # Create model.
    print('Training model...')
    rf, test_score = _create_model(train_x, train_y, test_x, test_y, random_state, n_trees)
    print(f'Test score: { test_score }')

    if input('Confirm saving model [y/n]') == 'y':
        # Remove dir if exists.
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

        # Save model.
        with open(os.path.join(path, 'model.pkl'), 'wb') as f:
            pickle.dump(rf, f)

        # Save preprocessing scalers.
        with open(os.path.join(path, 'property_one_hot.pkl'), 'wb') as f:
            pickle.dump(property_one_hot, f)

        # Save preprocessing scalers.
        with open(os.path.join(path, 'county_one_hot.pkl'), 'wb') as f:
            pickle.dump(county_one_hot, f)

        with open(os.path.join(path, 'normalization.pkl'), 'wb') as f:
            pickle.dump(scaler, f)
        
        print(f'Model saved at {path}')
    else:
        print('Saved cancelled.')


if __name__ == '__main__':
    # Parse Terminal Arguments. 
    parser = ArgumentParser(description='Create Random Forest models from Rental data from SQL server.')
    parser.add_argument('--tr', default=0.2, help='Test Ratio', type=float)
    parser.add_argument('--path', default=os.path.join(os.getcwd(), 'rental_rf'), help='Directory for saving model as pkl file.')
    parser.add_argument('--random', default=DEFAULT_RANDOM_STATE, type=int, help=f'Random State, default = {DEFAULT_RANDOM_STATE}.')
    parser.add_argument('--n_trees', default=DEFAULT_N_TREES, type=int, help=f'Random Forest Hyperparameter: number of decision trees, default = {DEFAULT_N_TREES}')
    args = vars(parser.parse_args())

    # Run main.
    main(path=args['path'], test_size=args['tr'], random_state=args['random'], n_trees=args['n_trees'])
    


