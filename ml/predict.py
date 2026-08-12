"""
Prediction functions for trained models.
"""

import joblib
import pandas as pd


def load_saved_model(model_path):
    """
    Loads a saved machine learning model.
    """

    model = joblib.load(model_path)

    return model


def preprocess_input(
    input_data,
    scaler,
    encoders=None
):
    """
    Preprocess user input before prediction.
    """

    df = pd.DataFrame([input_data])

    if encoders:

        for column, encoder in encoders.items():

            if column in df.columns:

                df[column] = encoder.transform(
                    df[column].astype(str)
                )

    scaled = scaler.transform(df)

    return scaled


def predict(
    model,
    processed_input,
    target_encoder=None
):
    """
    Predict using trained model.
    """

    prediction = model.predict(processed_input)

    if target_encoder is not None:

        prediction = target_encoder.inverse_transform(prediction)

    return prediction[0]