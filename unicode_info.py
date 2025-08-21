import requests
import unicodedata

control_names = {}
url = "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt"
response = requests.get(url)
response.raise_for_status()

for i, line in enumerate(response.text.splitlines()):
    fields = line.split(';')
    if len(fields) > 1:
        codepoint = int(fields[0], 16)
        name = fields[10]
        if name != "":
            try:
                name = unicodedata.name(chr(codepoint))
            except:
                control_names[codepoint] = name

def get_char_name(c):
    try:
        name = unicodedata.name(c)
    except ValueError:
        try:
            name = control_names[ord(c)]
        except KeyError:
            name = f"[PRIVATE]"

    return name

def print_char_set(cs):
    for c in sorted(list(cs)):
        print(f"U+{ord(c):04X} {c} {get_char_name(c)}")
