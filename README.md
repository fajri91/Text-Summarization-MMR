# TextSummarization-MMR

MMR (Maximum Maarginal Relevance) is an extractive summarization that was introduced by Jaime Carbonell and Jade Goldstein.
http://repository.cmu.edu/cgi/viewcontent.cgi?article=1330&context=compsci

MMR aims to obtain the most relevance sentences by scoring whole sentences in the document.
The MMR criterion strives to reduce redudancy while maintaining the content relevance in re-ranking retireved sentences

## Dependency

- This code is implemented in Python
- Since I built it for Bahasa Indonesia, I use Sastrawi libary for stemming ```pip install Sastrawi```
- The list of stopwords in Bahasa Indonesia (as provided in this folder)
- It also use "sklearn libarary". Please install it by ```pip install sklearn```
- And this one ```pip install termcolor```

## How to run

- In you terminal type it as ```python mmr.py [Document.txt]```

## Output

![MMR Output](https://github.com/fajri91/document/blob/master/mmr.jpg)
