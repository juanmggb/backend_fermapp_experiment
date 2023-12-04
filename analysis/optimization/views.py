from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from analysis.optimization.utils import estimate_parameters, get_ordered_params
from analysis.utilis.numerical_methods import perform_simulation

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import itertools


@api_view(["POST"])
def parameter_optimization(request):
    kinetic_data = request.data.get("kineticData")
    kinetic_model = kinetic_data.get("model")
    experimental_data = request.data.get("experimentalData")
    t_values = experimental_data.get("t")
    x_values = experimental_data.get("x")
    s_values = experimental_data.get("s")
    p_values = experimental_data.get("p")
    GA_params = request.data.get("GAParams")

    if any(
        val is None
        for val in [kinetic_data, t_values, x_values, s_values, p_values, GA_params]
    ):
        return Response(
            {"error": "All inputs are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    fixed_params, best_params, error, opt_params = estimate_parameters(
        kinetic_data, t_values, x_values, s_values, p_values, GA_params
    )

    ordered_params = get_ordered_params(best_params, fixed_params)

    sol = perform_simulation(
        kinetic_model,
        [x_values[0], s_values[0], p_values[0]],
        t_values,
        ordered_params,
    )

    # Serialize the simulation results
    time_data = sol.t.tolist()
    x_data = sol.y[0].tolist()
    s_data = sol.y[1].tolist()
    p_data = sol.y[2].tolist()

    response_data = {
        "time": time_data,
        "x": x_data,
        "s": s_data,
        "p": p_data,
        "best_params": opt_params,
        "error": error,
        "model_type": kinetic_model,
        # add any other relevant information
    }

    print("response_data", response_data)

    return Response(response_data, status=200)


@api_view(["POST"])
def media_optimization(request):
    data = request.data

    # Extracting the relevant data
    experimental_data = data.get("processData")
    la_params = data.get("LRParams")

    # Converting the data to a pandas DataFrame
    df = pd.DataFrame(experimental_data)

    # Extracting the variables for analysis
    X = df[[la_params["x_var"], la_params["y_var"]]].values  # Independent variables
    z = df[la_params["z_var"]].values  # Dependent variable

    # Splitting the data into training and testing sets
    X_train, X_test, z_train, z_test = train_test_split(
        X,
        z,
        test_size=float(la_params["test_size"]),
        random_state=int(la_params["random_state"]),
    )

    # Normalizing the data if required
    if la_params["normalization"]:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    # Creating polynomial features if degree is more than 1
    if int(la_params["polynomial_degree"]) > 1:
        poly = PolynomialFeatures(degree=int(la_params["polynomial_degree"]))
        X_train = poly.fit_transform(X_train)
        X_test = poly.transform(X_test)

    # Performing the Linear Regression analysis
    lr = LinearRegression()
    lr.fit(X_train, z_train)
    z_pred = lr.predict(X_test)

    # Calculate metrics
    print(z_test, z_pred)
    r2 = r2_score(z_test, z_pred)
    mae = mean_absolute_error(z_test, z_pred)
    mse = mean_squared_error(z_test, z_pred)
    rmse = np.sqrt(mse)

    # Evaluating the predictions
    # Creating a response surface (or line) for plotting predictions
    x1_surf, x2_surf = np.meshgrid(
        np.linspace(X[:, 0].min(), X[:, 0].max(), 5),
        np.linspace(X[:, 1].min(), X[:, 1].max(), 5),
    )
    X_surf = np.c_[x1_surf.ravel(), x2_surf.ravel()]
    if la_params["normalization"]:
        X_surf = scaler.transform(X_surf)
    if int(la_params["polynomial_degree"]) > 1:
        X_surf = poly.transform(X_surf)
    z_surf = lr.predict(X_surf)
    z_surf = z_surf.reshape(x2_surf.shape)

    response_surface = {
        "x_surf": x1_surf.tolist(),
        "y_surf": x2_surf.tolist(),
        "z_surf": z_surf.tolist(),
    }

    # Generate feature names based on the polynomial degree
    feature_names = ["Intercept"]
    if int(la_params["polynomial_degree"]) > 1:
        for d in range(1, int(la_params["polynomial_degree"]) + 1):
            feature_names.extend(
                generate_feature_names([la_params["x_var"], la_params["y_var"]], d)
            )
    else:
        feature_names.extend([la_params["x_var"], la_params["y_var"]])

    # Prepare the response data
    response_data = {
        "response_surface": response_surface,
        "model_params": dict(zip(feature_names, [lr.intercept_, *lr.coef_])),
        "model_metrics": {
            "r2": r2,
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
        },
        "data_split": {
            "test_size": float(la_params["test_size"]),
            "random_state": int(la_params["random_state"]),
        },
        "features": {
            "dependent_variable": la_params["z_var"],
            "independent_variables": [la_params["x_var"], la_params["y_var"]],
        },
        "preprocessing": {
            "normalization": la_params["normalization"],
            "polynomial_degree": int(la_params["polynomial_degree"]),
        },
    }

    print("metrics", response_data["model_metrics"])

    return Response(response_data, status=200)


# Utility function to generate feature names
def generate_feature_names(input_vars, degree):
    combinations = itertools.combinations_with_replacement(input_vars, degree)
    feature_names = []
    for combination in combinations:
        name = " * ".join(combination)
        feature_names.append(name)
    return feature_names
