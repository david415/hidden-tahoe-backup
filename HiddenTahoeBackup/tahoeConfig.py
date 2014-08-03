
# external modules
import re
import os.path

# internal modules
from tahoeCommands import watchTahoeCmd


# XXX TODO: generate the "introducers" file
# for the "multi-introducer" introduced
# by Leif Ryge's truckee feature branch
def createIntroducers(introducerNodes, tahoeDir=None):
    pass

def genStorageConfig(storageNodes):
    config = "\n[client-server-selection]"
    for name, furl in storageNodes.items():
        m = re.match(r'pb://(.*)@.+', furl)
        assert m
        seed = m.group(1)

        config += """
server.v0-%s.type = tahoe-foolscap
server.v0-%s.nickname = %s
server.v0-%s.seed = %s
server.v0-%s.furl = %s
""" % (seed, seed, name, seed, seed, seed, furl)

    return config

def genTahoeConfig(manifest, tahoeDir=None):

    if len(manifest['fields']['introducerNodes']) > 1:
        createIntroducers(manifest['fields']['introducerNodes'], tahoeDir=tahoeDir)
        client = """
[client]
shares.needed = 3
shares.happy = 6
shares.total = 6
"""
    else:
        client = """
[client]
introducer.furl = %s
shares.needed = 3
shares.happy = 6
shares.total = 6
""" % manifest['fields']['introducerNodes'][0]

    config = """
[node]
nickname = client
web.reveal_storage_furls = true
web.port = tcp:7657:interface=127.0.0.1
web.static = public_html
tub.location = client.fakelocation:1
[storage]
enabled = false
[helper]
enabled = false
[drop_upload]
enabled = false
""" % manifest['fields']['introducerNodes']

    if len(manifest['fields']['storageNodes']) > 0:
        config += genStorageConfig(manifest['fields']['storageNodes'])

    return client + config


# XXX make idempotent?
def createTahoeConfigDir(nodeDir=None, manifest=None):

    # fails if the directory exists
    watchTahoeCmd("create-client %s" % (nodeDir,))

    config = genTahoeConfig(manifest)

    # XXX
    config_fh = open(nodeDir + '/tahoe.cfg', 'w')
    config_fh.write(config)
    config_fh.close()

    # Tahoe-LAFS cryptographic capability aliases file
    aliases_str = ""
    for name, capability in manifest['fields']['snapshotAliases'].items():
        aliases_str += name + ": " + capability + "\n"

    # XXX
    aliases_file = os.path.join(nodeDir, 'private', 'aliases')
    aliases_fh = open(aliases_file, 'w')
    aliases_fh.write(aliases_str)
    aliases_fh.close()
