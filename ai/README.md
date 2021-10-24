# Dog detection AI
## 1. SetUp
```bash
docker build -t jphacks_ai:latest ./environment
```
```bash
docker run -it --name jphacks_ai --gpus all -v $(pwd):/workspace jphacks_ai:latest /bin/bash
```
## 2. Usage
### 2.1 Get vector
画像のパスを指定し、ベクトルを取得する。
```Python
from dog_vector import DogVector

dogs_path_list = ['./input/individual_dogs/1_1.jpg']

# vector_out_dir : str
# 　　ベクトルの出力先ディレクトリ
dogvec = DogVector(img_path_list=dogs_path_list, vector_out_dir='./vectors')
vec_dict = dogvec.get_vector()

vec_dict >>> {'ImageFilename':[0.01, 0.04, 0.03, ... , 0.92]}  
```
### 2.2 Get Cosine similarity
2つのベクトルからコサイン類似度を求める
```Python
import utils.calc_sim import get_cos_sim

v1 = [0, 1, 2, 3, 4]  # list or numpy
v2 = [0, 1, 2, 3, 4]  # list or numpy
cos_sim = get_cos_sim(v1=v1, v2=v2)
```

