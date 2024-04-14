# wikipedia-crawler
Extracts plain-text from series of Wikipedia articles and saves to a local text file.

The goal is to have text samples of a specific language on a specific topic, so the output can be used on computer analysis applied to linguistics (word frequency, distribution, etc), **or to generate wordlists of any language on Wikipedia (294 languages)**.

## Usage:

```
python3 wikipedia-crawler.py https://en.wikipedia.org/wiki/Biology
```
Generates `output.txt`, extracting only a single article. **Parameters to go crawling:**
```
--articles=10 --interval=5 --output=biology.txt 
```

Generates [`biology.txt`](https://raw.githubusercontent.com/AndreiRegiani/wikipedia-crawler/master/example_output/biology_english.txt), crawling `10` articles related to `Biology`. Requests interval set to `5` seconds (default) to not abuse their servers.
Session log containing all visited URLs is saved as `session_biology.txt`. Running with the same output will use the same session file.

In this example the initial article is [Biology](https://en.wikipedia.org/wiki/Biology), the crawler will continue extracting related pages: [Natural Science](https://en.wikipedia.org/wiki/Natural_science), [Evolution](https://en.wikipedia.org/wiki/Evolution), ...

## Dependencies:
* [BeautifulSoap 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](http://docs.python-requests.org/)

```
<!-- It need python3.9 -->
conda create -n web_crawler python=3.9
conda activate web_crawler


<!-- also to avoid ssl issue you need run  -->
pip install --upgrade certifi
<!-- then run the dependencies  -->
pip install -r requirements.txt
```



## Updates 
The new versiion will take all the urls in ./inputs/target_urls.txt file , run them one by one and save output into outputs file, also the session outputs there.

to batch run we run 
```
./wikipedia-batch-crawler.sh

```