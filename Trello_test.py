import Trello
from os.path import dirname, exists
from os import remove

#outdir = dirname(__file__)
outdir = "V:/PBI/DATA"
outfilename = "%s/Trello.json" % outdir

remove(outfilename) if exists(outfilename) else None

Trello.dump_board(outfilename)
