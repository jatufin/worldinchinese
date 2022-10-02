#!/usr/bin/python
import sys
import codecs

# the csv files are in format
# key;lang1;lang2;lang3
# key1;word1_lang1;word1_lang2; ...
# key2;word2_lang2;word2_lang2; ...

# usage csv2pages.py file1.csv file2.csv file3.csv

def handleFile(basename):
    csv_file = basename + ".csv"
    js_file = basename + ".js"
    html_file = basename + ".html"

    IN_FILE = open("QUIZBASE.HTML","r")
    html_string = IN_FILE.read()
    IN_FILE.close()

    OUT_FILE = open(html_file, "w")
    s = html_string.replace("%%JS_FILENAME%%", js_file)
    OUT_FILE.write(s)
    OUT_FILE.close()

    print '<p><a href="%s" target="quiz">%s</a></p>' % (html_file, basename)
    
    IN_FILE = codecs.open(csv_file,"r", "utf-8")
    lines = IN_FILE.readlines()
    IN_FILE.close()

    JS_FILE = codecs.open(js_file,"w", "utf-8")

    langs = lines[0].strip().replace('"', '').split(",")[1:]


    langs_sorted = langs[:]
    langs_sorted.sort()
    
    s = "langs = ["
    for lang in langs_sorted:
        s += '"' + lang + '",'

    s = s[:-1] + "];\n\n"

    JS_FILE.write(s)
    JS_FILE.write("wlist = new WordList();\n\n")

    s = "deflang1 = '%s';\n" % langs[0]
    JS_FILE.write(s)
    s = "deflang2 = '%s';\n" % langs[1]
    JS_FILE.write(s)

    for line in lines[1:]:
        words = line.strip().replace('"', '').split(",")
        key = words[0]
        for lang, word in zip(langs, words[1:]):
            s = 'wlist.setWord("%s", "%s", "%s");\n' % (key, lang, word)
            JS_FILE.write(s)

    JS_FILE.close()


for filename in sys.argv[1:]:
    handleFile(filename.replace(".csv", ""))

               



