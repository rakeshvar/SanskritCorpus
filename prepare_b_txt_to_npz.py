from pathlib import Path
from unicode_info import print_char_set
import numpy as np

print("Reading Train Text")
train_char_set = set(Path("devanagari_train.txt").read_text())
print("Reading Test Text")
test_char_set = set(Path("devanagari_test.txt").read_text())

all_char_set = train_char_set | test_char_set
only_in_train = train_char_set - test_char_set
only_in_test = test_char_set - train_char_set

print("\nCharacterSet TRAIN")
print_char_set(train_char_set)
print("\nCharacterSet TrainOnly")
print_char_set(only_in_train)

print("\nCharacterSet TEST")
print_char_set(test_char_set)
print("\nCharacterSet TestOnly")
print_char_set(only_in_test)
if len(only_in_test) > 0 :
    print("WARNING: There are characters in Test that are not in train.\n"
          "         Use different seed to generate splits.")

print("\nCharacterSet All")
print_char_set(all_char_set)

stoi = {c:i for i, c in enumerate(sorted(list(all_char_set)))}
itos = {i:c for c, i in stoi.items()}

if False:
    with open("lookup.py", "w") as f:
        f.write(f"stoi={stoi}\nitos={itos}\n")
        f.write("""
def encode(s):
    return [stoi[c] for c in s]
def decode(l):
    return "".join([itos[i] for i in l])
""")

def encode(s):
    return [stoi[c] for c in s]
def decode(l):
    return "".join([itos[i] for i in l])

def save_text_to_bin(txt_file):
    in_path = Path(txt_file)
    out_path = in_path.with_suffix(".npz")
    encoded_data = encode(in_path.read_text())
    print(f"Saving {txt_file} to {out_path.name}")
    np.savez_compressed(out_path, data=np.array(encoded_data, dtype=np.uint8))

save_text_to_bin("devanagari_train.txt")
save_text_to_bin("devanagari_test.txt")
