.. _manual:

.. title:: Manual


.. raw:: html

     <br><br>


**NAME**


 ``GCID`` - genocide count id


**SYNOPSIS**

::

 sudo python3 -m pip install gcid``
 sudo cp /usr/local/gcid/gcid.service
         /etc/systemd/system``
 sudo systemctl enable gcid --now

 default is #gcid on localhost

**DESCRIPTION**


 ``GCID`` holds evidence that king netherlands is doing a genocide, a 
 written :ref:`response <king>` where king netherlands confirmed taking note
 of “what i have written”, namely :ref:`proof <evidence>` that medicine he
 uses in treatement laws like zyprexa, haldol, abilify and clozapine are poison
 that make impotent, is both physical (contracted muscles) and mental (let 
 people hallucinate) torture and kills members of the victim groups. 


 ``GCID`` contains :ref:`correspondence <writings>` with the
 International Criminal Court, asking for arrest of the king of the 
 netherlands, for the genocide he is committing with his new treatement laws.
 Current status is an outside the jurisdiction judgement of the prosecutor 
 which requires a :ref:`basis to prosecute <home>` to have the king actually
 arrested.


 ``GCID`` is also a bot, intended to be programmable, with a client program to
 develop modules on and a systemd version with code included to run a 24/7
 presence in a channel. It can show genocide and suicide stats of king
 netherlands his genocide into a IRC channel, display rss feeds, log simple
 text messages, source is :ref:`here <source>`.


**CONFIGURATION**


 use sudo, ``gcidctl`` needs root privileges


 ``irc``

 :: 

  gcidctl cfg server=<server>
  gcidctl cfg channel=<channel>
  gcidctl cfg nick=<nick>
  

 ``sasl``

 ::

  gcidctl pwd <nsvnick> <nspass>
  gcidctl cfg password=<frompwd>


 ``rss``

 ::

  gcidctl rss <url>
  gcidctl dpl <str_in_url> <i1,i2>
  gcidctl rem <str_in_url>
  gcidctl nme <str_in_url< <name>
    

**COMMANDS**

 ::

  cmd - commands
  cfg - irc configuration
  dlt - remove a user
  dpl - sets display items
  ftc - runs a fetching batch
  fnd - find objects 
  flt - instances registered
  log - log some text
  mdl - genocide model
  met - add a user
  mre - displays cached output
  nck - changes nick on irc
  now - genocide stats
  pwd - sasl nickserv name/pass
  rem - removes a rss feed
  req - reconsider
  rss - add a feed
  slg - slogan
  thr - show the running threads
  tpc - genocide stats into topic


**FILES**


 | ``/usr/local/share/doc/gcid/*``
 | ``/usr/local/gcid/``


**AUTHOR**


 Bart Thate <thatebhj@gmail.com>


**COPYRIGHT**


 ``GCID`` is placed in the Public Domain.
