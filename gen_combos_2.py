#!/usr/bin/env python3
# gen_combos_2.py
# Streams all concatenations of two words (word1 + word2) from a wordlist to stdout.
# Usage:
#   python3 gen_combos_2.py wordlist.txt > combos.txt
#   python3 gen_combos_2.py wordlist.txt | ./hashcat -m 3200 -a 0 hashes.txt --stdin
 
import sys
import argparse
 
def stream_pairs(wordlist_path, skip_self=False, strip=True):
    """
    Streams every concatenation of two words from the given file:
      for w1 in words:
        for w2 in words:
           yield w1 + w2
    If skip_self is True, it will skip pairs where w1 == w2.
    """
    # Read words into memory (needed to iterate twice). If your wordlist is VERY large,
    # consider splitting or using a disk-based approach; this handles typical sizes.
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        words = [line.rstrip('\n') for line in f if line.rstrip('\n')]
 
    total = len(words)
    print(f"# words: {total}. producing {total * total} candidates (including self-pairs)", file=sys.stderr)
    if skip_self:
        print("# skipping self-pairs (w1 == w2)", file=sys.stderr)
 
    for w1 in words:
        for w2 in words:
            if skip_self and w1 == w2:
                continue
            yield f"{w1}{w2}"
 
def main():
    p = argparse.ArgumentParser(description="Stream all word1+word2 combos from a wordlist.")
    p.add_argument('wordlist', nargs='?', default='wordlist.txt', help='path to wordlist (default: wordlist.txt)')
    p.add_argument('--no-self', action='store_true', help='skip pairs where word1 == word2')
    args = p.parse_args()
 
    try:
        for cand in stream_pairs(args.wordlist, skip_self=args.no_self):
            sys.stdout.write(cand + '\n')
    except FileNotFoundError:
        print(f"Error: wordlist not found: {args.wordlist}", file=sys.stderr)
        sys.exit(2)
    except BrokenPipeError:
        # Useful when piping into something that closes early (e.g., head)
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
 
if __name__ == '__main__':
    main()
