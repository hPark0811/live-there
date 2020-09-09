import os
import pickle
import numpy as np
import sklearn

DIR_PATH = os.path.dirname(__file__)
MODEL_PATH = os.path.join(DIR_PATH, 'pickles/model.pkl')
PROPERTY_ONE_HOT = os.path.join(DIR_PATH, 'pickles/property_one_hot.pkl')
COUNTY_ONE_HOT = os.path.join(DIR_PATH, 'pickles/county_one_hot.pkl')
NORMALIZE_SCALER = os.path.join(DIR_PATH, 'pickles/normalization.pkl')

initialized = False
_model = None
_property_one_hot = None
_county_one_hot = None
_normal_scaler = None


def init():
    global initialized
    if initialized:
        raise Warning('The module is already initialized.')
    else:
        initialized = True
        global _model, _property_one_hot, _county_one_hot, _normal_scaler

        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)

        # TODO: only single one hot enocoding.
        with open(PROPERTY_ONE_HOT, 'rb') as f:
            _property_one_hot = pickle.load(f)

        with open(COUNTY_ONE_HOT, 'rb') as f:
            _county_one_hot = pickle.load(f)

        with open(NORMALIZE_SCALER, 'rb') as f:
            _normal_scaler = pickle.load(f)


def predict(property_types, county_types, bed_counts, bath_counts):
    global initialized
    if not initialized:
        raise Exception('ml/rental module is not initialized.')
    
    valid_params = [
        isinstance(property_types, (list, np.ndarray, np.array)),
        isinstance(county_types, (list, np.ndarray, np.array)),
        isinstance(bath_counts, (list, np.ndarray, np.array)),
        isinstance(property_types, (list, np.ndarray, np.array)),
        len(bed_counts) == len(bath_counts),
        len(bed_counts) == len(property_types),
        len(bed_counts) == len(county_types),
    ]

    if not all(valid_params):
        raise ValueError("Invalid arguments")
    
    n_data = len(bed_counts) 
    
    features = np.stack([bed_counts, bath_counts]).T
    features = _normal_scaler.transform(features)

    p_sparse = _property_one_hot.transform(
        np.array(property_types).reshape(n_data, 1)).toarray()
    c_sparse = _county_one_hot.transform(
        np.array(county_types).reshape(n_data, 1)).toarray()
    
    x = np.concatenate([features, p_sparse, c_sparse], axis=1)

    prediction = _model.predict(x)
    
    return prediction.item() if n_data == 1 else prediction

if __name__ == '__main__':
    init()
    print(predict(['condo', 'condo', 'condo', 'condo'], ['Toronto', 'Toronto', 'Toronto', 'Toronto'], [1, 2, 1, 3], [1, 3, 2, 1]))
    from itertools import product
    a = [1, 2, 3, 4]
    b = [3, 2, 1]

    print(np.array(list(product(a, b, b.copy()))))
    



