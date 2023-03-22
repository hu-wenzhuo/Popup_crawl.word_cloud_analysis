import pandas as pd
from snownlp import SnowNLP
from wordcloud import WordCloud
from pprint import pprint
import jieba.analyse
from PIL import Image
import numpy as np


# 情感分析打标
def sentiment_analyse(v_cmt_list):
    """
    情感分析打分
    :param v_cmt_list: 需要处理的评论列表
    :return:
    """
    score_list = []  # 情感评分值
    tag_list = []  # 打标分类结果
    pos_count = 0  # 计数器-积极
    neg_count = 0  # 计数器-消极
    for comment in v_cmt_list:
        tag = ''
        sentiments_score = SnowNLP(comment).sentiments
        if sentiments_score < 0.3:
            tag = '消极'
            neg_count += 1
        else:
            tag = '积极'
            pos_count += 1
        score_list.append(sentiments_score)  # 得分值
        tag_list.append(tag)  # 判定结果
    print('积极评价占比：', round(pos_count / (pos_count + neg_count), 4))
    print('消极评价占比：', round(neg_count / (pos_count + neg_count), 4))
    df['情感得分'] = score_list
    df['分析结果'] = tag_list
    # 把情感分析结果保存到excel文件
    df.to_excel('情感评分结果.xlsx', index=None)
    print('情感分析结果已生成：情感评分结果.xlsx')


def make_wordcloud(v_str, v_stopwords, v_outfile):
    """
    绘制词云图
    :param v_str: 输入字符串
    :param v_stopwords: 停用词
    :param v_outfile: 输出文件
    :return: None
    """
    print('开始生成词云图：{}'.format(v_outfile))
    try:
        stopwords = v_stopwords  # 停用词
        backgroud_Image = np.array(Image.open('背景2.jpg'))  # 读取背景图片
        wc = WordCloud(
            background_color="black",  # 背景颜色
            width=1800,  # 图宽
            height=2500,  # 图高
            max_words=1000,  # 最多字数
            font_path='C:\Windows\Fonts\Deng.ttf',
            stopwords=stopwords,  # 停用词
            mask=backgroud_Image,  # 背景图片
        )
        #jieba_text = " ".join(jieba.lcut(v_str))  # jieba分词
        data = v_str.apply(jieba.cut, cut_all=False)
        dataAfter = data.apply(lambda x: [i for i in x if i not in v_stopwords])
        v_list = [str(i) for i in dataAfter.values.tolist()]
        jieba_text = ''.join(str(i) for i in v_list)
        wc.generate_from_text(jieba_text)  # 生成词云图
        wc.to_file(v_outfile)  # 保存图片文件
        print('词云文件保存成功：{}'.format(v_outfile))
    except Exception as e:
        print('make_wordcloud except: {}'.format(str(e)))


if __name__ == '__main__':
    df = pd.read_csv('弹幕.csv')
    v_cmt_list = df['弹幕内容'].values.tolist()
    print('弹幕条数:{}'.format(len(v_cmt_list)))
    v_cmt_list = [str(i) for i in v_cmt_list]
    v_cmt_str = ''.join(str(i) for i in v_cmt_list)

    sentiment_analyse(v_cmt_list)
    # 2、用jieba统计弹幕中的top10高频词
    keywords_top10 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=10)
    print('top10关键词及权重：')
    pprint(keywords_top10)

    stopwords = set()
    content = [line.strip() for line in open('baidu_stopwords.txt', 'r', encoding='utf-8').readlines()]
    stopwords.update(content)

    make_wordcloud(v_str=df['弹幕内容'], v_stopwords=stopwords, v_outfile='词云.jpg')
