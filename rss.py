import feedparser
import html2text

def convert_text_to_md():
    d = feedparser.parse('https://fbis251.github.io/overwatch_news_feed/pc.atom')
    returnstuff = ""
    for post in d.entries:
        output = (post.title.encode('ascii', 'ignore').decode('ascii'))
        output = output + ("\n=====================================")
        html = (post.summary.encode('ascii', 'ignore').decode('ascii'))
        text = html2text.html2text(html)
        returnstuff = returnstuff + output + text
    return returnstuff

def check_for_update():
    d = feedparser.parse('https://fbis251.github.io/overwatch_news_feed/pc.atom')
    post = d.entries[0]
    title = post.title.encode('ascii', 'ignore').decode('ascii')
    print(title)

check_for_update()
#print(convert_text_to_md())
