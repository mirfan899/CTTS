### Run normalized to convert Cantonese characters to words
```shell
./sppas/bin/normalize.py -i /Users/mirfan/PycharmProjects/sppas/sppas/ASR1.txt -o /Users/mirfan/PycharmProjects/sppas/sppas/ASR1.csv -r /Users/mirfan/PycharmProjects/sppas/resources/vocab/yue.vocab
```
### txt directory for characters as txts and words segmentation as csvs
```shell
./sppas/bin/normalize.py -i /Users/mirfan/PycharmProjects/sppas/txt/ASR2.txt -o /Users/mirfan/PycharmProjects/sppas/txt/ASR2.csv -r /Users/mirfan/PycharmProjects/sppas/resources/vocab/yue.vocab
```

### Push changes to forked sppas
https://help.github.com/en/articles/changing-a-remotes-url
```shell
git remote set-url origin https://github.com/mirfan899/sppas.git
git remote set-url origin git@github.com:mirfan899/sppas.git
``` 
