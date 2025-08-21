# Sanskrit Text Data

# Origin
The `gretril_devanagari.zip` has been downloaded from GRETIL website. 
When unzipped it will be a folder full of text files. 

# Processing
Unzip the `gretril_devanagari.zip` file to `gretril_devanagari/` folder. And run...

```bash
python prepare_a_clean_and_save_txts.py 
```
Will 
 - open each file in the folder
 - clean it to contain only Devanagari and punctuation
 - save all content to devanagari.txt
 - split to train and test
   - save `devanagari_train.txt`
   - save `devanagari_test.txt`

Now you can run...
```bash
 python prepare_b_txt_to_npz.py
```

This will save 
- `devanagari_train.txt` → `devanagari_train.npz`
- `devanagari_test.txt` → `devanagari_test.npz`

# Format

The devanagari text is read into a string. Then each character is encoded using the lookup table in `lookup.py`.
This becomes a `numpy` array of `uint8`. This is saved in the `.npz` files. 
These can be used to load in your application. 
Like the `Sanskrit GPT`!