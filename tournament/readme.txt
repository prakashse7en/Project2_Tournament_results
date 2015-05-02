                                                        Tournament_Results
														-------------------

This project is used to design a database for saving and updating tournament results. In addition the results are fetched and processed in python modules
The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

Folders/Files present:
--------
1) tournament_basic - 
		Contains -
			i)tournament.py - contains operations like creating connection with db ,insert,delete,update etc
			ii)tournament.sql - contains sql commands for creating tables,triggers and views
			iii)tournament_test.py - contains methods to a)get the player standings,
							             b)perform swiss pairings etc.

2) tournament_credit - 
		Contains -
			i)tournament.py - contains operations like creating connection with db ,insert,delete,update etc
			ii)tournament_swiss.sql - contains sql commands for creating tables,triggers and views
			iii)tournament_test.py - contains methods to a)get winner of the tournament,
								     b)get rank of each players at the end of tournament,
							             c)perform swiss pairings etc.
Working and Set up
-----------------------
Required - Git - Unix-style terminal and shell (Git Bash) to acces the folders present i remote system
		   VirtualBox - used to run VM
		   Vagrant -  configures the VM and lets you share files between your host computer and the VM's filesystem
For download links and in depth details for installation please visit - https://www.udacity.com/wiki/ud197/install-vagrant

Working - 
		  1) connect to remote desktop via git bash using vagrant up,vagrant ssh commands from the fullstack/vagrant folder
		  2) Run sql files from either tournament_credit or tournament_basic path present in remote desktop
		  3) Run tournament_test.py from the same path where sql is executed										

Contacts
  --------

     o please send your queries regarding this project to prakash.dec20@gmail.com 

