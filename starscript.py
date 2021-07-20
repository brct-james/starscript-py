from SpacePyTraders import client
import logging
import threading
import time
import sys

# logging config
logger = logging.getLogger()
#logging.CRITICAL / .WARNING
logger.setLevel(level=logging.CRITICAL)

# API Setup

USERNAME = "Greenitthe"
TOKEN = "c8283f54-c08f-4773-8c40-fc99b0071a19"

api = client.Api(USERNAME, TOKEN)
print("[GAME API STATUS]", api.game.get_game_status()['status'])

#background thread function (handles running commands)
commandQueue = []
def processCommandQueue():
  while True:
    if (len(commandQueue) > 0):
      interpretCommand(commandQueue.pop(0))

def queueCommand(newComm):
  commandQueue.append(newComm)

def queueAllCommands(newCommList):
  for comm in newCommList:
    queueCommand(comm)

# Plan Helper Functions
def interpretCommand(line):
  cmd = line.split()
  if (cmd[0] == "#" or cmd[0][0] == "#"):
    # print("Comment: ", cmd[1:])
    pass
  elif (cmd[0] == "get"):
    # len(cmd) > # ensures no IndexErrors break threading
    if (len(cmd) > 1 and cmd[1] == "info"):
      info = api.account.info()['user']
      printLevel(1, "User: " + info['username'])
      printLevel(2, "Credits: " + str(info['credits']))
      printLevel(2, "Ships: " + str(info['shipCount']))
      printLevel(2, "Structures: " + str(info['structureCount']))
    elif (len(cmd) > 1 and cmd[1] == "loans"):
      loans = api.loans.get_user_loans()['loans']
      for loan in loans:
        printLevel(1, "Loan ID: " + str(loan['id']))
        printLevel(2, "Type: " + str(loan['type']))
        printLevel(2, "Status: " + str(loan['status']))
        printLevel(2, "Repayment Amount: " + str(loan['repaymentAmount']))
    elif (len(cmd) > 1 and cmd[1] == "loc"):
      if (len(cmd) > 3 and cmd[2] == "info"):
        try:
          loc = api.locations.get_location(cmd[3])['location']
        except Exception as e:
          print("[WARNING] Not a valid location or could not get info (" + str(cmd[3]) + ").")
        else:
          printLevel(1, "Location info for symbol " + str(cmd[3]) + ":")
          printLevel(2, "Name: " + str(loc['name']))
          printLevel(2, "Type: " + str(loc['type']))
          printLevel(2, "Coords: (" + str(loc['x']) + ", " + str(loc['y']) + ")")
          printLevel(2, "Allows Construction: " + str(loc['allowsConstruction']))
          printLevel(2, "Traits:")
          for trait in loc['traits']:
            printLevel(3, str(trait))
          printLevel(2, "Docked Ships: " + str(loc['dockedShips']))
      elif (len(cmd) > 3 and cmd[2] == "ships"):
        try:
          ships = api.locations.get_ships_at_location(cmd[3])['ships']
        except Exception as e:
          print("[WARNING] Not a valid location, or no owned ships at location to provide data. Location: (" + str(cmd[3]) + ").")
        else:
          numShips = len(ships)
          if (numShips > 15):
            printLevel(1, "Too many ships docked, won't print. Number Docked: " + str(len(ships)))
          else:
            printLevel(1, "Ships docked at " + str(cmd[3]) + ":")
            for ship in ships:
              printLevel(2, "Ship Type: " + str(ship['shipType']))
              printLevel(3, "Owner: " + str(ship['username']))
              printLevel(3, "Ship ID: " + str(ship['shipId']))
      elif (len(cmd) > 3 and cmd[2] == "market"):
        try:
          market = api.locations.get_marketplace(cmd[3])['marketplace']
        except Exception as e:
          print("[WARNING] Not a valid location, or no owned ships at location to provide data. Location: (" + str(cmd[3]) + ").")
        else:
          printLevel(1, "Marketplace Listings At " + str(cmd[3]))
          for listing in market:
            printLevel(2, str(listing['symbol']))
            printLevel(3, "Sell Price: " + str(listing['sellPricePerUnit']))
            printLevel(3, "Buy Price: " + str(listing['purchasePricePerUnit']))
            printLevel(3, "Available: " + str(listing['quantityAvailable']))
            printLevel(4, "Volume per Unit: " + str(listing['volumePerUnit']) + ", Spread: " + str(listing['spread']) + ", Price per Unit: " + str(listing['pricePerUnit']))
      else:
        print("[Invalid Command] `" + " ".join(cmd) + "`, GET expects 3rd parameter from list [info, ships, market]")
    elif (len(cmd) > 1 and cmd[1] == "ships"):
      ships = api.ships.get_user_ships()['ships']
      for ship in ships:
        printShipInfo(ship)
    elif (len(cmd) > 2 and cmd[1] == "ship"):
      try:
        ship = api.ships.get_ship(cmd[2])['ship']
      except Exception as e:
        print("[WARNING] Not a valid ship id, or could not get ship details. ID: (" + str(cmd[2]) + ").")
      else:
        printShipInfo(ship)
    else:
      print("[Invalid Command] `" + " ".join(cmd) + "`, GET LOC expects 2nd parameter from list [info, loans, loc, ships, ship]")
  else:
      print("[Invalid Command] `" + " ".join(cmd) + "`, valid plan-level commands are: [get]")

def printLevel(level, text):
  res = "".join([" -"]*(level)) + " " + text
  print(res)

def printShipInfo(ship):
  printLevel(1, "Ship ID: " + str(ship['id']))
  printLevel(2, "Manufacturer: " + str(ship['manufacturer']) + " | Type: " + str(ship['type']) + " | Class: " + str(ship['class']))
  printLevel(2, "Location: " + str(ship['location']) + " | Coordinates: (" + str(ship['x']) + ", " + str(ship['y']) + ")")
  printLevel(2, "Flight Speed: " + str(ship['speed']) + " | Plating: " + str(ship['plating']) + " | Weapons: " + str(ship['weapons']))
  printLevel(2, "Cargo (Current " + str(ship['maxCargo'] - ship['spaceAvailable']) + "/" + str(ship['maxCargo']) + " Max):")
  printLevel(2, "Loading Speed: " + str(ship['loadingSpeed']))
  for good in ship['cargo']:
    printLevel(3, "Good: " + str(good['good']))
    printLevel(4, "Quantity: " + str(good['quantity']) + " | Volume: " + str(good['totalVolume']))

# File Stuff
planfile = open("plans/test.starplan", "r")
plan = planfile.readlines()
planfile.close()

commands = list(map(lambda line: line.strip('\n'), plan))
queueAllCommands(commands)

threadingCQ = threading.Thread(target=processCommandQueue)
threadingCQ.daemon = True
threadingCQ.start()

while True:
  rawcmd = input("").lower()
  if rawcmd == 'exit' or rawcmd == 'stop' or rawcmd == 'quit':
    sys.exit()
  elif rawcmd[0:1] == ':':
    cmd = rawcmd[1:].strip('\n')
    queueCommand(cmd)
  else:
      print("[Invalid Script Command] `" + rawcmd + "`, valid script-level commands are: [exit, stop, quit]")
      printLevel(1, "Use a colon (e.g. `:get info`) to input plan-level commands from terminal")