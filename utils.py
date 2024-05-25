import os
import threading
import pandas as pd
import model
import pickle
import errors
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load data from a pickle file.

    Args:
        data_path (str): The path to the directory containing the pickle file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the pickle file is not found, an empty DataFrame is returned.
    """
    try:
        file_path = os.path.join(data_path, 'data.pkl')
        data = pd.read_pickle(file_path)
        return data
    except FileNotFoundError:
        return pd.DataFrame()

    
def save_data(online_data: list, room: str, data_path: str) -> None:
    """
    Save online data to a pickle file.

    Args:
        online_data (list): The online data to be saved.
        room (str): The room associated with the online data.
        data_path (str): The path to the directory where the data will be saved.

    Returns:
        None
    """
    try:
        online_data = process_online_data(online_data, room=room)
        online_data_df = pd.DataFrame([online_data])

        # Load the existing data
        data = load_data(data_path=data_path)

        # Concatenate the existing data with the new data
        df = pd.concat([data, online_data_df], ignore_index=True)
        df.fillna(0, inplace=True)

        # Save the concatenated DataFrame to a pickle file
        file_path = os.path.join(data_path, 'data.pkl')
        df.to_pickle(file_path)
        
        model.train(data_path=data_path)
    except FileNotFoundError:
        online_data_df = pd.DataFrame([online_data])
        file_path = os.path.join(data_path, 'data.pkl')
        online_data_df.to_pickle(file_path)
    

def delete_data(data_path: str) -> None:
    """
    Delete the data file located at the given data path.

    Args:
        data_path (str): The path to the data directory.

    Returns:
        None
    """
    try:
        file_path = os.path.join(data_path, 'data.pkl')
        os.remove(file_path)
    except FileNotFoundError:
        pass


def process_online_data(online_data: list, room=None) -> dict:
    """
    Process the online data and return a dictionary containing the access point IDs and their corresponding quality.

    Args:
        online_data (list): A list of dictionaries representing the online data.
        room (str, optional): The room associated with the online data. Defaults to None.

    Returns:
        dict: A dictionary containing the access point IDs as keys and their corresponding quality as values.
              If a room is provided, it also includes a "room" key with the room value.
    """
    sample = {}
    for ap in online_data:
        id = ap.get("ssid")    
        quality = ap.get("quality")
        sample[id] = quality
    if room:
        sample["room"] = room
    return sample


def async_save_data(online_data: dict, room: str, data_path: str) -> None:
    """
    Asynchronously saves the online data to a specified data path.

    Args:
        online_data (dict): The online data to be saved.
        room (str): The room identifier.
        data_path (str): The path where the data will be saved.

    Returns:
        None
    """
    thread = threading.Thread(target=save_data, args=(online_data, room, data_path))
    thread.start()
    

def get_pipeline(clf=RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")):
    """
    Returns a scikit-learn pipeline with the specified classifier.

    Args:
        clf (estimator, optional): The classifier to use in the pipeline. Defaults to RandomForestClassifier.

    Returns:
        pipeline: A scikit-learn pipeline object.
    """
    return make_pipeline(clf)


def get_model_file(data_path: str) -> str:
    """
    Returns the file path of the model located in the given data path.

    Args:
        data_path (str): The path to the data directory.

    Returns:
        str: The file path of the model.

    Raises:
        errors.ModelNotFound: If the model file is not found in the data path.
    """
    try:
        return os.path.join(data_path, 'model.pkl')
    except Exception:
        raise errors.ModelNotFound()


def get_model(data_path: str):
    """
    Load and return a trained model from the specified data path.

    Args:
        data_path (str): The path to the data directory.

    Returns:
        object: The trained model loaded from the file.

    Raises:
        errors.ModelNotFound: If the model file is not found.
    """
    model_file = get_model_file(data_path)
    try:
        with open(model_file, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        raise errors.ModelNotFound()
    

def get_train_data(data_path: str) -> tuple:
    """
    Load and preprocess training data.

    Args:
        data_path (str): The path to the data file.

    Returns:
        tuple: A tuple containing the features (X) and the target variable (y).
    """
    data = load_data(data_path=data_path)

    if data.empty:
        raise errors.DataNotFound()

    X = data.drop("room", axis=1)
    y = data["room"]
    return X, y


def preprocess_sample(sample: dict, data_path: str):
    """
    Preprocesses a sample by filling in missing values with the median value from the training data.

    Args:
        sample (dict): A dictionary representing a sample.
        data_path (str): The path to the training data.

    Returns:
        pd.DataFrame: The preprocessed sample with missing values filled in.
    """
    # Load the data
    data = load_data(data_path=data_path)

    if data.empty:
        raise errors.DataNotFound()
   
    # Some APs may not be in the model, so we need to fill in the missing values
    sample = process_online_data(sample, room=None)
    X = pd.DataFrame([sample])
    
    # X has to contain all the columns in data, if X miss some columns it has to be added with the median value of the column
    missing_columns = set(data.drop(columns=["room"]).columns) - set(X.columns)
    
    for col in missing_columns:
        X[col] = 0
        
    # X has to contain all the columns in data, if X has more columns than data, it has to be removed
    X = X[data.drop(columns=["room"]).columns]
    return X
