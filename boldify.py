
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Make sure to download once
# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('stopwords')

def boldify_text(text, top_n=5):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in words if w.isalpha() and w not in stop_words]
    common = [word for word, _ in Counter(filtered).most_common(top_n)]

    # Apply bold
    for word in set(common):
        text = text.replace(word, f"\033[34m{word}\033[0m")
    return text

while True:
    text = input("Enter text to boldify (or 'exit' to quit): ")
    if text.lower() == 'exit':
        break
    print(boldify_text(text))

"""
def test_ansi_codes():
    for code in range(0, 48):
        print(f"\033[{code}mCode {code}: This is a test string.\033[0m")

if __name__ == "__main__":
    test_ansi_codes()
"""

