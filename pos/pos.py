from nltk.tag.stanford import StanfordPOSTagger
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))

stanford_model =path+'/cantonese.tagger'
stanford_jar = path+'/stanford-postagger/stanford-postagger-3.9.1.jar'
tagger = StanfordPOSTagger(stanford_model, stanford_jar)
tagger.java_options = '-mx1024m'
# text = ["咁 都 真係 天公 做 美 啦 因為 呢 天氣 真係 好好 好 涼爽"]
# taggs = tagger.tag(text)
# words = [item[1].split("/")[0] for item in taggs]
# tags = [item[1].split("/")[1] for item in taggs]
# assert len(tags) == len(words)
# print(words, tags)


def get_tags(sentence=None):
    """
    Convert the sentence into words and POS tags list
    :param sentence:
    :return:
    """
    tags = tagger.tag([sentence])
    wrds = [item[1].split("/")[0] for item in tags]
    # tags = [item[1].split("/")[1] for item in tags]
    tags = [item[1].split("/")[1][0].lower() for item in tags]
    assert len(tags) == len(wrds)
    return wrds, tags


# text = "整 完 香腸 同埋 蛋 之後 呢 我 就 叫 馮 曉 立 起身 咁 佢 起 咗 身 我哋 一齊 食早餐 呢 我 先至 開始 拾 嗰 隻 糭"
# words, tags = get_tags(text)
#
# words = [item[1].split("/")[0] for item in tags]
# tags = [item[1].split("/")[1] for item in tags]
# assert len(tags) == len(words)
# print(words)
# print(tags)
