# Match-Up-Server

A general server for setting up matches.  Inspired by [CS:GO](http://blog.counter-strike.net/) match-up system.

This module is dependent on [Tornado](http://www.tornadoweb.org/en/stable/).

## Usage

	pip install tornado # if you haven't done so
	python match.py

Now navigate to `localhost:8000`.  You can open up multiple windows for testing.  Enter a team name and the number of players in the team.  When a match is ready, the client will be notified via websocket.

There are two configurable parameters: the number of players per team and the number of teams that a match requires.  The two parameters default to 5 and 2 (as in CS:GO), but you can configure them via command line like this:

	python match.py --num-teams=4 --num-per-team=1