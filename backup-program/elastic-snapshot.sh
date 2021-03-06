#!/bin/bash

# Install jq binary:
# - yum install jq
# - apt-get install jq
# - or download from http://stedolan.github.io/jq/


# Register repo
# $ curl -XPUT 'http://<host>:<port>/_snapshot/dbmiannotator-elastic-snapshot' -d '{
#     "type": "fs",
#     "settings": {
#         "location": "/home/dbmiannotator-elastic-snapshot",
#         "compress": true
#     }
# }'



# Configuration
LIMIT=30  # Number of backups
REPO=dbmiannotator-elastic-snapshot # Name of snapshot repository

HOST=$1
PORT=$2

if [[ -z $HOST || -z $PORT ]]; then
    echo "Usage: bash elastic-snapshot.sh <hostname> <port>"
    echo "ex. bash elastic-snapshot.sh localhost 9200"
    exit
else

    curl -XPUT "http://$HOST:$PORT/_snapshot/dbmiannotator-elastic-snapshot" -d '{ "type": "fs", "settings": { "location": "/home/dbmiannotator-elastic-snapshot", "compress": true }}'

    # Create snapshot
    SNAPSHOT=`date +%Y%m%d-%H%M%S`
    curl -XPUT "$HOST:$PORT/_snapshot/$REPO/$SNAPSHOT?wait_for_completion=true"


    # Get a list of snapshots that we want to delete
    SNAPSHOTS=`curl -s -XGET "$HOST:$PORT/_snapshot/$REPO/_all" | jq -r ".snapshots[:-${LIMIT}][].snapshot"`

    # Loop over the results and delete each snapshot
    for SNAPSHOT in $SNAPSHOTS
    do
        echo "Deleting snapshot: $SNAPSHOT"
        curl -s -XDELETE "$HOST:$PORT/_snapshot/$REPO/$SNAPSHOT?pretty"
    done
    echo "Create snapshot - Done!"
fi


