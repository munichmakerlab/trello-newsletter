from trello import TrelloClient
from datetime import date
from sys import exit, argv
from email.message import Message
import smtplib
from textwrap import wrap

import config

def debug_out(str):
    if config.debug:
        print "-- %s" % str

if len(argv) != 2 or argv[1] not in ["preview", "final"]:
    print "Usage: newsletter.py [preview|final]"
    exit(1)

client = TrelloClient(
    api_key=config.api_key,
    api_secret=config.api_secret,
    token=config.token,
    token_secret=config.token_secret
)

org_name = config.org_name
brd_name = config.brd_name

year = date.today().isocalendar()[0]
week = date.today().isocalendar()[1]
list_name = "%04d-%02d" % (year,week)

out = []

orgs = filter(lambda x: x.name == org_name, client.list_organizations())
if len(orgs) != 1:
    print "Error while filtering organzation"
    exit(1)

debug_out("Organization found")

brds = filter(lambda x: x.name == brd_name, orgs[0].get_boards("open"))
if len(brds) != 1:
    print "Error while filtering boards"
    exit(1)

debug_out("Board found")

lists = filter(lambda x: x.name == list_name, brds[0].get_lists("open"))

if len(lists) != 1:
    print "Error while filtering lists"
    exit(1)

cards = lists[0].list_cards()

debug_out("List found, with %s cards" % len(cards))

if len(cards) == 0:
    print "Empty list. Not sending anything"
    exit(1)

for card in cards:
    if card.description != "":
        out.append("* %s" % card.name)
        out += wrap(card.description)
        out.append("")
    else:
        debug_out("Card '%s' has no description text. Skipping" % card.name)

subject = "MuMaNews - CW %02d" % week

if argv[1] == "preview":
    subject = "[PREVIEW] %s" % subject

out = wrap(config.pre_bullet_points) + [""] + out + wrap(config.post_bullet_points)
body = "\n".join(out)

debug_out("Finished generating newsletter.")
debug_out("Generated output:")
print "Subject: %s" % subject
print
print body

if argv[1] == "preview":
    rcpt = config.MAIL_TO_PREVIEW
elif argv[1] == "final":
    rcpt = config.MAIL_TO

msg = Message()
msg.set_payload(body, "utf-8")
msg["Subject"] = subject
msg["From"] = config.MAIL_FROM
msg["To"] = rcpt

debug_out("Sending message")
server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
server.ehlo()
server.starttls()
server.ehlo()
server.login(config.SMTP_USER, config.SMTP_PASS)
text = msg.as_string()
server.sendmail(config.MAIL_FROM, rcpt.split(","), text)
server.quit()
