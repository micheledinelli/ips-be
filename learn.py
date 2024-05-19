import pickle
import utils


def train_model():
    model_file = utils.get_model_file()
    X, y = utils.get_train_data()
    if len(X) == 0:
        raise ValueError("No wifi access points have been found during training")
    lp = utils.get_pipeline()
    lp.fit(X, y)
    with open(model_file, "wb") as f:
        pickle.dump(lp, f)
    return lp


def predict(sample):
    sample = utils.preprocess_sample(sample)
    print(sample)
    model = utils.get_model()
    return model.predict(sample)