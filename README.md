# starscript

This is a python script for automating the game [Space Traders](https://spacetraders.io), and is built on the [SpacePyTraders SDK](https://github.com/ZacHooper/spacePyTraders).

## Installation

Install pipenv: `pip install --user pipenv`

Source your profile: `source ~./profile`

Run `launchdev.sh` and pipenv will handle installing dependencies

## Changelog

### v0.0.3 - Threading & Live Commands

- Added threading
- Command Queue now runs on a separate thread from main, user can enter their own commands into main
- - `quit` quit execution
- - \[Planned] `qc ...` queue following command

### v0.0.2 - Preliminary command implementation

- Read `.starplan` text files and parse out basic commands
- - `# <comment>` Ignored
- - `get ...` Get request
- - - `info` Specifies account info (credits, ship count, etc.)
- - - `loans` Specifies loan info (all loans associated with account)
- - - `loc ...` Specify location request
- - - - `info` Specifies location info (traits, type, name, etc.)
- - - - `ships` Specifies list of ships docked at location (ship id, owner, type)
- - - - `market` Specifies market data from location (good names, prices, quantity, etc.)
- - - `ships` Specifies list of all owned ships
- - - `ship` Specifies info about single ship

### v0.0.1

- SpacePyTraders SDK installed, able to do basic query
- Setup pipenv

## Roadmap

- 1:1 command parity with SDK/API endpoints
- `.starsession` file for remembering credentials
- - Auto-register & run startup script (+notify) on server wipe
- `.starsettings` file for remembering settings (e.g. log verbosity, notification preferences, etc.)
- `.starlog` file for logging longitudinal data (changes will be streamed to captains-log for filing in DB for long-term storage)
- `.starhistory` file for logging commands and their source (plan \[and how plan was started/assigned], cli, helmsman, etc.), errors, notable events, etc.
- Script Variables
- - Save data returned by requests for use in conditional commands
- Notifications
- - Will be able to notify user through various avenues when plan (cmd) or script (hard-coded events like wipe or unrecoverable errors) encounters the need to
- - Integration with Discord as a bot?
- - Email?
- - SMS?
- Commands for working with **Plans** in `/plans`
- - `list`, `new`, `edit`, `del`, etc.
- - `loop` and `goto` commands for use within plans
- - conditionals
- - Consider more how plans interact with ships, probably most simply by keeping a list of ships locally, and storing an assigned plan for each. OR by storing a list of active plans, and an associated list of assigned ships?
- Interactive CLI, perhaps using [Nubia](https://github.com/facebookincubator/python-nubia)
- Consider alternative UI options later (e.g. web/windows)
- API for integration with helmsman
- - Primarily for working on plans remotely
- - Also allows assigning different plans to ships remotely (using plans local to starscript)
- Integration with captains-log
- - Can save API calls by passing information directly from starscript to captains-log (if passed relevant data CL can skip next automatic data poll, otherwise will simply ignore the input)
- space-opera: Allow for ship `groups` and `pools`
- - `groups`: Ships that are grouped will all use the same plan (maybe include in base starscript)
- - `pools`: Ships that are part of a pool can be dynamically assigned to certain plans conditionally. Ships can be a part of multiple pools but (maybe?) are only able to be active in one pool at a time
