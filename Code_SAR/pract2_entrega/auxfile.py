from typing import Optional

def word_analysis(word):
        if(len(word) > 2):
            pref2 = word[0: 2] + "-"
            suf2 = "-" + word[len(word) - 2: len(word)]
            print(pref2)
            print(suf2)

print(word_analysis("patata"))