import numpy as np
import pickle

def load_np_array(path:str) -> np.ndarray:
    with open(path, "rb") as f :
        array = pickle.load(f)

    return array