import numpy as np

def get_cos_sim(v1, v2):
    """
    画像から出力した2つのベクトルからコサイン類似度を計算するメソッド

    Parameters
    ----------
    v1 : list or numpy
        1つめのベクトル
    v2 : list or numpy
        2つめのベクトル
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
