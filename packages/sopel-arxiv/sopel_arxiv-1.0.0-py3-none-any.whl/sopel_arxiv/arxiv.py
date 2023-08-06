from functools import partial
from pathlib import PurePath
import requests
import urllib.parse
import xml.etree

from sopel import plugin


ARXIV_PATTS = [
    r"https?://arxiv.org/abs/(?P<arxiv_id>.*)",
    r"https?://arxiv.org/pdf/(?P<arxiv_id>.*)\.pdf",
]
ARXIV_QUERY_URL = "https://export.arxiv.org/api/query?id_list={entryid}"


@plugin.url(*ARXIV_PATTS)
@plugin.output_prefix("[arXiv] ")
def arxiv_summarize(bot, trigger):
    urlinfo = urllib.parse.urlparse(trigger.group(0))
    entryid_raw = PurePath(urlinfo.path).parts[-1]
    entryid = entryid_raw.removesuffix(".pdf")

    response = requests.get(ARXIV_QUERY_URL.format(entryid=entryid))
    response.raise_for_status()

    root = xml.etree.ElementTree.fromstring(response.content)
    ns = {"feed": "http://www.w3.org/2005/Atom"}

    findall = partial(root.findall, namespaces=ns)

    query_title, article_title = (node.text for node in findall(".//feed:title"))
    authors = [node.text for node in findall(".//feed:author/feed:name")]
    try:
        summary = findall(".//feed:summary")[0].text.replace("\n", " ").strip()
    except:
        summary = ""

    if len(authors) <= 3:
        author_list = ", ".join(authors)
    else:
        author_list = ", ".join(authors[:3]) + " et al."


    if summary:
        bot.say(f'“{article_title}” {author_list} — «{summary}', truncation="…", trailing="»")
    else:
        bot.say(f'“{article_title}” {author_list}', truncation="…")
