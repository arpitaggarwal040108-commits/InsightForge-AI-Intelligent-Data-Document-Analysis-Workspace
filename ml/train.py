"""
Training and evaluation functions.
"""

import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from ml.models import get_model


def train_model(
    processed_data,
    model_name,
    task="classification",
    save_path=None
):
    """
    Train and evaluate a machine learning model.
    """

    X_train = processed_data["X_train"]
    X_test = processed_data["X_test"]
    y_train = processed_data["y_train"]
    y_test = processed_data["y_test"]

    model = get_model(
        model_name=model_name,
        task=task
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    if task == "classification":

        metrics = {

            "accuracy":
                round(
                    accuracy_score(
                        y_test,
                        predictions
                    ),
                    4
                ),

            "precision":
                round(
                    precision_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    ),
                    4
                ),

            "recall":
                round(
                    recall_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    ),
                    4
                ),

            "f1_score":
                round(
                    f1_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    ),
                    4
                ),

            "confusion_matrix":
                confusion_matrix(
                    y_test,
                    predictions
                ).tolist()

        }

    else:

        mse = mean_squared_error(
            y_test,
            predictions
        )

        metrics = {

            "mae":
                round(
                    mean_absolute_error(
                        y_test,
                        predictions
                    ),
                    4
                ),

            "mse":
                round(
                    mse,
                    4
                ),

            "rmse":
                round(
                    mse ** 0.5,
                    4
                ),

            "r2_score":
                round(
                    r2_score(
                        y_test,
                        predictions
                    ),
                    4
                )

        }

    if save_path:

        joblib.dump(
            model,
            save_path
        )

    return {

        "model": model,

        "predictions": predictions,

        "metrics": metrics

    }