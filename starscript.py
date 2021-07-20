from SpacePyTraders import client
import logging
import threading
import time
import sys

# clear console
import os
os.system('cls' if os.name == 'nt' else 'clear')

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
  elif (cmd[0] == "help"):
    printlv(-1)
    if len(cmd) == 1:
      printlv(0, "Available Plan Commands")
      printlv(1, "get | Gets info from api, args specify what is requested")
      printlv(2, "info | Gets info about the player's account (e.g. credits, shipCount, etc.)")
      printlv(2, "loans | Gets info about loans associated with the player's account")
      printlv(2, "loc | Gets info about a specified location based on the argument supplied")
      printlv(3, "info <locId> | Gets info about the specified location and its features")
      printlv(3, "ships <locId> | [Must have ship at location] Gets info on the ships docked at the specified location")
      printlv(3, "market <locId> | [Must have ship at location] Gets info on the market data for the specified location")
      printlv(2, "ships | Gets info on all ships owned by the player")
      printlv(2, "ship <shipId> | Gets info for the specified ship")
      # printlv(1, "get | ")
      # printlv(1, "get | ")
    elif len(cmd) == 2:
      printlv(0, "Detailed help for " + cmd[1])
      printlv(1, "WIP - see .starcommands on roadmap")
    printlv(-1)
  elif (cmd[0] == "get"):
    # len(cmd) > # ensures no IndexErrors break threading
    if (len(cmd) > 1 and cmd[1] == "info"):
      info = api.account.info()['user']
      printlv(-1)
      printlv(1, "User: " + info['username'])
      printlv(2, "Credits: " + str(info['credits']))
      printlv(2, "Ships: " + str(info['shipCount']))
      printlv(2, "Structures: " + str(info['structureCount']))
      printlv(-1)
    elif (len(cmd) > 1 and cmd[1] == "loans"):
      loans = api.loans.get_user_loans()['loans']
      printlv(-1)
      printlv(0, "Loans associated with user:")
      for loan in loans:
        printlv(-1)
        printlv(1, "Loan ID: " + str(loan['id']))
        printlv(2, "Type: " + str(loan['type']))
        printlv(2, "Status: " + str(loan['status']))
        printlv(2, "Repayment Amount: " + str(loan['repaymentAmount']))
      printlv(-1)
    elif (len(cmd) > 1 and cmd[1] == "loc"):
      if (len(cmd) > 3 and cmd[2] == "info"):
        cmd[3] = cmd[3].upper()
        try:
          loc = api.locations.get_location(cmd[3])['location']
        except Exception as e:
          printlv(-1)
          printlv(0, "[WARNING] Not a valid location or could not get info (" + str(cmd[3]) + ").")
          printlv(-1)
        else:
          printlv(-1)
          printlv(1, "Location info for symbol " + str(cmd[3]) + ":")
          printlv(2, "Name: " + str(loc['name']))
          printlv(2, "Type: " + str(loc['type']))
          printlv(2, "Coords: (" + str(loc['x']) + ", " + str(loc['y']) + ")")
          printlv(2, "Allows Construction: " + str(loc['allowsConstruction']))
          printlv(2, "Traits:")
          for trait in loc['traits']:
            printlv(3, str(trait))
          printlv(2, "Docked Ships: " + str(loc['dockedShips']))
          printlv(-1)
      elif (len(cmd) > 3 and cmd[2] == "ships"):
        cmd[3] = cmd[3].upper()
        try:
          ships = api.locations.get_ships_at_location(cmd[3])['ships']
        except Exception as e:
          printlv(-1)
          printlv(0, "[WARNING] Not a valid location, or no owned ships at location to provide data. Location: (" + str(cmd[3]) + ").")
          printlv(-1)
        else:
          numShips = len(ships)
          printlv(-1)
          if (numShips > 15):
            printlv(1, "Too many ships docked, won't print. Number Docked: " + str(len(ships)))
          else:
            printlv(1, "Ships docked at " + str(cmd[3]) + ":")
            for ship in ships:
              printlv(-1)
              printlv(2, "Ship Type: " + str(ship['shipType']))
              printlv(3, "Owner: " + str(ship['username']))
              printlv(3, "Ship ID: " + str(ship['shipId']))
          printlv(-1)
      elif (len(cmd) > 3 and cmd[2] == "market"):
        cmd[3] = cmd[3].upper()
        try:
          market = api.locations.get_marketplace(cmd[3])['marketplace']
        except Exception as e:
          printlv(-1)
          printlv(0, "[WARNING] Not a valid location, or no owned ships at location to provide data. Location: (" + str(cmd[3]) + ").")
          printlv(-1)
        else:
          printlv(-1)
          printlv(1, "Marketplace Listings At " + str(cmd[3]))
          for listing in market:
            printlv(-1)
            printlv(2, str(listing['symbol']))
            printlv(3, "Sell Price: " + str(listing['sellPricePerUnit']))
            printlv(3, "Buy Price: " + str(listing['purchasePricePerUnit']))
            printlv(3, "Available: " + str(listing['quantityAvailable']))
            printlv(4, "Volume per Unit: " + str(listing['volumePerUnit']) + ", Spread: " + str(listing['spread']) + ", Price per Unit: " + str(listing['pricePerUnit']))
          printlv(-1)
          printlv(-1)
      else:
        printlv(-1)
        printlv(0, "[Invalid Command] `" + " ".join(cmd) + "`, GET expects 3rd parameter from list [info, ships, market]")
        printlv(-1)
    elif (len(cmd) > 1 and cmd[1] == "ships"):
      ships = api.ships.get_user_ships()['ships']
      printlv(-1)
      printlv(0, "Owned Ships:")
      for ship in ships:
        printShipInfo(ship)
      printlv(-1)
    elif (len(cmd) > 2 and cmd[1] == "ship"):
      try:
        ship = api.ships.get_ship(cmd[2])['ship']
      except Exception as e:
        printlv(-1)
        printlv(0, "[WARNING] Not a valid ship id, or could not get ship details. ID: (" + str(cmd[2]) + ").")
        printlv(-1)
      else:
        printShipInfo(ship)
    else:
      printlv(-1)
      printlv(0, "[Invalid Command] `" + " ".join(cmd) + "`, GET LOC expects 2nd parameter from list [info, loans, loc, ships, ship]")
      printlv(-1)
  else:
    printlv(-1)
    printlv(0, "[Invalid Command] `" + " ".join(cmd) + "`, valid plan-level commands are: [get]")
    printlv(-1)

