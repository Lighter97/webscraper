import requests
from bs4 import BeautifulSoup
from pathlib import Path
from jinja2 import Template, Environment, PackageLoader, select_autoescape

# Download the target site
site_url = "https://pasmi.ru/"
response = requests.get(site_url)

# Find all DOM elements with proper tag
scraper = BeautifulSoup(response.text, "html.parser")
news_list = scraper.find_all("div", class_="content")

# Limit of parsed news
i = 0
limit = 10

# Filling the dict
news_objects = []
for entry in news_list:
    if i < limit:
        news = {}
        if entry.h2.contents[0].name == "a":
            news["id"] = i
            news["title"] = entry.h2.get_text().replace(u'\ufeff', '')
            news["link"] = entry.h2.a["href"].replace(u'\ufeff', '')
            news["desc"] = entry.p.get_text().replace(u'\ufeff', '') if entry.p else ""
            news_objects.append(news)

            i += 1
    else:
        break

# Render and save the HTML file with results
filename = "result.html"
filepath = Path() / filename

env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)
templatename = "base.html"
template = env.get_template(templatename)

with open(filepath, "w") as file:
    file.write(
        template.render(news=news_objects)
    )
