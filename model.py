import pickle
import utils


def train(data_path: str):
    """
    Trains a machine learning model using the provided data.

    Args:
        data_path (str): The path to the data.

    Returns:
        lp: The trained machine learning model.
    """
    model_file = utils.get_model_file(data_path=data_path)
    X, y = utils.get_train_data(data_path=data_path)
    if len(X) == 0:
        raise ValueError("No wifi access points have been found during training")
    lp = utils.get_pipeline()
    lp.fit(X, y)
    with open(model_file, "wb") as f:
        pickle.dump(lp, f)
    return lp


def predict(sample, data_path: str):
    """
    Predicts the output for a given sample using a trained model.

    Args:
        sample: The input sample to be predicted.
        data_path: The path to the data.

    Returns:
        The predicted output for the given sample.
    """
    sample = utils.preprocess_sample(sample, data_path=data_path)
    model = utils.get_model(data_path=data_path)
    return model.predict(sample)[0]


def predict_proba(sample, data_path: str):
    """
    Predicts the probability of a sample belonging to a certain class.

    Args:
        sample: The input sample to be predicted.
        data_path: The path to the data.

    Returns:
        The predicted probability of the sample belonging to a certain class.
    """
    sample = utils.preprocess_sample(sample, data_path=data_path)
    model = utils.get_model(data_path=data_path)
    return model.predict_proba(sample)[0]