"""
Machine Learning Model Factory
Returns the requested ML model.
"""

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor
)
from sklearn.neighbors import (
    KNeighborsClassifier,
    KNeighborsRegressor
)


def get_model(model_name, task="classification", **kwargs):
    """
    Returns the selected machine learning model.

    Parameters
    ----------
    model_name : str
        Name of the model.

    task : str
        "classification" or "regression"

    kwargs : dict
        Extra model parameters.

    Returns
    -------
    sklearn model
    """

    if task == "classification":

        models = {

            "Logistic Regression":
                LogisticRegression(max_iter=1000, **kwargs),

            "Decision Tree":
                DecisionTreeClassifier(**kwargs),

            "Random Forest":
                RandomForestClassifier(**kwargs),

            "KNN":
                KNeighborsClassifier(**kwargs)

        }

    elif task == "regression":

        models = {

            "Linear Regression":
                LinearRegression(**kwargs),

            "Decision Tree":
                DecisionTreeRegressor(**kwargs),

            "Random Forest":
                RandomForestRegressor(**kwargs),

            "KNN":
                KNeighborsRegressor(**kwargs)

        }

    else:

        raise ValueError(
            "Task must be either 'classification' or 'regression'."
        )

    if model_name not in models:

        raise ValueError(
            f"Model '{model_name}' is not supported."
        )

    return models[model_name]