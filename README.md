

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


#### are you a security UX design expert?

Please contact me! I need your help to make sure hidden-tahoe-backup has
an excellently easy to use intuitive user interface.

#### are you a PyGTK+3 expert?

Please contact me if you would like to help out with
writing the graphical user interface for this project!


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


##### why not just use gpg in symmetric mode to encrypt the backup manifest?

**gpg** is terribly powerful as well as terrible. **gpg --symmetric** does not MAC the ciphertext!
Instead I use **DJB's NaCl SecretBox** to verifiably encrypt/decrypt the backup manifests.


#### why Tails?

Tails being a security hardened and easy to use Linux distribution is an excellent platform
from which to run the Tahoe-LAFS client. Using Tails ensures that novice computer users can leverage Tahoe-LAFS's
security features while reducing their risk of exposing another weak link in their system's security.
Tails is an utterly worthy platform in part because of the careful attention being paid to entropy
generation, clock sychronization, user space and kernel security hardening, network firewall rules,
frequent software security updates, expert peer review etc.


#### why Tahoe-LAFS?

##### verified end to end crypto
Tahoe Least Authoratative File System is a distributed cryptographic file
storage system which offers users very powerful features for the user.
Among the many features it is worth mentioning that because of the verified end to end crypto,
the security guarantees that Tahoe-LAFS provides are qualitatively different
than those of cloud storage providers such as Google Drive, Dropbox and Amazon S3.
These cloud storage services can do their best to prevent their servers from getting hacked...
However if an attacker gains access they will have access to the data in plaintext.
This is in direct contrast to Tahoe-LAFS storage servers which only see ciphertext.

##### data redundancy & censorship resistance
Additionally Tahoe-LAFS has flexible RAID-like data redundancy that implies censorship resistance:
If K out of N storage nodes are needed to reconstruct the data set then ((N - K) + 1) storage
nodes would have to be taken out in order to effectively censor content on the onion grid.

In the context of defeating censorship of politically sensitive material it would seem appropriate to ensure a
geopolitical distribution of storage servers such that at least K storage servers would be protected a bit more
than the rest of the grid. In some contexts this could mean operating at least K storage nodes under the territory of allied governments.

##### cryptographic capabilities model
Tahoe-LAFS has a powerful capabilities model which essentially implements a distributed access control system.
Users may choose on a per file basis if they would like to share a VerifyOnly, ReadOnly or ReadWrite cryptographic
capability with another user. Knowledge of one file does not imply any knowledge of other files that might be stored
in the grid.


#### example using the CLI:

```bash
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$ hiddenBackupCLI.py
Must specific either backup or restore.
usage: hiddenBackupCLI.py [-h] [--start] [--stop] [--restore] [--backup]
                          [--manifest MANIFEST] [--node-directory NODEDIR]

optional arguments:
  -h, --help            show this help message and exit
  --start               start Tahoe-LAFS client
  --stop                stop Tahoe-LAFS client
  --restore             restore
  --backup              backup
  --manifest MANIFEST   Backup manifest
  --node-directory NODEDIR
                        Specify which Tahoe node directory should be used.
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$ hiddenBackupCLI.py --start --manifest testManifest.json.secretbox  --node-directory testNode
Enter passphrase:
watchTahoeCmd
watching Tahoe command: tahoe create-client testNode
Node created in '/home/amnesia/Persistent/projects/hidden-tahoe-backup/testNode'
 Please set [client]introducer.furl= in tahoe.cfg!
 The node cannot connect to a grid without it.
 Please set [node]nickname= in tahoe.cfg
watchTahoeCmd
watching Tahoe command: usewithtor tahoe start testNode
STARTING '/home/amnesia/Persistent/projects/hidden-tahoe-backup/testNode'
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$
```

You should now look at the local gateway node http interface.
Usually Tahoe-LAFS clients set this server to listen on interface 127.0.0.1 port 3456.
However in the case of Tails port 7657 is accessible from the browser because I2p uses this.
If you don't use I2p with Tails then it should be no problem.

Once this status web page indicates that you are connected to enough Tahoe-LAFS storage nodes then
you can begin a backup or restore operation for example:

```bash
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$ hiddenBackupCLI.py --restore --manifest testManifest.json.secretbox --node-directory testNode/
Enter passphrase:
watchTahoeCmd
watching Tahoe command: tahoe cp -d testNode/ -v -r backup_test1:testDir1/Latest test2
attaching sources to targets, 0 files / 1 dirs in root
targets assigned, 0 dirs, 0 files
starting copy, 0 files, 0 directories
Success: files copied
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$ hiddenBackupCLI.py --stop --manifest testManifest.json.secretbox --node-directory tes
Enter passphrase:
watchTahoeCmd
watching Tahoe command: tahoe stop testNode/
STOPPING '/home/amnesia/Persistent/projects/hidden-tahoe-backup/testNode'
process 13612 is dead
(virtenv-hidden-tahoe)amnesia@amnesia:~/Persistent/projects/hidden-tahoe-backup$
```


#### more technical details:

* read my favorite white paper about Tahoe-LAFS: http://www.laser.dist.unige.it/Repository/IPI-1011/FileSystems/TahoeDFS.pdf
* Tahoe-LAFS website: https://tahoe-lafs.org/trac/tahoe-lafs
* Tails website: https://tails.boum.org/
* Tor project website: https://www.torproject.org/
* DJB's NaCl crypto library: http://nacl.cr.yp.to/
* libsodium fork of NaCl: https://github.com/jedisct1/libsodium

#### software dependencies

* Tahoe-LAFS
* Torsocks
* tor
* pynacl
* libsodium

**GUI:**
* GTK+3
* Twisted
* pygtk

**The Torsocks dependency** will be removed once my native Tor integration is merged and resolves Tahoe-LAFS trac ticket 517:
https://tahoe-lafs.org/trac/tahoe-lafs/ticket/517


#### development style

I'm using an iterative approach so I can quickly produce a **working proof of concept!**

This backup system is currently built by wrapping the "tahoe cp" and "tahoe backup" commands...
however in the future this "backup manifest" functionality could be implemented
directly in the Tahoe-LAFS gateway node.

These "backup manifests" are essentially an alternate configuration format for Tahoe-LAFS
with metadata for performing backup and restore operations.

I'm looking forward to implementing several other Tahoe-LAFS backup systems for Tails.
I think they will each have their own advantages. Clearly this system's advantage is the
ability to reduce the complexity of data retrieval to a passphrase and information about
where to find the encrypted manifest.


#### suggestions and feature requests welcome

* [my contact info](https://www.lumiere.net/~mrdavid/contact.txt)

* [my github profile](https://github.com/david415)
