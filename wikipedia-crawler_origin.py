#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import argparse
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from pypinyin import pinyin, Style

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from urllib.parse import unquote

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# DEFAULT_OUTPUT = 'output.txt'
DEFAULT_INTERVAL = 5.0  # interval between requests (seconds)
DEFAULT_ARTICLES_LIMIT = 1  # total number articles to be extrated
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

visited_urls = set()  # all urls already visited, to not visit twice
pending_urls = []  # queue


def load_urls(session_file):
    """Resume previous session if any, load visited URLs"""

    try:
        with open(session_file) as fin:
            for line in fin:
                visited_urls.add(line.strip())
    except FileNotFoundError:
        pass


def scrap(base_url, article, output_file, session_file):
    """Represents one request per article"""

    full_url = base_url + article
    print(f"going to scrap {unquote(full_url)}")

# pip install --upgrade certifi

    # try:
        # r = requests.get(full_url, headers={'User-Agent': USER_AGENT})
    r = requests.get(full_url, headers={'User-Agent': USER_AGENT},verify=False)
    # except requests.exceptions.ConnectionError:
    #     print(f"Check your Internet connection as we see {requests.exceptions.ConnectionError}")
    #     input("Press [ENTER] to continue to the next request.")
    #     return

    if r.status_code not in (200, 404):
        print("Failed to request page (code {})".format(r.status_code))
        input("Press [ENTER] to continue to the next request.")
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    
    content = soup.find('div', {'id':'mw-content-text'})

    h2 = soup.findAll('h2')

    h3 = soup.findAll('h3')
    print(f"h2===========================\n")
    # print(h2)

    # <span class="mw-headline" 
    for h in h2:
        # print(h)
        if len(h) > 1: #TypeError: slice indices must be integers or None or have an __index__ method
            for x in h.find('span', {'class':'mw-headline'}):
                print(x)
        else:
            continue

    # print(f"h3===========================\n")
    # for h in h3.find('span', {'class':'mw-headline'}):
    #     print(h)


    with open(session_file, 'a') as fout:
        fout.write(full_url + '\n')  # log URL to session file

    # add new related articles to queue
    # check if are actual articles URL
    for a in content.find_all('a'):
        href = a.get('href')
        if not href:
            continue
        if href[0:6] != '/wiki/':  # allow only article pages
            continue
        elif ':' in href:  # ignore special articles e.g. 'Special:'
            continue
        elif href[-4:] in ".png .jpg .jpeg .svg":  # ignore image files inside articles
            continue
        elif base_url + href in visited_urls:  # already visited
            continue
        if href in pending_urls:  # already added to queue
            continue
        pending_urls.append(href)

    # skip if already added text from this article, as continuing session
    if full_url in visited_urls:
        return
    visited_urls.add(full_url)

    parenthesis_regex = re.compile('\(.+?\)')  # to remove parenthesis content
    citations_regex = re.compile('\[.+?\]')  # to remove citations, e.g. [1]

    # get plain text from each <p>
    p_list = content.find_all('p')
    with open(output_file, 'a', encoding='utf-8') as fout:
        for p in p_list:
            text = p.get_text().strip()
            text = parenthesis_regex.sub('', text)
            text = citations_regex.sub('', text)
            if text:
                fout.write(text + '\n\n')  # extra line between paragraphs


def main(initial_url, articles_limit, interval, output_file):
    """ Main loop, single thread """

    minutes_estimate = interval * articles_limit / 60
    print("This session will take {:.1f} minute(s) to download {} article(s):".format(minutes_estimate, articles_limit))
    print("\t(Press CTRL+C to pause)\n")
    
    session_file = "./outputs/session_" + output_file

    load_urls(session_file)  # load previous session (if any)
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(initial_url))
    initial_url = initial_url[len(base_url):]
    pending_urls.append(initial_url)

    counter = 0
    while len(pending_urls) > 0:
        try:
            counter += 1
            if counter > articles_limit:
                break
            try:
                next_url = pending_urls.pop(0)
            except IndexError:
                break

            time.sleep(interval)
            article_format = next_url.replace('/wiki/', '')[:35]
            print("{:<7} {}".format(counter, article_format))
            scrap(base_url, next_url, f"./outputs/{output_file}", session_file)
        except KeyboardInterrupt:
            input("\n> PAUSED. Press [ENTER] to continue...\n")
            counter -= 1

    print("Finished!")
    sys.exit(0)

# This is the entry point of whole program ...
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("initial_url", help="Initial Wikipedia article, e.g. https://en.wikipedia.org/wiki/Biology")
    parser.add_argument("-a", "--num_articles", nargs='?', default=DEFAULT_ARTICLES_LIMIT, type=int, help="Total number of linked articles from base url")
   
    parser.add_argument("-i", "--interval", nargs='?', default=DEFAULT_INTERVAL, type=float, help="Interval between requests")
    # parser.add_argument("-o", "--output", nargs='?', default=DEFAULT_OUTPUT, help="File output")
   

    args = parser.parse_args()
    


    # parsed_url = urlparse(args.initial_url)

    art_name=unquote(args.initial_url.split('/')[-1])
    print (f"art_name:{art_name}")
    py=(pinyin(art_name, style=Style.NORMAL))
    pyname="_".join([word[0].strip("'") for word in py])
    output = f"{pyname}.txt"

    print("save to :", output)


    main(args.initial_url, args.num_articles, args.interval, output)
