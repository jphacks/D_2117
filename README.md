# FindPet.Me 〜日々の投稿が大切な家族をづなぐ〜
[![IMAGE ALT TEXT HERE](https://user-images.githubusercontent.com/64422386/139472603-10e6fca2-038d-4122-884a-cd926fec199a.jpg)](https://www.youtube.com/watch?v=LUPQFB4QyVo)
## 製品概要
[FindPet.Me Webページ](http://date.ddns.net:7777/)
### 背景(製品開発のきっかけ、課題等）

「愛犬と離れ離れになったらどうしよう」ふと、思いました。<br>
これがきっかけとなり、日本でのペット迷子対策について調査しました。<br>

日本における犬猫の飼育数は約2000万匹とされており、人々は動物と共存しています。<br>
そんな中、毎年多くのペットが路上を徘徊していたり、逃い込んできたりして保護されています。<br>
現在では迷子になった際の対処法として、マイクロチップの埋め込みや迷子礼などの方法があります。<br>
しかしながらこれらの方法は普及していません。<br>加えて、マイクロチップを読み込むために専用の機器が必要な点や、迷子札だと取れてしまう可能性が考えられます。<br><br>
私達はこれらの課題解決を目指した迷子のペットを探すプラットフォームとして<br>
「SNSへの日々の投稿 × AIマッチング」による【迷子のペットを探し出すアプリ】を開発しようと考えました。
### 製品説明（具体的な製品の説明）
### 特長
![タイムライン](https://user-images.githubusercontent.com/64422386/139514454-36af1182-d787-461c-a3ca-351e5ab52066.png)
#### 1. ペットの投稿に特化したオープン型「SNS」

#### 2. 日々の投稿を「AI」が分析し、飼い主とペットの再会を後押しする
飼い主からペット迷子申請がされると、「画像分析AI」がペットの特徴を分析し、「飼い主が投稿したペット画像」と「ペットを捜索する協力者からの投稿画像」を自動マッチング

#### 3. ペットのかわいい写真をクラウドに保存し、いつでも思い出を振り返ることができる

### 解決出来ること
ペットが迷子になってしまった際に、これまでよりも迅速な飼い主とペットの再開が可能になります。<br>
- 迷子のペットと飼い主が再会するまでのフロー<br>
    1. 犬が迷子になってしまった場合、飼い主はタイムラインに「迷子速報」を発出します。
    2. 「迷子速報」を元に、他のユーザーは協力して徘徊している犬を探して「迷子発見速報」を発出します。
    3. AI(人工知能)が「日々のSNSの投稿」と「迷子発見速報」を分析し、「迷子発見速報」で得られた情報を正しい飼い主へとピンポイントで通知します。またタイムラインにも表示することで、さらなる協力を求めます。

### 今後の展望
- 犬以外の「猫」など他の動物にも対応する
    - 現在対応しているAIモデルでは、「犬」以外のオブジェクトをすべて消す処理をしています。そのため「犬猫以外を削除」に変更し、Webアプリ側も対応させることで実現可能です。 
- 迷子捜索時に「位置情報」と「時間」から絞り込む機能を追加
    - 「迷子速報(飼い主)」と「迷子発見速報(協力者)」のマッチングを現在は「画像分析AI」が担っていますが、それ以前の前提として「位置情報」と「時間」から絞り込む必要があると考えております。
- 迷子のペットを捜索する協力者側に、マッチング成功時に得られる「ポイント」制度を導入する
    - 協力者側のメリットを担保することで、協力者数を増やし迷子探しコミュニティを結成する必要があると考えております。
- 「プライベートチャット」機能を追加する
    - 現在「FindPet.Me」はすべて「オープン型SNS」となっておりユーザー同士の個人情報はメールでやり取りしていただくことになっております。すべて「FindPet.Me」内で完結させることで使いやすさを向上させる必要があると考えております。
### 注力したこと（こだわり等）
- 「犬画像分析AI」のアルゴリズム開発に注力した
    - 日々犬画像や犬の種類が増え続ける中で、再学習が不要な類似画像検索のアルゴリズムを採用しました。これにより、AIが計算をするのは画像が保存されて特徴ベクトルを計算する際の際の1度だけであり、AIサーバーへの負荷を軽減しました。
    - 犬画像撮影時の背景にAIの精度が左右されにくいよう、「セマンティックセグメンテーション」を活用し犬以外の背景を削除し、トリミングする処理を加えました。
- AI処理を REST API として独立させることで、Webサーバーへの負荷軽減や処理速度向上に努めました。
    - AI REST APIは、1枚あたりの処理に0.5秒程度しかかかりません。
- タイムラインの投稿から「#ハッシュタグ」を自動生成
    - [gooラボ 形態素解析API](https://labs.goo.ne.jp/api/jp/morphological-analysis/)を使用し、タイムラインのつぶやきから、形態素解析APIを活用し名詞を抽出するのに使用しました。
    -　抽出された名詞を文字列の長い順に並び替え、最大３つの名詞を「#ハッシュタグ」として表示しました。
    -　![ハッシュタグ](https://user-images.githubusercontent.com/64422386/139514461-3609836d-9840-413f-b3d6-adb66a554a53.png)
- データベース(MySQL)処理の最適化
    - 「画像」と「ベクトル」はそれぞれファイル(画像ファイル, バイナリファイル)としてストレージに保存し、DBテーブルにはファイルパスを格納しました。
- 新規会員登録時にメール認証を実装した
    - 偽メールで会員登録がされないよう、会員登録時に入力したメールアドレス宛に「200文字のトークン」を加えたURLを送信し、そのリンクにアクセスされた場合に本登録が完了する使用にしました。
- 「FindPet.Me」UI をレスポンシブ(スマホ・PCなど画面サイズに応じて最滝化された)なデザインにした
    - 短期間でモダンなデザインにするために、Webデザインフレームワークに「Bootstrap v5.0」を使用しました。
    - また前ページで統一されたデザインとなっております。ご覧いただければ幸いです。


## 開発技術
### 活用した技術
#### API・データ
- [gooラボ 形態素解析API](https://labs.goo.ne.jp/api/jp/morphological-analysis/)
    - タイムラインのつぶやきから、形態素解析APIを活用し名詞を抽出するのに使用しました。抽出された名詞を文字列の長い順に並び替え、最大３つの名詞を「#ハッシュタグ」として表示しました。
- [Kaggle Dogs vs. Cats データセット](https://www.kaggle.com/c/dogs-vs-cats/data)
    - AIテスト用データ

#### フレームワーク・ライブラリ・モジュール
- Backend
    - App : Flask
    - Web server : Nginx, waitress
    - AI API : PyTorch, Flask
- Frontend
    - Web design : Bootstrap

#### デバイス
- Webサーバー
    - Windowsサーバー(オンプレミス)
- APIサーバー
    - Windowsサーバー(オンプレミス)
- Webアプリ表示クライアント(確認済み)
    - Windows (Chrome, Edge)
    - Mac (Chrome, Safari)
    - Android (Chrome)
    - iOS, iPadOS (Chrome, Safari)

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
