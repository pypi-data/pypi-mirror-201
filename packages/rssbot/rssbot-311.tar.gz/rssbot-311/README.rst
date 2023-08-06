README
######


**NAME**


|

``rssbot`` - feeding rss into your channel

|

**SYNOPSIS**

|

::

 $ sudo python3 -m pip install rssbot
 $ sudo cp /usr/local/rssbot/rssbot.service /etc/systemd/system
 $ sudo systemctl enable rssbot --now

 (*) default channel/server is #rssbot on localhost

|

**DESCRIPTION**

|

``rssbot`` is a python3 irc bot that feeds rss into your channel, it uses
systemd to run a 24/7 presence in a channel. The daemon is without any
commands available, a seperate program ``rssbotctl`` is provided todo the
bot's management. ``rssbot`` can handle SASL connection to modern irc
networks.

``rssbot`` is a contribution back to society, it is placed in the Public Domain

|

**CONFIGURATION**

|

configuration is done by calling the ``cfg`` command of ``rssbotctl``

| 

**irc**

|

::

 $ sudo rssbotctl cfg server=<server> channel=<channel> nick=<nick>

|

**sasl**

|

::

 $ sudo rssbotctl pwd <nsnick> <nspass>
 $ sudo rssbotctl cfg password=<outputfrompwd>

|

**rss**

|

::

 $ sudo rssbotctl rss <url>

|

**COMMANDS**

|

here is a short description of ``rssbotctl`` commands::


 cfg - show the irc configuration, also edits the config
 cmd - show all commands
 dlt - remove a user
 dne - flag todo as done
 dpl - set display items for a rss feed
 ftc - run a rss feed fetching batch
 met - add a users with there irc userhost
 mre - displays cached output, channel wise.
 nme - set name of a rss feed
 pwd - combine a nickserv name/password into a sasl password
 rem - remove a rss feed by matching is to its url
 rss - add a feed to fetch, fetcher runs every 5 minutes
 tdo - adds a todo item, no options returns list of todo's
 upt - show uptime

|

**AUTHOR**

|

Bart Thate - thatebhj@gmail.com

|

**COPYRIGHT**

|

``rssbot`` is placed in the Public Domain.
