"""
Note this file contains _NO_ flask functionality.
Instead it makes a file that takes the input dictionary Flask gives us,
and returns the desired result.

This allows us to test if our modeling is working, without having to worry
about whether Flask is working. A short check is run at the bottom of the file.
"""

import pickle
import numpy as np
from sklearn.externals import joblib

# lr_model is our simple logistic regression model
# lr_model.feature_names are the four different iris measurements
lr_model = joblib.load('/Users/randy/Documents/GitHub/Twitch_Chat_Harassment/notebooks/twitch_models.p')
feature_names = lr_model.keys()


# with open("static/models/lr.pkl", "rb") as f:
#     lr_model = pickle.load(f)
#
# feature_names = lr_model.feature_names


def make_prediction(feature_dict):
    """
    Input:
    feature_dict: a dictionary of the form {"feature_name": "value"}

    Function makes sure the features are fed to the model in the same order the
    model expects them.

    Output:
    Returns (x_inputs, probs) where
      x_inputs: a list of feature values in the order they appear in the model
      probs: a list of dictionaries with keys 'name', 'prob'
    """
    x_input = [
        float(feature_dict.get(name, 0)) for name in lr_model.feature_names
    ]

    pred_probs = lr_model.predict_proba([x_input]).flat

    probs = [{'name': lr_model.target_names[index], 'prob': pred_probs[index]}
             for index in np.argsort(pred_probs)[::-1]]

    return (x_input, probs)


# This section checks that the prediction code runs properly
# To run, type "python predictor_api.py" in the terminal.
#
# The if __name__='__main__' section ensures this code only runs
# when running this file; it doesn't run when importing
if __name__ == '__main__':
    from pprint import pprint
    print("Checking to see what setting all params to 0 predicts")
    features = {f: '0' for f in feature_names}
    print('Features are')
    pprint(features)

    x_input, probs = make_prediction(features)
    print(f'Input values: {x_input}')
    print('Output probabilities')
    pprint(probs)
