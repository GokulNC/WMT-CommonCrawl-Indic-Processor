import os, sys, pickle
import string, re
from glob import glob
from tqdm import tqdm
from mmh3 import hash128

from utils import langcode2script, in_script, get_digits, load_pickle, num_lines_in_file, langcode2name

from indicnlp.tokenize.sentence_tokenize import sentence_split
from indicnlp.tokenize.indic_tokenize import trivial_tokenize
from indicnlp import common, loader
common.set_resources_path(os.environ['INDIC_RESOURCES_PATH'])
loader.load()


format_str = '%30s %11d %9d\n'
def save_result(fid, result_src, result, out_file, all_results=None):
    if fid==0: # Write Header
        out_file.write('%30s %11s %9s\n' % ('FILENAME', 'TOKENS', 'SENTENCES'))
    
    out_file.write(format_str % (os.path.basename(result_src), result['tokens'], result['sentences']))
    if not all_results is None:
        for stat in result:
            all_results[stat] += result[stat]
    return

all_puncs = set(string.punctuation+'\u0964\u0965')
def process_sentence(s, lang, script, normalizer, native_digits, min_tokens=5):
    s = normalizer.normalize(s)
    
    # Remove both eng and indic numbers
    num_masked = re.sub(r'[0-9]+\.?[0-9]+', '#', s)
    num_masked = re.sub(native_digits, '#', num_masked)
    
    # Tokenize and remove punctuation tokens
    tokens = trivial_tokenize(num_masked, lang)
    true_tokens = list(filter(lambda x: x not in all_puncs, tokens))
    spaced_sent = ' '.join(tokens)
    
    if len(true_tokens) < min_tokens:
        return None
    
    # If sentence has non-indic chars, drop it
    for c in spaced_sent:
        if not in_script(c, script): return None
    return true_tokens, spaced_sent
    
def process_raw(input_file, lang, normalizer, f_out, token_set, sent_hashes):
    token_count, sentence_count = 0, 0
    new_tokens = 0
    reader = open(input_file, 'r', encoding='utf-8', errors='replace')
    
    script = langcode2script(lang)
    native_digits = r'[{}]+'.format(get_digits(script))
    
    print('Processing %s' % input_file)
    for line in tqdm(reader, unit='lines', total=num_lines_in_file(input_file)):
        line = line.strip()
        if not line or 'http' in line: continue
        for sent in sentence_split(line, lang):
            if not sent: continue
            result = process_sentence(sent, lang, script, normalizer, native_digits)
            if not result is None:
                tokens, sent = result
                sentence_count += 1
                token_count += len(tokens)
                hash = hash128(' '.join(tokens))
                if hash not in sent_hashes:
                    sent_hashes.add(hash)
                    token_set.update(tokens)
                    new_tokens += len(tokens)
                    f_out.write(sent); f_out.write('\n')
    reader.close()
    return {'tokens': token_count, 'sentences': sentence_count}, new_tokens

def parse_and_store(raw_folder, output_file, lang, start_index=0):
    raw_files = sorted(glob(os.path.join(raw_folder, '*.raw')))
    
    log_dir = os.path.join('logs', langcode2name(lang))
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    tokens_dump = os.path.join(log_dir, 'tokens.pkl')
    sent_hashes_dump = os.path.join(log_dir, 'sent_hashes.pkl')
    
    from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
    normalizer = IndicNormalizerFactory().get_normalizer(lang)
    
    if start_index == 0:
        token_set, sent_hashes = set(), set()
        out_mode = 'w'
    else:
        print('--- APPEND MODE ---')
        token_set = load_pickle(tokens_dump, default=set())
        sent_hashes = load_pickle(sent_hashes_dump, default=set())
        out_mode = 'a'
    
    if not output_file: output_file = os.path.join(log_dir, 'parsed_final.txt')
    f_out = open(output_file, out_mode, encoding='utf-8', buffering=128*1024*1024) #, errors='ignore')
    stats_file = os.path.join(log_dir, 'stats.log')
    stats_out = open(stats_file, out_mode, buffering=1)
    print('WRITING OUTPUT to %s and LOGS to %s\n' % (output_file, stats_file))
    
    stats = {'tokens': 0, 'sentences': 0}
    total_tokens = 0
    
    for fid, file in enumerate(raw_files, start_index):
        result, new_tokens = process_raw(file, lang, normalizer, f_out, token_set, sent_hashes)
        
        print('Saving results...\n')
        save_result(fid, file, result, stats_out, stats)
        total_tokens += new_tokens
        f_out.write('\n\n')
        
        with open(tokens_dump, 'wb') as fp:
            pickle.dump(token_set, fp)
            
        with open(sent_hashes_dump, 'wb') as fp:
            pickle.dump(sent_hashes, fp)
    
    save_result(-1, 'TOTAL STATS', stats, stats_out)
    unique_stats = {'tokens': len(token_set), 'sentences': len(sent_hashes)}
    save_result(-1, 'UNIQUE STATS', unique_stats, stats_out)
    
    stats_out.write('\n%30s %11d\n' % ('TOTAL OBTAINED TOKENS', total_tokens))
    f_out.close(); stats_out.close()
    return unique_stats

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, type=str)
    parser.add_argument("--out_file", type=str)
    parser.add_argument("--lang_code", required=True, type=str)
    parser.add_argument("--start_index", default=0, type=int)
    args = parser.parse_args()
    parse_and_store(args.folder, args.out_file, args.lang_code, int(args.start_index))