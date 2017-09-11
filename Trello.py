from trello import TrelloClient
import TrelloConfig as cfg
from re import search
from json import dump

client = TrelloClient(
    api_key = cfg.trello['TRELLO_API_KEY'],
    api_secret = cfg.trello['TRELLO_API_SECRET'],
    token = cfg.trello['OAUTH_TOKEN'],
    token_secret = cfg.trello['OAUTH_TOKEN_SECRET']
)

def dump_board(outfilename):

    activities = []
    members = {}

    boards = client.list_boards()
    for board in boards:
        lsts = board.list_lists()

        for lst in lsts:
            cards = lst.list_cards()
            for card in cards:
                activity = {}
                activity["Board Name"] = board.name
                activity["List Name"] = lst.name
                activity["Card Name"] = card.name
                labels = []
                for label in card.labels:
                    labels.append(label.name)
                activity["Labels"] = labels
                due = card.due
                card_members = []
                idMembers = card.idMembers
                for idMember in idMembers:
                    if members.get(idMember,None) is None: members[idMember] = client.get_member(idMember).full_name
                    card_members.append(members[idMember])
                if not due is None: due = search(r"((19|20)\d{2})-([0-1][0-9])-([0-3][0-9])", due).group(0)
                activity["Due Date"] = due
                activity["Members"] = card_members
                activities.append(activity)

    with open(outfilename, 'w') as outfile: dump(activities, outfile)

    print("Boards exported to %s" % outfilename)
