import re
import random
from tqdm import tqdm
from pathlib import Path

allowed_ranges = [(ord(' '), ord('?')), (0x900, 0x97f)] # ASCII Punctuation and Devanagari
allowed_single = {ord(c) for c in '\n\x1e[\\]_{}|'}

def is_allowed(ch: str) -> bool:
    cp = ord(ch)
    if cp in allowed_single:
        return True
    return any(lo <= cp <= hi for lo, hi in allowed_ranges)

def clean_text(text):
    text = text.replace("\r", "\n")
    text = text.replace("\t", "  ")
    text = text.replace("\f", "\x1E")   # form feed -> record separator
    text = text.replace("\u00A0", " ")  # non-breaking space -> space
    text = text.replace("\ufeff", "")   # strip BOM
    text = "".join(ch for ch in text if is_allowed(ch))
    text = re.sub(r"  +", "  ", text)      # Limit spaces to maximum of two
    text = re.sub(r" +\n", "\n", text)     # Delete space at end of line
    text = re.sub(r"\n\n+", "\n\n", text)  # Limit to two consequetive linebreaks
    return text.strip()


def check_dir_exists(input_dir):
    if not Path(input_dir).exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}/\n"
                                f"Extract the zip file to create the directory.\n")


def clean_split_and_save_train_test(input_dir,  output_file, train_out, test_out, train_fraction, seed):
    """
    Clean text files and split them into train/test sets reproducibly.
    Args:
        input_dir: Directory containing .txt files
        output_file: Output path for all data
        train_out: Output path for training data
        test_out: Output path for test data
        train_fraction: Fraction of files to put in training set (0.0 to 1.0)
        seed: Random seed for reproducible splits (default: 42)
    """
    check_dir_exists(input_dir)
    paths = sorted(Path(input_dir).rglob("*.txt"))
    print("Writing training text to ", train_out)
    print("Writing testing text to ", test_out)
    print("Writing all text to ", output_file)

    random.seed(seed)
    with (open(output_file, "w", encoding="utf-8") as allout,
          open(train_out, "w", encoding="utf-8") as trainout,
          open(test_out, "w", encoding="utf-8") as testout):
        for i, f in tqdm(enumerate(paths), desc="Processing files", total=len(paths)):
            raw_text = f.read_text(encoding="utf-8", errors="ignore")
            cleaned = clean_text(raw_text)

            allout.write("\x1E")  # separator between files
            allout.write(cleaned)

            out = trainout if random.random() < train_fraction else testout
            tqdm.write(f"{out.name} ← {f.relative_to(input_dir)}")
            out.write("\x1E")  # separator between files
            out.write(cleaned)

TRAIN_FRAC = 7/8
SEED = 21
clean_split_and_save_train_test("gretil_devanagari",
                                "devanagari.txt",
                                "devanagari_train.txt",
                                "devanagari_test.txt",
                                TRAIN_FRAC, SEED)

train_sz = Path("devanagari_train.txt").stat().st_size / (10**6)
test_sz = Path("devanagari_test.txt").stat().st_size / (10**6)
print(f"Data Size: \n\tTrain:{train_sz:7.2f} \n\tTest:{test_sz:7.2f}"
      f" \n\tTotal:{train_sz+test_sz:7.2f} \n\tRatio:{test_sz/train_sz:.0%}")

