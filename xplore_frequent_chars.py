from collections import Counter
from typing import Dict, List, Tuple

starts = " \n\x1e\"\'(.।॥"


def find_top_substrings_all_lengths(filepath: str) -> Dict[int, List[Tuple[str, int]]]:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    for length in range(1, 11):
        counter = Counter()
        for i in range(len(text) - length + 1):
            if text[i] in starts:
                counter[text[i + 1:i + length]] += 1

        results = counter.most_common(20)

        print(f"\n=== TOP 20 SUBSTRINGS OF LENGTH {length} ===")
        for i, (substring, count) in enumerate(results, 1):
            display = repr(substring) if length == 1 else f"'{substring}'"
            print(f"{i:2d}. {display:<20} : {count:,} times")