
hidden-tahoe-backup
===================

disclaimer: this is a very rough draft development version with no peer review


a clandestine distributed backup system for Tails and other discerning users of Tor and strong crypto



Project Objective:
------------------

This project's objective is to help people in oppressive surveillance states ensure the
confidentiality and integrity of their data. A Tahoe-LAFS backup system can have interesting
political implications such as powerful operational security tactics to ensure confidentiality
of data while traveling internationally in the most hostile environments where one could be
subject to search and seizure. Tools that enable these highly effective operational security
tactics need to made easier to use so that journalist and other political targets can effectively
use them without being required to have specialized knowledge of computer security.

The two highest priorities of this project are that of usuability and security.
Tahoe-LAFS is not widely used by novice computer users because of the useability issues.
Tails (The amnesiac incognito live system) is now a well known Linux "live" distribution
with a reputation for making powerful cryptographic/security/anonymity software easy to use.
A Tails integrated backup system using Tahoe-LAFS must be easy to use in order for it to
receive widspread adoption and to be consistent with the desires of the Tails development roadmap.

This is a prototype backup system designed for Tails.
It can be used to backup/restore your Tails Persistent volume to a Tahoe-LAFS onion grid.
There are several other ways to integrate Tahoe-LAFS and Tails; I intend on writing more soon.

An easy-to-use integrated backup system for Tails has an
enormous amount of potential to help novice computer users
leverage the powerful features of Tahoe-LAFS.


What is an onion grid?
----------------------

It's a Tahoe-LAFS storage grid, a collection of Tahoe-LAFS storage servers that
are only accessible via Tor hidden services. That means the identity/location of the
storage servers are protected by the Tor network.


What else is "hidden" about this backup system?
-----------------------------------------------

You can hide your backup-manifest after performing a backup.
This allows you to wipe your Tails Persistent volume if you
will be traveling through a hostile environment.


What is Tahoe-LAFS?
-------------------

Tahoe-LAFS - Least Authoratative File System is a distributed cryptographic file
storage system which offers users very powerful features. Among the many features
it is worth mentioning that the security guarantees that Tahoe-LAFS provides are qualitatively different
than that of cloud storage providers such as Google Drive, Dropbox and Amazon S3.
These cloud storage services can do their best to prevent their servers from getting hacked...
However if an attacker gains access they will have access to the data in plaintext.
This is in direct contrast to Tahoe-LAFS storage servers which only see ciphertext.

Additionally Tahoe-LAFS has flexible data redundancy and a cryptographic capabilities model allowing users
to share ReadOnly or ReadWrite access to files. Tahoe's RAID-like data redundancy accross storage servers
does imply censorship resistance; if K out of N storage nodes are needed to reconstruct the data set
then ((N - K) + 1) storage nodes would have to be taken out in order to effectively censor content on the onion grid.
In the context of defeating censorship of politically sensitive material it would seem appropriate to ensure a
geopolitical distribution of storage servers such that at least K storage servers would benefit from the protection
of allied governments.

For more technical details about Tahoe-LAFS read my favorite white paper about Tahoe-LAFS here:
http://www.laser.dist.unige.it/Repository/IPI-1011/FileSystems/TahoeDFS.pdf

And the official Tahoe-LAFS website here:
https://tahoe-lafs.org/trac/tahoe-lafs



Tails website:
https://tails.boum.org/

Tahoe-LAFS website:
https://tahoe-lafs.org/trac/tahoe-lafs

Tor project website:
https://www.torproject.org/


Requirements
------------

Tahoe-LAFS
Torsocks
tor


Suggestions and feature requests welcome:
-----------------------------------------

contact info:
https://www.lumiere.net/~mrdavid/contact.txt

https://github.com/david415
https://github.com/david415/hidden-tahoe-backup
