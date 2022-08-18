# Forked from [wswu/trabina](https://github.com/wswu/trabina)

We wanted to use, and add to, the "Translation Matrix of the Bible's Names Across 591 Languages." Created by  Winston Wu, Nidhi Vyas, and David Yarowsky at John's Hopkins University. 

The SILNLP tools for machine translation currently don't do a good job of translating names. They are able to make good use of a dictionary of names. Further improvements to the accuracy of translation are achieved when the names come with a list of the verses in which they occur.

This is in early stages now in August 2022. The main addition is the data from the assets folder of the [silnlp](https://github.com/sillsdev/silnlp/tree/master/silnlp/assets) repo. These contain lists of names and terms along with the verse references in which they occur. 

The main code addition is match_biblical_names.ipynb,  a jupyter notebook for experimenting with various ways of combining the data.



## Original Readme for [wswu/trabina](https://github.com/wswu/trabina)

Transliteration of Bible names. Requires Python 3.6 and [Unidecode](https://pypi.python.org/pypi/Unidecode) for computing a baseline.

Set the relevant paths in `train-{system}.sh` and run with

    python makejobs.py
    qsub translit.sh

For failed runs, resubmit with

    python checkfailed.py -exec

Bible names translation matrix in `data`. Transliteration output in `trabina-output`.

Citations

- *Creating a Translation Matrix of the Bible's Names Across 591 Languages.* Winston Wu, Nidhi Vyas, and David Yarowsky (2018).
- *A Comparative Study of Extremely Low-Resource Transliteration of the World's Languages.* Winston Wu and David Yarowsky (2018).
