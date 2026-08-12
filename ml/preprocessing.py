import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.preprocessing import StandardScaler


def preprocess_dataset(df, target_column):

    """
    Complete preprocessing pipeline.
    """

    df = df.copy()

    # -------------------------
    # Separate Features & Target
    # -------------------------

    X = df.drop(columns=[target_column])

    y = df[target_column]

    # -------------------------
    # Encode categorical features
    # -------------------------

    encoders = {}

    categorical_columns = X.select_dtypes(include="object").columns

    for column in categorical_columns:

        encoder = LabelEncoder()

        X[column] = encoder.fit_transform(X[column].astype(str))

        encoders[column] = encoder

    # -------------------------
    # Encode target if needed
    # -------------------------

    target_encoder = None

    if y.dtype == "object":

        target_encoder = LabelEncoder()

        y = target_encoder.fit_transform(y)

    # -------------------------
    # Train Test Split
    # -------------------------

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42

    )

    # -------------------------
    # Feature Scaling
    # -------------------------

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    X_test = scaler.transform(X_test)

    return {

        "X_train": X_train,

        "X_test": X_test,

        "y_train": y_train,

        "y_test": y_test,

        "scaler": scaler,

        "encoders": encoders,

        "target_encoder": target_encoder

    }