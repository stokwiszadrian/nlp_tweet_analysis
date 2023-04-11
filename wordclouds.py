from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import csv
import matplotlib.pyplot as plt
words = []
with open("most_common_polswe_after_negative.csv") as f:
    rows = csv.DictReader(f)
    for row in rows:
        if row['word'] != 'd':
            words.append(row['word'])

f.close()
print(words)
r = r"[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż!?.*]+"
wordcloud = WordCloud(max_font_size=100, max_words=25, width=1200, height=600, background_color="black", regexp=r, colormap="Reds_r").generate(" ".join(word for word in words))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()