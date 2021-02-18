import requests
import lxml.html
import json

html = requests.get("https://store.steampowered.com/explore/new")
doc = lxml.html.fromstring(html.content)
#           Common XPATH Expressions
# Expression        Description
# nodename          Selects all nodes with the name "nodename"
# /                 Selects from the root node
# //                Selects nodes in the document from the current node that match the selection no matter where they are
# .                 Selects the current node
# ..                Selects the parent of the current node
# @                 Selects attributes
# https://www.w3schools.com/xml/xpath_syntax.asp

#               HTML Structure
# div.tab_content#tab_newreleases_content
#   a.tab_item app_impression_tracked [multiple]
#       div.tab_item_content
#           div.tab_item_name //Text = Game Name
#           div.tab_item_details
#               span.platform_img win [Multiple or singlular] //Ending indicates OS
#               div.tab_item_top_tags
#                   span.top_tag [multiple] //Text = tag

# div.tab_content#tab_newreleases_content
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

# Get game titles
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

# Get game prices
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

# Get game tags
tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = [div.text_content() for div in tags_divs]

# Get platform names for each game
platforms = []
tab_item_details = new_releases.xpath('.//div[@class="tab_item_details"]')
spans = []
for tab in tab_item_details:
    spans.append(tab.xpath('.//span'))
for span in spans:
    plat = []
    for tag in span:
        class_name = tag.classes._attributes['class'][13:]
        if len(class_name) > 0:
            plat.append(class_name)
    platforms.append(",".join(plat))

# Store output in a list of dictionaries
output = []
for title, price, tag, platform in zip(titles, prices, tags, platforms):
    resp = {}
    resp['title'] = title
    resp['tags'] = tag
    resp['price'] = price
    resp['platforms'] = platform
    output.append(resp)

# Dump list of dictionaries to a JSON file
with open('result.json', 'w') as fp:
    json.dump(output, fp)
