from urllib.request import urlopen
import re, os
from utils import run_command, langcode2name

WMT_CC_LIST_URL = 'http://data.statmt.org/ngrams/raw/'

def get_all_urls_from_website(website):
    website = urlopen(WMT_CC_LIST_URL)
    html = str(website.read())
    links = re.findall('"((http)s?://.*?)"', html)
    return [url for url, _ in links]

def gen_downloader(script, links):
    script.write('echo Downloading files...\n\n')
    for link in links:
        script.write('axel %s\n' % link)
    
    script.write('\necho Extracting files...\n')
    script.write('unxz -kv *.xz\n')
    script.write('# rm *.xz\n')
    return

def gen_all_CC_urls(lang):
    print('Retrieving %s' % WMT_CC_LIST_URL)
    links = get_all_urls_from_website(WMT_CC_LIST_URL)
    pattern = '/raw/' + lang + '.20'
    links = [url for url in links if pattern in url]
    
    log_dir = os.path.join('downloads', langcode2name(lang))
    os.makedirs(log_dir, exist_ok=True)
    bash_script = os.path.join(log_dir, 'downloader.sh')
    script = open(bash_script, 'w')
    gen_downloader(script, links)
    script.close()
    run_command('chmod 777 ' + bash_script)
    
    print('Now go into ./%s/ and use ./downloader.sh to download and extract raw data!' % log_dir)
    return links

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang_code", required=True, type=str)
    args = parser.parse_args()
    gen_all_CC_urls(args.lang_code)