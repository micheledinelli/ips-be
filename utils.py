import os
import threading
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import learn

def load_data(data_path: str) -> pd.DataFrame:
    try:
        file_path = os.path.join(data_path, 'data.pkl')
        data = pd.read_pickle(file_path)
        return data
    except FileNotFoundError:
        return pd.DataFrame()

    
def save_data(online_data: list, room: str, data_path: str) -> None:
    try:
        online_data = process_online_data(online_data, room=room)
        online_data_df = pd.DataFrame([online_data])

        # Load the existing data
        data = load_data(data_path)

        # Concatenate the existing data with the new data
        df = pd.concat([data, online_data_df], ignore_index=True)
        df.fillna(0, inplace=True)

        # learn.train_model(df, data_path)
        
        # Save the concatenated DataFrame to a pickle file
        file_path = os.path.join(data_path, 'data.pkl')
        df.to_pickle(file_path)
    except FileNotFoundError:
        online_data_df = pd.DataFrame([online_data])
        file_path = os.path.join(data_path, 'data.pkl')
        online_data_df.to_pickle(file_path)
    

def delete_data(data_path: str) -> None:
    try:
        file_path = os.path.join(data_path, 'data.pkl')
        os.remove(file_path)
    except FileNotFoundError:
        pass


def process_online_data(online_data: list, room=None) -> dict:
    sample = {}
    for ap in online_data:
        id = ap.get("bssid") + "-" + ap.get("ssid")    
        quality = ap.get("quality")
        sample[id] = quality
    if room:
        sample["room"] = room
    return sample


def async_save_data(online_data: dict, room: str, data_path: str) -> None:
    thread = threading.Thread(target=save_data, args=(online_data, room, data_path))
    thread.start()
    

def get_pipeline():
    return RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
