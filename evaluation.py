import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import re
import spacy
import datetime
from collections import Counter

# nltk.download([
#     # "names",
#     # "stopwords",
#     # "state_union",
#     # "twitter_samples",
#     # "movie_reviews",
#     # "averaged_perceptron_tagger",
#     # "vader_lexicon",
#     # "punkt",
#     # "wordnet",
#     # "omw-1.4"
#  ])
stopwords = []
with open("stopwords.txt", newline='') as file:
    for line in file.readlines():
        line = line.split("\r")
        stopwords.append(line[0])
file.close()

hashtag = "esppol"
dateformat = "%Y-%m-%d %H:%M:%S"
match_start = datetime.datetime.strptime("2021-06-19 19:00:00", dateformat)
sid = SentimentIntensityAnalyzer()
nlp = spacy.load("pl_core_news_md")
lemmatizer = nlp.get_pipe("lemmatizer")
n = 0
with open(f"tweets_{hashtag}.csv", newline='') as txt:
    with open(f"sentiment_{hashtag}_before.csv", newline='') as output_before:
        with open(f"sentiment_{hashtag}_after.csv", newline='') as output_after:

            allWordsBeforePositive = []
            allWordsBeforeNegative = []
            allWordsAfterPositive = []
            allWordsAfterNegative = []
            allWordsAfter = []
            allWordsBefore = []

            lines = csv.DictReader(txt)

            sent_before = csv.DictReader(output_before)
            sent_after = csv.DictReader(output_after)

            regex = re.compile('[^AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż!?.]')
            regex_alph = re.compile(re.compile('[^AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]'))

            compoundTotal = 0.0

            tweetsBeforeNegative = 0
            tweetsBeforePositive = 0
            tweetsAfterNegative = 0
            tweetsAfterPositive = 0
            tweetsBefore = 0
            tweetsAfter = 0

            for row in lines:

                n += 1
                data = row['date'].split("+")
                data = datetime.datetime.strptime(data[0], dateformat)
                print(n)

                sentrow = {}
                try:
                    if data < match_start:
                        tweetsBefore += 1
                        sentrow = next(sent_before)
                        print("BEFORE")
                    else:
                        tweetsAfter += 1
                        sentrow = next(sent_after)
                        print("AFTER")
                    compound = float(sentrow['compound'])
                except StopIteration:
                    compound = 0.0

                if -0.05 < compound < 0.05:
                    continue

                content = row['content'].split('\n')
                content = " ".join(content)
                content = content.split(" ")
                content = list(filter(lambda s: not s.startswith("http"), content))
                content = list(filter(lambda s: not s.startswith("#"), content))
                content = list(map(lambda s: regex.sub("", s), content))
                content = list(filter(lambda s: len(s) != 0, content))

                lemmatized = nlp(" ".join(content).capitalize())

                content = " ".join(content)
                content = [token.lemma_ for token in lemmatized]
                content = list(map(lambda s: regex_alph.sub("", s), content))
                content = list(map(lambda s: s.lower(), content))
                content = list(filter(lambda s: len(s) != 0, content))
                content = list(filter(lambda s: s != 'u', content))
                content = list(filter(lambda s: s not in stopwords, content))

                if data < match_start:
                    allWordsBefore.extend(content)
                    if compound >= 0.05:
                        allWordsBeforePositive.extend(content)
                        tweetsBeforePositive += 1
                    else:
                        allWordsBeforeNegative.extend(content)
                        tweetsBeforeNegative += 1
                else:
                    allWordsAfter.extend(content)
                    if compound >= 0.05:
                        allWordsAfterPositive.extend(content)
                        tweetsAfterPositive += 1
                    else:
                        allWordsAfterNegative.extend(content)
                        tweetsAfterNegative += 1
                compoundTotal += compound

txt.close()
output_before.close()
output_after.close()

print(f"TWEETS TOTAL: {n}")
print(f"TWEETS BEFORE: {tweetsBefore}")
print(f"POSITIVE TWEETS BEFORE: {tweetsBeforePositive}")
print(f"NEGATIVE TWEETS BEFORE: {tweetsBeforeNegative}")
print(f"TWEETS AFTER: {tweetsAfter}")
print(f"POSITIVE TWEETS AFTER: {tweetsAfterPositive}")
print(f"NEGATIVE TWEETS AFTER: {tweetsAfterNegative} \n")

print(f"AVERAGE COMPOUND: {compoundTotal / n}, {compoundTotal}")

count_before = Counter(allWordsBefore)
count_after = Counter(allWordsAfter)
count_before_positive = Counter(allWordsBeforePositive)
count_before_negative = Counter(allWordsBeforeNegative)
count_after_positive = Counter(allWordsAfterPositive)
count_after_negative = Counter(allWordsAfterNegative)
most_common = count_before_positive.most_common(40)

with open(f"most_common_{hashtag}_before_positive.csv", 'w', newline='') as mc:
    writer = csv.writer(mc)
    writer.writerow(['word', 'count'])
    for entry in most_common:
        writer.writerow([entry[0], entry[1]])

mc.close()

most_common = count_before_negative.most_common(40)
with open(f"most_common_{hashtag}_before_negative.csv", 'w', newline='') as mc:
    writer = csv.writer(mc)
    writer.writerow(['word', 'count'])
    for entry in most_common:
        writer.writerow([entry[0], entry[1]])

mc.close()

most_common = count_after_positive.most_common(40)
with open(f"most_common_{hashtag}_after_positive.csv", 'w', newline='') as mc:
    writer = csv.writer(mc)
    writer.writerow(['word', 'count'])
    for entry in most_common:
        writer.writerow([entry[0], entry[1]])

mc.close()

most_common = count_after_negative.most_common(40)
with open(f"most_common_{hashtag}_after_negative.csv", 'w', newline='') as mc:
    writer = csv.writer(mc)
    writer.writerow(['word', 'count'])
    for entry in most_common:
        writer.writerow([entry[0], entry[1]])

mc.close()

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

mc.close()
