
from trello import TrelloClient
from datetime import date
from sys import exit
import config

def debug_out(str):
    if config.debug:
        print "-- %s" % str

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

for card in cards:
    if card.description != "":
        out.append("* %s" % card.name)
        out.append("%s" % card.description)
        out.append("")
    else:
        debug_out("Card '%s' has no description text. Skipping" % card.name)

debug_out("Finished generating newsletter.")
debug_out("Generated output:")

print "\n".join(out)
