README
######


**NAME**


``OPB`` - object programming bot.


**SYNOPSIS**

::

 python3 -m opb [<cmd>|-c|-d] [key=value] [key==value]


**DESCRIPTION**


``opb`` is a IRC bot, intended to be programmable, with a client program (opb),
command line interface (opbc) and a daemon version (opbd), it provides object
persistence, an event handler and some basic code to load modules that can
provide additional functionality.

``opb`` uses object programming, object oriented programming without the
oriented. Object programming is programming where the methods are seperated
out into functions that use the object as the first argument of that funcion.
This gives base class definitions a clean namespace to inherit from and to load
json data into the object's __dict__. A clean namespace prevents a json loaded
attribute to overwrite any methods.

``opb`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
and paths carry the type in the path name what makes reconstruction from
filename easier then reading type from the object.

``opb`` has some functionality, mostly feeding RSS feeds into a irc
channel. It can do some logging of txt and take note of things todo.


**INSTALL**


::

 $ sudo pip3 install opb


**CONFIGURATION**


configuration is done by calling the ``cfg`` command:


IRC

::

 $ python3 -m opb cfg server=<server> channel=<channel> nick=<nick>

 (*) default channel/server is #opb on localhost


SASL

::

 $ python3 -m opb pwd <nickservnick> <nickservpass>
 $ python3 -m opb cfg password=<outputfrompwd>


USERS

as default the user's userhost is not checked when a user types a command in a
channel. To enable userhost checking enable users with the ``cfg`` command::

 $ python3 -m opb cfg users=True


To add a user to the bot use the met command::

 $ python3 -m opb  met <userhost>

to delete a user use the del command with a substring of the userhost::

 $ python3 -m opb del <substring>


RSS

::

 $ python3 -m opb rss <url>



**RUNNING**


this part shows how to run ``opb``.


**cli**


without any arguments ``opb`` doesn't respond, add arguments to have
``opb`` execute a command::


 $ python3 -m opb
 $


the ``cmd`` command shows you a list of available commands::


 $ python3 -m opb cmd
 cfg,cmd,dlt,dpl,flt,fnd,ftc,met,mre,nme,pwd,rem,rss,thr,upt


**console**


use the ``-c`` option to start the bot as a console::

 $ python3 -m opb -c
 OPB started at Fri Jan 6 01:49:58 2023
 > cmd
 cfg,cmd,dlt,dpl,flt,ftc,krn,log,met,mre,nme,pwd,rem,rss,thr,upt
 >

running the bot in the background is done by using the ``-d`` option::

 $ python3 -m opb -d
 $


**COMMANDS**


here is a short description of the commands::

 cfg - show the irc configuration, also edits the config
 cmd - show all commands
 dlt - remove a user
 dne - flag todo as done
 dpl - set display items for a rss feed
 flt - show a list of bot registered to the bus
 fnd - allow you to display objects on the datastore, read-only json files on disk 
 ftc - run a rss feed fetching batch
 log - log some text
 met - add a users with there irc userhost
 mre - displays cached output, channel wise.
 nme - set name of a rss feed
 pwd - combine a nickserv name/password into a sasl password
 rem - remove a rss feed by matching is to its url
 rss - add a feed to fetch, fetcher runs every 5 minutes
 thr - show the running threads
 tdo - adds a todo item, no options returns list of todo's
 upt - show uptime


**PROGRAMMING**


The ``opb`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

 >>> from opb import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 >>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

great for giving objects peristence by having their state stored in files::

 >>> from opb import Object, write
 >>> o = Object()
 >>> write(o)
 opb.objects.Object/89efa5fd7ad9497b96fdcb5f01477320/2022-11-21/17:20:12.221192


**AUTHOR**


Bart Thate - operbot100@gmail.com


**COPYRIGHT**


``opb`` is placed in the Public Domain.
