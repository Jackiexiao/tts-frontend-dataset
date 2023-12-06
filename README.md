# tts-frontend-dataset
TTS 前端数据集汇总: 多音字 / 韵律 / 文本归一化
TTS FrontEnd DataSet: Polyphone / Prosody / TextNormalization

欢迎贡献,添加更多数据集, Feel free to contribute and add more datasets!

## ChangeLog
- 2023-12-25 添加中文多音字韵律数据

## Todo
- [ ] 添加更多语种数据

## 数据说明
### 中文Chinese
- 中文多音字韵律数据集 Chinese Polyphone and Prosody Dataset
  - 描述 Description
    - 包含61万句多音字,397个多音字, 以及32万句韵律数据. 但准确率未评估
    - Contains 610k polyphone sentences, 397 polyphones, and 320k prosody sentences. But the accuracy is not evaluated.
  - 下载 Download
    - 百度网盘: 链接: https://pan.baidu.com/s/14h6qy8AKcdjgo_rs-h2kgA?pwd=3d7s 提取码: 3d7s
    - GoogleDrive: https://drive.google.com/file/d/18qCKEqQGEdrLMNPB0CmdtH1XOqgs9w1o/view?usp=sharing
  - 数据来源
    - 文本来源: 
      - 随机挑选自 维基百科json版(wiki2019zh) from https://github.com/brightmart/nlp_chinese_corpus
      - Randomly selected from wiki2019zh
    - 标注来源:
      - 使用字节的 TTS API 返回结果 https://www.volcengine.com/product/voice-tech
      - TTS Api from ByteDance
      - 代码
        ```
        # 1. get your token from https://www.volcengine.com/product/voice-tech
        # 2. prepare txtfile then run code
        python bd_tts.py -n 2 -o output/
        python extract_data_from_bd_json.py 
        python get_g2p_data.py
        ```
  - 数据格式
    - Example: The polyphone is surrounded with ▁ in training corpus.
        ```
        # 多音字polyphone
        宋代出现了▁le5▁燕乐音阶的记载
        爆发了▁le5▁占领华尔街示威活动
        # 韵律prosody
        蔡少芬 #2 拍拖 #2 也不认啦 #4
        瓦塔拉 #1 总统 #1 已 #1 下令 #3 坚决 #1 回应 #1 袭击者 #4
        ```
  - Lexicon 《现代汉语词典》（第7版） 网友 txt 校对
    - https://github.com/CNMan/XDHYCD7th
- TN 文本正则化
  - data/zh_cn/tn/Chinese_TN_Dataset.7z  标贝开源的非商用TN数据
    - https://www.data-baker.com/data/index/TNtts/
    - Example:
        ```
        1 M-DIGIT
        4 E-DIGIT
        年 S-SELF
        7 S-CARDINAL
        月 S-SELF
        ```

### 英文English
- TN 
  - https://www.kaggle.com/c/text-normalization-challenge-english-language/data
- g2p
  - Lexicon: en-uk 英式音标
    - beep.tar.gz http://svr-www.eng.cam.ac.uk/comp.speech/Section1/Lexical/beep.html
    - Example: `IMPRESS ih m p r eh s`

### 粤语Cantonese
- G2P
    - Standard 标准: [香港粤语拼音方案](https://jyutping.org/jyutping/)
    - Lexicon
        - 粤语审音字库 http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/   
        - 粤语开放词典，有例句，包括了一些新词和新读法 http://kaifangcidian.com/han/yue 
        - 粤语发音字典，有例句 http://www.yueyv.com/


## 参考开源项目 Reference github project

### Chinese
- TN
    - https://github.com/wenet-e2e/WeTextProcessing
    - https://github.com/Ailln/cn2an
- G2P
    - https://github.com/wenet-e2e/wetts/tree/main/wetts/frontend
    - https://github.com/GitYCC/g2pW
    - https://github.com/kakaobrain/g2pm
- Prosody
    - https://github.com/wenet-e2e/wetts/tree/main/wetts/frontend
    - https://github.com/thuhcsi/SpanPSP

### English
- TN
    - https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/nlp/text_normalization/nn_text_normalization.html
- G2P
- Prosody


### Cantonese

- TN
- G2P
- Prosody

## 声明 Declaration
如有侵权请联系我 If there is any infringement, please contact me

## 讨论 Discussion

### 使用 chatgpt 标注多音字?
> 使用 gpt 4, 可能是我使用姿势不对, 没有得到一个好的结果, 我没有做深入的尝试, 如果你能得到一个好的结果欢迎与我分享

User:
```
你现在是一个中文多音字数据标注员，请按照以下格式对中文的多音字进行标注，例子：

宋代出现了▁le5▁燕乐音阶的记载
爆发了▁le5▁占领华尔街示威活动

请标注下面数据中的多音字

12月2日，江西南昌一彩票店售出中得2.2亿元大奖的彩票
为城市一线工作者营造温馨舒适的生活环境、提供多元化的配套服务。
被砸得一踏糊涂
```

ChatGPT
```
根据您的要求，这里是对给定文本中多音字的标注：

12月2日，江西南昌一彩票店售出中得▁zhong4▁2.2亿元大奖的彩票
为城市一线工作者营造温馨舒适的生活环境、提供多元化的配套服务。
被砸得一踏糊涂
在这些句子中，我只找到了一个多音字的例子，即“中”在“中得2.2亿元大奖”的上下文中读作“zhong4”。其他句子中没有显而易见的多音字。
```

User
```
继续标注

若是能让东冕少主看上
与祝先生同行的夏先生因为没注意
强烈的感觉到主人有难瞬间跳出灵魂空间
```

ChatGPT
```
以下是对您提供的文本中的多音字进行标注：

若是能让东▁mian3▁冕少主看上
与祝先生同行的夏▁xia4▁先生因为没注意
强烈的感觉到主人有难瞬间跳出灵魂空间
在这些句子中，“冕”在“东冕少主”中读作“mian3”，而“夏”在“夏先生”中读作“xia4”。其他部分没有发现多音字的用例。
```
