def analyze_values(actual_values, predicted_values):
    """
    Compares actual vs. predicted values and calculates the percentage difference where
    actual values are lower than predicted.

    Parameters:
        actual_values (list or np.array): True values
        predicted_values (list or np.array): Model predictions

    Returns:
        list of tuples: (percentage difference, index)
    """
    if len(actual_values) != len(predicted_values):
        raise ValueError("Both lists must be of the same length")

    results = []
    for i, (actual, predicted) in enumerate(zip(actual_values, predicted_values)):
        if actual < predicted:
            percent_lower = ((predicted - actual) / predicted) * 100
            results.append((percent_lower, i))

    return results
