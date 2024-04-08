# Filename: dynamic_pipeline_with_nn.py

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import numpy as np


def analyze_problem_statement(problem_statement):
    """
    Analyze the problem statement to determine the type of problem.
    """
    if (
        "classify" in problem_statement
        or "classification" in problem_statement
    ):
        return "classification"
    elif (
        "predict" in problem_statement
        or "regression" in problem_statement
    ):
        return "regression"
    else:
        return "unknown"


def generate_solving_function(problem_type, dataset=None):
    """
    Dynamically generate a function that tries multiple models and selects the best one.
    """
    if problem_type == "classification":
        models = {
            "RandomForestClassifier": RandomForestClassifier(),
            "LogisticRegression": LogisticRegression(),
            "NeuralNetwork": (  # Placeholder for NN model
                "NN_Classification"
            ),
        }
    elif problem_type == "regression":
        models = {
            "RandomForestRegressor": RandomForestRegressor(),
            "RidgeRegression": Ridge(),
            "NeuralNetwork": (  # Placeholder for NN model
                "NN_Regression"
            ),
        }
    else:
        print("Unknown problem type.")
        return None

    def solve_with_nn(X_train, X_test, y_train, y_test, problem_type):
        """
        Trains and evaluates a simple neural network.
        """
        model = Sequential(
            [
                Dense(
                    128,
                    activation="relu",
                    input_shape=(X_train.shape[1],),
                ),
                Dense(64, activation="relu"),
                Dense(
                    1,
                    activation=(
                        "sigmoid"
                        if problem_type == "classification"
                        else "linear"
                    ),
                ),
            ]
        )
        model.compile(
            optimizer=Adam(),
            loss=(
                "binary_crossentropy"
                if problem_type == "classification"
                else "mean_squared_error"
            ),
            metrics=(
                ["accuracy"]
                if problem_type == "classification"
                else ["mse"]
            ),
        )
        model.fit(
            X_train, y_train, epochs=100, batch_size=10, verbose=0
        )
        eval_result = model.evaluate(X_test, y_test, verbose=0)
        return model, eval_result[1]

    def solving_function(X, y):
        """
        Function to try multiple models and select the one with the best performance.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        best_score = -np.inf
        best_model = None
        best_model_name = ""

        for name, model in models.items():
            if "NeuralNetwork" in name:
                model, score = solve_with_nn(
                    X_train, X_test, y_train, y_test, problem_type
                )
            else:
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                score = (
                    accuracy_score(y_test, predictions)
                    if problem_type == "classification"
                    else r2_score(y_test, predictions)
                )
            print(f"{name} Performance: {score}")

            if score > best_score:
                best_score = score
                best_model = model
                best_model_name = name

        print(
            f"Best Model: {best_model_name} with a score of"
            f" {best_score}"
        )
        return best_model

    return solving_function


def pipeline(dataset=None):
    """
    The main pipeline prompts for a problem statement and uses an optional dataset to dynamically create and apply a solving function.
    """
    problem_statement = input("Enter your problem statement: ")
    problem_type = analyze_problem_statement(problem_statement)
    solving_function = generate_solving_function(
        problem_type, dataset
    )

    if solving_function and dataset is not None:
        X, y = dataset
        solving_function(X, y)
    else:
        print(
            "No dataset provided or unknown problem type. Function"
            " generation might be limited."
        )


# Example usage
if __name__ == "__main__":
    # Example dataset for demonstration; replace with actual data as needed.
    X, y = make_classification(
        n_samples=100,
        n_features=4,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
    dataset = (X, y)

    pipeline(dataset)
