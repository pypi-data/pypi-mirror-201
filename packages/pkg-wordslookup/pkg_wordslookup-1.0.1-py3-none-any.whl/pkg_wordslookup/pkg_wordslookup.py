from string import punctuation
def load_text(input_file):
    """Load text from a text file and return it as a string"""
    with open(input_file, "r") as file:
        text = file.readlines()
    return text

def clean_text(text):
    """Lowercase and remove punctuation from a string"""
    text = text.lower()
    for p in punctuation:
        text = text.replace(p,"")
    return text

def words_lookup(input_file, input_word):
    text = load_text(input_file)
    n = 0
    result = ""
    for line in text:
        line = clean_text(line)
        if input_word in line:
            result = result + line
            n+=1
    summary = "\nThe word \"{}\" appeared {} times".format(input_word, n)
    result = result + summary
    print(summary)
    return result