# Dog detection AI
## 1. SetUp
```bash
docker build -t jphacks_ai:latest ./environment
```
```bash
docker run -it --name jphacks_ai --gpus all -v $(pwd):/workspace jphacks_ai:latest /bin/bash
```
## 2. Preparation
前準備
- /secret.yaml ファイルを作成
```Yaml
AI:
  API_KEY: 'API_KEYは管理者までお問い合わせください。'
```
- AI API Flaskサーバーを起動 (Flaskサーバーは開発用の為、運用時はNginx, uWSGIを挟むことを推奨)
```Python
python /run_ai_api.py
```

## 3. Usage
### 3.1 AI REST API
画像をAPI経由でPOSTして、特徴ベクトルを取得する。

"endpoint", "img_path", "api_key"の3つを指定する。
```Python
import requests
import yaml

endpoint = "http://127.0.0.1:5000/predict"
img_path = './ai/input/1_1.jpg'

with open('secret.yaml', 'r') as f:
    secret = yaml.safe_load(f)
api_key = secret['AI']['API_KEY']

resp = requests.post(endpoint, files={"file": open(img_path,'rb')}, headers={'api_key':api_key})

resp_dict = resp.json()
print(resp_dict)  # 4096次元ベクトルがlist型で格納される
# api_keyが正しい場合
-> {'authentication': 'ok', 'vector': [-1.6974670886993408, -1.3484156131744385, ... , -0.9846966862678528]}
# api_keyが間違っている場合
-> {'authentication': 'no'}
```
### 3.2 AI Module
Pythonモジュールを呼び出し、画像のパスを指定して特徴ベクトルを取得する。
```Python
from dog_vector import DogVector

dogs_path_list = ['./input/individual_dogs/1_1.jpg']

# vector_out_dir : str
# 　　ベクトルの出力先ディレクトリ
dogvec = DogVector(img_path_list=dogs_path_list, vector_out_dir='./vectors')
vec_dict = dogvec.get_vector()

print(vec_dict)
-> {'ImageFilename':[-1.6974670886993408, -1.3484156131744385, ... , -0.9846966862678528]}  
```
### 2.2 Get Cosine similarity
2つのベクトルからコサイン類似度を求める
```Python
import utils.calc_sim import get_cos_sim

v1 = [0, 1, 2, 3, 4]  # list or numpy
v2 = [0, 1, 2, 3, 4]  # list or numpy
cos_sim = get_cos_sim(v1=v1, v2=v2)
```

