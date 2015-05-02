Tournament_Results
-------------------

What is it?
-----------

This project is used to design a database for saving and updating tournament results.
In addition the results are fetched and processed in python modules.The game tournament 
will use the Swiss system for pairing up players in each round: players are not eliminated, 
and each player is paired with another player with the same number of wins, or as close as possible.

Files Included:
--------------
1) tournament_basic - 
      i)tournament.py - contains operations like creating connection with db ,insert,delete,update etc
     ii)tournament.sql - contains sql commands for creating tables,triggers and views
    iii)tournament_test.py - contains methods to get the player standings,perform swiss pairings etc.

2) tournament_credit - 
      i)tournament.py - contains operations like creating connection with db ,insert,delete,update etc
     ii)tournament_swiss.sql - contains sql commands for creating tables,triggers and views
    iii)tournament_test.py - contains methods to get winner of the tournament, get rank of each players 
        at the end of tournament,perform swiss pairings etc.
        
Installation
------------

Install Git, VirtualBox and Vagrant.
For download links and in depth details for installation please visit - https://www.udacity.com/wiki/ud197/install-vagrant
Git - Unix-style terminal and shell (Git Bash) to acces the folders present in remote system.
VirtualBox - used to run VM.
Vagrant -  configures the VM and lets you share files between your host computer and the VM's filesystem.

Working 
------------
1) connect to remote desktop via git bash using vagrant up,vagrant ssh commands from the fullstack/vagrant folder
2)Vagrant up is used to create a connection with the host followed by vagrant ssh which connects to the remote desktop
2) Run sql files from either tournament_credit or tournament_basic path present in remote desktop
3)Commands for running the sql file - /i tournament_swiss.sql (where tournament_swiss.sql is the sql file to be run, 
 contains sql query for creating database schema(tables,views,triggers) )

3) Run tournament_test.py from the same path where sql is executed										

Contacts
  --------

     o please send your queries regarding this project to prakash.dec20@gmail.com 

