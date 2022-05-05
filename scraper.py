import json
import requests
from bs4 import BeautifulSoup

product_id = input("Please enter the product ID:\n").replace(" ", "")
print("Product ID entered. Igniting the Scrape Machine...")

product_url = "https://www.ceneo.pl/" + product_id + "#tab=reviews"

all_opinions = []
opinion_amount = 0

while product_url:
    response = requests.get(product_url)
    page = BeautifulSoup(response.text, "html.parser")
    opinions = page.select("div.js_product-review")

    for opinion in opinions:
        opinion_id = opinion["data-entry-id"]
        author = opinion.select_one("span.user-post__author-name").get_text().strip()
        try:
            recommendation = opinion.select_one("span.user-post__author-recomendation> em.recommended").get_text().strip()
        except AttributeError:
            recommendation = None
        stars = opinion.select_one("span.user-post__score-count").get_text().strip()
        content = opinion.select_one("div.user-post__text").get_text().strip()
        useful = opinion.select_one("button.vote-yes > span").get_text().strip()
        useless = opinion.select_one("button.vote-no > span").get_text().strip()
        published_date = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"]
        try:
            purchased_date = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"]
        except TypeError:
            purchased_date = None
        pros = opinion.select("div[class$=positives] ~ div.review-feature__item")
        pros = [item.get_text().strip() for item in pros]
        cons = opinion.select("div[class$=negatives] ~ div.review-feature__item")
        cons = [item.get_text().strip() for item in cons]

        single_opinion = {
            "opinion_id": opinion_id,
            "author": author,
            "recomendation": recommendation,
            "stars": stars,
            "content": content,
            "useful": useful,
            "useless": useless,
            "published": published_date,
            "purchased": purchased_date,
            "pros": pros,
            "cons": cons
        }

        all_opinions.append(single_opinion)
        opinion_amount += 1

    try:
        product_url = "https://www.ceneo.pl" + page.select_one("a.pagination__next")["href"]
    except TypeError:
        product_url = None

with open("opinions/" + product_id + ".json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)

print(f"Done! Opinions found in the scrapescape: {opinion_amount}.")
