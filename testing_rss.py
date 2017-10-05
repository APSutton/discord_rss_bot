import feedparser
import time
import html2text
import discord
import asyncio
from datetime import datetime as dt

# create a new client
client = discord.Client()

# secret token
#token = "MzM1NTE0OTg5MDI2NzM4MTc3.DErFJQ.T0gKkvzsZPzD67y371cbD-ez_EQ"
token = 'MzMwMjE1NTgyNTU5NjMzNDA4.DLXDIQ.Si0YVqcY5KYJHMGOHDWNx5Vsjhk'
#token = 'MzMwMjE1NTgyNTU5NjMzNDA4.DDd2HQ.4H4Tr1pEbPaLmWgaoMGvAeYnDvU'
#token = 'MzY0OTM0ODQ4ODY5MTcxMjAw.DLXAQg.cT76Uc2qHNrD4q21OLisKXHo0CY'
# app_id from discord developer's app creation section
app_id = '8KHGJP-YY7AKKGGWU'
# channel_id for Nocturne-testing
channel_id_primary = '343973348658774016'
# channel_id for James' server
channel_id = '279350547260112896'
rss_url = 'https://fbis251.github.io/overwatch_news_feed/pc.atom'

global previousTitle
global count
count = 0
previousTitle = ''

# parses rss and converts the html to markdown
def convert_text_to_md():
    d = feedparser.parse(rss_url)
    returnstuff = ""
    # use the most recent post
    post = d.entries[0]
    output = (post.title.encode('ascii', 'ignore').decode('ascii'))
    output = output + ("\n---------------------------------------\n")
    html = (post.summary.encode('ascii', 'ignore').decode('ascii'))
    text = html2text.html2text(html)
    returnstuff = returnstuff + output + text
    return returnstuff

def need_to_update():
    global previousTitle
    d = feedparser.parse(rss_url)
    post = d.entries[0]
    title = post.title.encode('ascii', 'ignore').decode('ascii')
    if title != previousTitle:
        previousTitle = title
        return 1
    
async def unixReport():
    global count
    while True:
        if dt.now().minute == 0: #if you want to add channels, then add more await bot.send_message stuff idk
            if count == 0:
                count = 1
                if need_to_update(): 
                    message = convert_text_to_md()

                    if len(message) > 1500:
                        position = 0
                        end = 1500
                        go = 1
                        while (go > 0):
                            info = '..' + message[position:end] + '..'
                            await client.send_message(client.get_channel(channel_id), info)
                            await client.send_message(client.get_channel(channel_id_primary), info)
                            position = position + 1500
                            end = end + 1500
                            if go == 2:
                                go = 0
                                break
                            if end > (len(message) - 1):
                                end = len(message)-1
                                go = 2
                    else:
                        await client.send_message(client.get_channel(channel_id), message)
                        await client.send_message(client.get_channel(channel_id_primary), messaage)
        elif dt.now().minute == 1:
            count = 0
        await asyncio.sleep(1)

# runs when the client first connects
@client.event
async def on_ready():
    global count
    global xtime
    xtime = str(dt.now())
    asyncio.get_event_loop().create_task(unixReport())

    # print info to terminal
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # print connected servers
    for server in client.servers:
        print(server.name)
    print('------')

# runs when a member joins the server
# (only once, when they're invited)
@client.event
async def on_member_join(member):
    message = "```Hello! I'll keep you updated on OverWatch news!```"
    tmp = await client.send_message(member.server, message)


# this runs when any message is sent in a connected channel
#@client.event
#async def on_message(message):


client.run(token)
