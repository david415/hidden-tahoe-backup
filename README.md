

### hidden-tahoe-backup

**disclaimer: this is a very early development version with no peer review**

a clandestine distributed backup system for Tails


#### project objective

This project's objective is to help people in oppressive surveillance states ensure the
confidentiality and integrity of their data. A Tahoe-LAFS backup system can have interesting
political implications such as powerful operational security tactics to ensure confidentiality
of data while traveling internationally in the most hostile environments where one could be
subject to search and seizure. Tools that enable these highly effective operational security
tactics need to made easier to use so that everyone can use them.

The two highest priorities of this project are that of usuability and security.
Tahoe-LAFS is not widely used by novice computer users because of the useability issues.
Tails (The amnesiac incognito live system) is now a well known Linux "live" distribution
with a reputation for making powerful cryptographic/security/anonymity software easy to use.
A Tails integrated backup system using Tahoe-LAFS must be easy to use in order for it to
receive widspread adoption and to be consistent with the desires of the Tails development roadmap.

This is a prototype backup system designed for Tails... but it will work just fine for non-Tails systems.
It can be used to backup and restore your Tails Persistent volume to a Tahoe-LAFS onion grid.
There are several ways to integrate Tahoe-LAFS and Tails; this. is. just. one. way. to. do. it.


#### what is an onion grid?

It's a Tahoe-LAFS storage grid, a collection of Tahoe-LAFS storage servers that are only
accessible via Tor hidden services. That means the identity/location of the storage servers
are protected by the Tor network.

At this time the Tor Project is redesigning Tor hidden services to have more powerful security
and anonymity guarantees. This project will benefit from these future design changes to Tor Hidden Services.


#### what else is "hidden" about this backup system?

A remarkable feature of this backup system is it's encrypted backup manifests.
That is, a ciphertext blob, MAC'ed and symmetrically encrypted with an entropic user supplied passphrase;
the plaintext data will contain a small amount of critical information that allows the Tahoe-LAFS user to
retreive a backup snapshot from the onion grid. The idea here is to ensure future access to the Tahoe-LAFS
cryptographic capability and grid connecting information so that the user can retreive their data.

This encrypted manifest must be stored in a safe place for later retreival. If for instance an individual wishing
to travel through a hostile environment where search and seizure are real possibilities then in that case
the goal should be to travel with no sensitive information, ciphertext or key material.

To achieve this goal the user may send an encrypted message to several trusted parties containing the encrypted
backup manifest, a small ciphertext blob. Once data is uploaded to the grid and the redundant copies of the
ciphertext blob are hidden to ensure future access then the user can wipe her drives in preparation for traveling
in hostile environments.

Upon arrival the ciphertext blob is retreived from one of the trusted parties. If the MAC is valid and the user is able to
decrypt the blob then the resulting information is used to setup a Tahoe-LAFS configuration directory. Backup manifest data
specifies the Tahoe-LAFS snapshot locations and which local directories to restore the data to.


#### why Tails?

Tails being a security hardened and easy to use Linux distribution is an excellent platform
from which to run the Tahoe-LAFS client. Using Tails ensures that novice computer users can leverage Tahoe-LAFS's
security features while reducing their risk of exposing another weak link in their system's security.
Tails is an utterly worthy platform in part because of the careful attention being paid to entropy
generation, clock sychronization, user space and kernel security hardening, network firewall rules,
frequent software security updates, expert peer review etc.


#### why Tahoe-LAFS?

Tahoe Least Authoratative File System is a distributed cryptographic file
storage system which offers users very powerful features including verified end to end crypto,
data redundancy and a cryptographic capabilities model. Among the many features
it is worth mentioning that because of the verified end to end crypto,
the security guarantees that Tahoe-LAFS provides are qualitatively different
than those of cloud storage providers such as Google Drive, Dropbox and Amazon S3.
These cloud storage services can do their best to prevent their servers from getting hacked...
However if an attacker gains access they will have access to the data in plaintext.
This is in direct contrast to Tahoe-LAFS storage servers which only see ciphertext.

Additionally Tahoe-LAFS has flexible RAID-like data redundancy that implies censorship resistance:
If K out of N storage nodes are needed to reconstruct the data set then ((N - K) + 1) storage
nodes would have to be taken out in order to effectively censor content on the onion grid.

In the context of defeating censorship of politically sensitive material it would seem appropriate to ensure a
geopolitical distribution of storage servers such that at least K storage servers would be protected a bit more
than the rest of the grid. In some contexts this could mean operating at least K storage nodes under the territory of allied governments.


For more technical details about Tahoe-LAFS:

* read my favorite white paper about Tahoe-LAFS: http://www.laser.dist.unige.it/Repository/IPI-1011/FileSystems/TahoeDFS.pdf

* Tahoe-LAFS website: https://tahoe-lafs.org/trac/tahoe-lafs


* Tails website: https://tails.boum.org/

* Tor project website: https://www.torproject.org/


#### requirements

* Tahoe-LAFS
* Torsocks
* tor


#### suggestions and feature requests welcome

* [my contact info](https://www.lumiere.net/~mrdavid/contact.txt)

* [my github profile](https://github.com/david415)
