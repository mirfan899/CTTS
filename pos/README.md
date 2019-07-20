# cantonese-pos-tagger
Tagging written Cantonese with part-of-speech information, using the Stanford POS Tagger and the Hong Kong Cantonese Corpus.

Use the model

```python
from nltk.tag.stanford import StanfordPOSTagger

stanford_model = './cantonese.tagger'
stanford_jar = './stanford-postagger/stanford-postagger-3.9.1.jar'
tagger = StanfordPOSTagger(stanford_model, stanford_jar)
tagger.java_options = '-mx4096m'
text = [["一 二 三 四 五 六 七 八 九十 十 一 十 二十 三十 四十 五十 六十 七十 八十 九 二十"]]
print(tagger.tag_sents(text))
```