def printlv(level, text=""):
  if level < 0:
    res = "------------------------------"
  else:
    res = "".join([" -"]*(level)) + " " + text
  print(res)

def printShipInfo(ship):
  printlv(-1)
  printlv(1, "Ship ID: " + str(ship['id']))
  printlv(2, "Manufacturer: " + str(ship['manufacturer']) + " | Type: " + str(ship['type']) + " | Class: " + str(ship['class']))
  printlv(2, "Location: " + str(ship['location']) + " | Coordinates: (" + str(ship['x']) + ", " + str(ship['y']) + ")")
  printlv(2, "Flight Speed: " + str(ship['speed']) + " | Plating: " + str(ship['plating']) + " | Weapons: " + str(ship['weapons']))
  printlv(2, "Cargo (Current " + str(ship['maxCargo'] - ship['spaceAvailable']) + "/" + str(ship['maxCargo']) + " Max):")
  printlv(2, "Loading Speed: " + str(ship['loadingSpeed']))
  for good in ship['cargo']:
    printlv(3, "Good: " + str(good['good']))
    printlv(4, "Quantity: " + str(good['quantity']) + " | Volume: " + str(good['totalVolume']))

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
  elif rawcmd == 'help':
    printlv(-1)
    printlv(0, "Available Commands:")
    printlv(1, "help | Print available commands and their functions")
    printlv(1, "exit / stop / quit | Stop script execution and exit")
    printlv(1, ":<plan-command> | Pass plan-level commands to the command queue")
    printlv(2, ":help | Get help for plan-level commands")
    printlv(2, ":get | Get from API")
    printlv(-1)
  elif rawcmd[0:1] == ':':
    cmd = rawcmd[1:].strip('\n')
    queueCommand(cmd)
  else:
    printlv(-1)
    print("[Invalid Script Command] `" + rawcmd + "`, valid script-level commands are: [exit, stop, quit]")
    printlv(1, "Use a colon (e.g. `:get info`) to input plan-level commands from terminal")
    printlv(-1)