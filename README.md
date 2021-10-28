# FindPet.Me 〜日々の投稿が大切な家族を救う〜
[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2021/07/JPHACKS2021_ogp.jpg)](https://www.youtube.com/watch?v=LUPQFB4QyVo)

## 製品概要
### 背景(製品開発のきっかけ、課題等）
日本における犬猫の飼育数は約2000万匹とされており、人々は動物と共存しています。<br>
そんな中、毎年多くのペットが路上を徘徊していたり、逃い込んできたりして保護されています。<br>
現在では迷子になった際の対処法として、マイクロチップの埋め込みや迷子礼などの方法があります。<br>
しながらこれらの方法はまだ普及しておらず、対策としては不十分です。<br>
私達は迷子のペットを探すプラットフォームとして、<br>
「周囲の人々によるSNS×AIマッチング」による【迷子のペットを探し出すアプリ】を開発しようと考えました。
### 製品説明（具体的な製品の説明）
### 特長
#### 1. ペットの投稿に特化したオープン型「SNS」

#### 2. ペット迷子申請がされると、「画像分析AI(人工知能)」がペットの特徴を分析し、飼い主と発見者からの投稿を自動マッチング

#### 3. ペットのかわいい写真をクラウド上に保存できる

### 解決出来ること
### 今後の展望
### 注力したこと（こだわり等）
* 
* 

## 開発技術
### 活用した技術
#### API・データ
* 
* 

#### フレームワーク・ライブラリ・モジュール
* 
* 

#### デバイス
* 
* 

### 独自技術
#### 犬画像を「画像分析AI(人工知能)」が分析し、犬同士の類似度を計算する技術
##### 「画像分析AI(人工知能)」のフロー
1. [FCN ResNet50 (ニューラルネットワーク)](https://arxiv.org/abs/1411.4038)に犬画像を入力し、セグメンテーションマスクを取得
2. (1.)で得られたセグメンテーションマスクにより、犬画像から犬以外のオブジェクトをすべて削除し、犬部分をトリミング
3. (2.)で得られた犬画像を、[VGG19(ニューラルネットワーク)](https://arxiv.org/abs/1409.1556)に入力し、4096次元の特徴量ベクトルを取得
4. (3.)で得られた犬ごとの特徴量ベクトル同士において、コサイン類似度(0.0〜1.0)を求める
5. (4.)で得られた犬ごとのコサイン類似度を類似度順に並べて、類似犬画像としてレコメンド

- 特に力を入れた部分<br>
[画像分析AIモデルをPyTorch(ニューラルネットワーク・フレームワーク)でコーディング](https://github.com/jphacks/D_2117/blob/dev_kuboko/ai/utils/model.py)<br>
    - Commit ID 01 [ac59e9744c529adc6aa759fc5df660fe653037a3](https://github.com/jphacks/D_2117/commit/ac59e9744c529adc6aa759fc5df660fe653037a3#diff-64f017e26787ef375a8d3506b2e62df90ab41ff128357162560b6e6e19fe4faa)<br>
    - Commit ID 02 [f39220917cfdba25fa897c7b198b7d16de0fa1a8](https://github.com/jphacks/D_2117/commit/f39220917cfdba25fa897c7b198b7d16de0fa1a8#diff-64f017e26787ef375a8d3506b2e62df90ab41ff128357162560b6e6e19fe4faa)

- 犬画像のセグメンテーション & 切り抜き
![dog_segmentation](https://user-images.githubusercontent.com/64422386/139197817-4e676b55-c878-4258-9176-be7f7d926c2a.png)<br>
- 犬画像をコサイン類似度順に並べ替え
![dog_cos_sim](https://user-images.githubusercontent.com/64422386/139198020-b713bbcb-37c8-4993-b8b3-a0cc54ca4844.jpg)



#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
- Jonathan Long, Evan Shelhamer, Trevor Darrell,「[Fully Convolutional Networks for Semantic Segmentation
](http://arxiv.org/abs/1411.4038)」, arXiv:1411.4038 [cs]
- Karen Simonyan, Andrew Zisserman, 「(Very Deep Convolutional Networks for Large-Scale Image Recognition
)[https://arxiv.org/abs/1409.1556]」, arXiv:1409.1556 [cs.CV]
