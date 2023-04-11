import requests as r
import json

txt = "Król Karol kupił królowej Karolinie korale koloru koralowego"
abc = r.post(f"https://translation.googleapis.com/language/translate/v2?key=AIzaSyDiAqiFdn8AFvhAmjLItZpFAGkdYs0hpy8&target=en&q={txt}")

print(abc.json()['data']['translations'][0]['translatedText'])