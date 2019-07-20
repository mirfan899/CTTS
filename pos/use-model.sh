#!/bin/sh
# To use: ./use-model.sh {path to props file}
java -mx1g -cp 'stanford-postagger/stanford-postagger-3.9.1.jar:' edu.stanford.nlp.tagger.maxent.MaxentTagger -props $1
