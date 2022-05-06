import json
import requests
from bs4 import BeautifulSoup

def get_item(ancestor, selector, attribute=None, return_list=False):
    '''docstring right here'''
    try:
        if return_list:
            return [item.get_text().strip() for item in ancestor.select_one(selector)]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    "opinion_id": ["data-entry-id"],
    "author": ["span.user-post__author-name"],
    "recomendation": ["span.user-post__author-recomendation> em.recommended"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "useful": ["button.vote-yes > span"],
    "useless": ["button.vote-no > span"],
    "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
    "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
}

product_id = input("Please enter the product ID:\n").replace(" ", "")
print("Product ID entered. Igniting the Scrape Machine...")

product_url = f"https://www.ceneo.pl/{product_id}#tab=reviews"

all_opinions = []
opinion_counter = 0
page_counter = 1

while product_url:
    response = requests.get(product_url)
    page = BeautifulSoup(response.text, "html.parser")
    opinions = page.select("div.js_product-review")

    for opinion in opinions:
        single_opinion = {
            key:get_item(opinion, *value)
                for key, value in selectors.items()
    }
        single_opinion["opinion_id"] = opinion["data-entry-id"]

        all_opinions.append(single_opinion)
        opinion_counter += 1

    print(f"Processing page number {page_counter}...")
    page_counter += 1

    try:
        product_url = "https://www.ceneo.pl" + page.select_one("a.pagination__next")["href"]
    except TypeError:
        product_url = None

with open(f"opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)

print(f"Done! Opinions found in the scrapescape: {opinion_counter}.")
