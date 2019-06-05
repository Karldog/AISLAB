# from gensim.models import word2vec
# model = word2vec.Word2Vec(sentences, sg=1, size=300, window=5, min_count=10, negative=5, sample=1e-4, workers=10)

from gensim.models import word2vec
import gensim
import logging
import jieba
import os

# def read_in_chunks(filePath,chunk_size=1024*1024):
#     file_object = open(filePath)
#     while True:

def cut_txt(old_file):
    global cut_file     # 分词之后保存的文件名
    cut_file = old_file + '_cut.txt'
    fo = open(cut_file, 'w', encoding='utf-8')
    j=0
    # try:
    with open(old_file, 'r', encoding='utf-8') as f:
        for line in f:
            j = j + 1
            print(j)
    # fi = open(old_file, 'r', encoding='utf-8').read()
    # except BaseException as e:  # 因BaseException是所有错误的基类，用它可以获得所有错误类型
    #     print(Exception, ":", e)    # 追踪错误详细信息
    # text = fi.read()  # 获取文本内容
            new_text = jieba.cut(line, cut_all=False)
    # new_text = jieba.cut(fi, cut_all=False)  # 精确模式
            str_out = ' '.join(new_text).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
                .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
                .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
                .replace('’', '')     # 去掉标点符号
    # fo = open(cut_file, 'w', encoding='utf-8')
            fo.write(str_out)
    fo.close()

def model_train(train_file_name, save_model_file):  # model_file_name为训练语料的路径,save_model为保存模型名
    # 模型训练，生成词向量
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(train_file_name)  # 加载语料
    model = gensim.models.Word2Vec(sentences, sg=1, size=300, window=5, min_count=10, negative=5, sample=1e-4, workers=10)  # 训练skip-gram模型; 默认window=5
    model.save(save_model_file)
    model.wv.save_word2vec_format(save_model_name + ".bin", binary=True)   # 以二进制类型保存模型以便重用

if __name__ == '__main__':
    cut_txt('./data/text.txt')
    save_model_name = 'word2vec.model'
    if not os.path.exists(save_model_name):     # 判断文件是否存在
        model_train(cut_file, save_model_name)
    else:
        print('此训练模型已经存在，不用再次训练')


