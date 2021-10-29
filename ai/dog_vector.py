import torch
from torch.utils.data import DataLoader

import pandas as pd
import numpy as np
from tqdm import tqdm
import os

from utils.config import get_config, seed_torch
from utils.dataset import CustomDataset
from utils.model import CustomModel


class DogVector:
    """
    画像のパスとベクトルの出力先を指定すると、
    出力先のディレクトリにベクトルファイル(.npy)を出力する

    Attributes
    ----------
        img_path_list : list
            画像のパス(String)を格納したリスト
        vector_out_dir : str, default None
            None ->
                返り値として、{'filepath': [0.24, 0.42 ..... 0.37]} Dictionary型が返却される。
                ベクトルファイルは保存されない
            Stringを指定  ->
                ベクトルの出力先のディレクトリ
                指定したディレクトリが存在しなかった場合は、ディレクトリが作成される。
                './vectors' とした場合、img_path_listで指定した画像ファイルに対するベクトルが出力される。
                例 -> './vectors/1_1.npy'
    """

    def __init__(self, img_path_list: list, vector_out_dir=None):

        maxLen_img_path_list = 1600  # これ以上だとサーバーに負荷がかかりすぎる可能性があるため上限を設定。
        assert len(img_path_list) <= maxLen_img_path_list, \
            f"The length of img_path_list must be less than or equal to {maxLen_img_path_list}."

        self.dogs_df = pd.DataFrame(columns=['path'])
        self.dogs_df['path'] = img_path_list

        self.config = get_config()
        self.bs = self.config.hparams.batch_size
        seed_torch(seed=self.config.seed)

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device : {self.device}")
        model = CustomModel()
        self.model = model.to(self.device).eval()

        self.vector_out_dir = vector_out_dir

    def _get_dl(self):

        ds = CustomDataset(df=self.dogs_df, config=self.config, phase='test')
        dl = DataLoader(ds, batch_size=self.bs, shuffle=False)

        return dl

    def get_vector(self):

        vec_dict = {}

        dl = self._get_dl()
        for i, (images, labels, filenames) in enumerate(tqdm(dl)):

            with torch.no_grad():
                out = self.model(images)
            out_list = out.to('cpu').detach().numpy().tolist()
            vec_dict.update(
                dict(zip(filenames, out_list))
            )

        # vector_out_dirが指定された場合のみ、ベクトルファイルを保存
        if type(self.vector_out_dir) is str:
            print(f"{len(list(vec_dict.keys()))} vector files is saving.")
            os.makedirs(self.vector_out_dir, exist_ok=True)
            for key in vec_dict.keys():
                vector_fname_extention = key.split('/')[-1]
                fname_extension = vector_fname_extention[-3:]  # jpg or JPG
                assert fname_extension in [
                    'jpg', 'JPG'], f"Filename extension is {fname_extension}, but it must {['jpg', 'JPG']}"
                vector_npy_path = os.path.join(
                    self.vector_out_dir, f"{vector_fname_extention[:-4]}.npy")
                np.save(vector_npy_path, vec_dict[key])

        return vec_dict


if __name__ == '__main__':

    dogs_dir = './input/kaggle_dogs'
    img_path_list = [
        'input/individual_dogs/1_1.jpg',
        'input/individual_dogs/2_1.jpg',
        'input/individual_dogs/3_1.jpg',
        'input/individual_dogs/4_1.jpg',
        'input/individual_dogs/5_1.jpg',
    ]
    dogvec = DogVector(img_path_list=img_path_list, vector_out_dir='./vectors')
    vec_dict = dogvec.get_vector()
    print(vec_dict.keys())
