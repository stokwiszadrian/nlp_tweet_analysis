import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import re
import spacy
import datetime
from collections import Counter
import requests as r

nltk.download([
    # "names",
    # "stopwords",
    # "state_union",
    # "twitter_samples",
    # "movie_reviews",
    # "averaged_perceptron_tagger",
    # "vader_lexicon",
    # "punkt",
    # "wordnet",
    # "omw-1.4"
 ])
stopwords = []
with open("stopwords.txt", newline='') as file:
    for line in file.readlines():
        line = line.split("\r")
        stopwords.append(line[0])
file.close()

hashtag = "polswe"
dateformat = "%Y-%m-%d %H:%M:%S"
match_start = datetime.datetime.strptime("2021-06-23 16:00:00", dateformat)
sid = SentimentIntensityAnalyzer()
nlp = spacy.load("pl_core_news_md")
lemmatizer = nlp.get_pipe("lemmatizer")
n = 0
with open(f"tweets_{hashtag}.csv", newline='') as txt:
    with open(f"sentiment_{hashtag}_before.csv", 'w', newline='') as output_before:
        with open(f"sentiment_{hashtag}_after.csv", 'w', newline='') as output_after:
            writer_before = csv.writer(output_before)
            writer_before.writerow(['compound', 'negative', 'neutral', 'positive'])
            writer_after = csv.writer(output_after)
            writer_after.writerow(['compound', 'negative', 'neutral', 'positive'])
            allWordsBefore = []
            allWordsAfter = []
            lines = csv.DictReader(txt)
            regex = re.compile('[^AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż!?.]')
            regex_alph = re.compile(re.compile('[^AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]'))
            for row in lines:
                n += 1
                data = row['date'].split("+")
                data = datetime.datetime.strptime(data[0], dateformat)
                print(data)
                # time.sleep(0.2)
                content = row['content'].split('\n')
                content = " ".join(content)
                content = content.split(" ")
                content = list(filter(lambda s: not s.startswith("http"), content))
                content = list(filter(lambda s: not s.startswith("#"), content))
                content = list(map(lambda s: regex.sub("", s), content))
                content = list(filter(lambda s: len(s) != 0, content))
                lemmatized = nlp(" ".join(content).capitalize())
                content = " ".join(content)
                #print(content)
                if len(content) == 0:
                    continue
                translated = r.post(f"https://translation.googleapis.com/language/translate/v2?key=AIzaSyDiAqiFdn8AFvhAmjLItZpFAGkdYs0hpy8&target=en&q={content}")
                translated = translated.json()['data']['translations'][0]['translatedText']
                print(translated)
                sent = sid.polarity_scores(translated)
                newrow = []
                for k in sorted(sent):
                    newrow.append(sent[k])
                    #print('{0}: {1}, '.format(k, sent[k]), end='')

                if data < match_start:
                    writer_before.writerow(newrow)
                    print("BEFORE")
                else:
                    writer_after.writerow(newrow)
                    print("AFTER")
                print(newrow)

                content = [token.lemma_ for token in lemmatized]
                content = list(map(lambda s: regex_alph.sub("", s), content))
                content = list(map(lambda s: s.lower(), content))
                content = list(filter(lambda s: len(s) != 0, content))
                content = list(filter(lambda s: s != 'u', content))
                content = list(filter(lambda s: s not in stopwords, content))
                if data < match_start:
                    allWordsBefore.extend(content)
                else:
                    allWordsAfter.extend(content)
                # print(allWords)

txt.close()
output_before.close()
output_after.close()
count_before = Counter(allWordsBefore)
count_after = Counter(allWordsAfter)
most_common = count_before.most_common(40)
with open(f"most_common_{hashtag}_before.csv", 'w', newline='') as mc:
    writer = csv.writer(mc)
    writer.writerow(['word', 'count'])
    for entry in most_common:
        writer.writerow([entry[0], entry[1]])

mc.close()

most_common = count_after.most_common(40)
with open(f"most_common_{hashtag}_after.csv", 'w', newline='') as mc:
    writer = csv.writer(mc)
    writer.writerow(['word', 'count'])
    for entry in most_common:
        writer.writerow([entry[0], entry[1]])