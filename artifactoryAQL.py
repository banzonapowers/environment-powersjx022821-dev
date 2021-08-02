#!/usr/bin/python3
import json
import sys
from cryptography.fernet import Fernet
from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth

key = b'iwJsebH4vFt8fB6-7k7zZjt6VNLgjjJLl5g1F1B8TVo='
cipher_suite = Fernet(key)
ciphered_text = b'gAAAAABetXhhcm52CJnfO81tb91Fb_ds3I_bGsoRHOm0H6qFUfPrrvRz_sKJEO2M8ACqBHV-cjrARl18vg-F-liSmNP2oWxSHw=='
unciphered_text = (cipher_suite.decrypt(ciphered_text))
unciphered_text = str(unciphered_text,'utf-8')
#print(unciphered_text)
unciphered_text="thisismycreds"

try:

    reponame = sys.argv[1]
    #daysdownloaded = sys.argv[2]
    #dayscreated = int(sys.argv[3])
    #print("repo: %s downloaded archive days: %s Non-downloaded Artifacts: %s" % (reponame, daysdownloaded, dayscreated))

except:
    print("No arguments passed or argument incomplete or invalid argument.")
    sys.exit()


aql = ArtifactoryPath(
    "http://artifactory-test-am2.devops.aig.net/artifactory/",
    auth=("demouser", unciphered_text),
    auth_type=HTTPBasicAuth,
)



args = [ 

"items.find",
	{   "repo": reponame,
        "$and": [
		{"type":"file"},
#		{"created_by":"abanzon"},
#   	{"size":{"$gt":"0"}}
#        {"created": {"$gt":"2020-05-05"}}
		]
	},
#sort({"$desc": ["size","name"]}),
#limit(100)
]

try:

    #artifacts_list = aql.aql(*args)
    artifacts_list = aql.aql(*args, ".include", ["stat.*", "release_artifact.*", "dependency.*", "artifact.*", "archive.*", "property.*"])
    artifact_pathlib = map(aql.from_aql, artifacts_list)
    artifact_pathlib_list = list(map(aql.from_aql, artifacts_list))

except:

    print("Invalid value, please check arguments.")
    sys.exit()

pathlist = []

for mylist in artifacts_list:
    checkpath = str(mylist['repo'] + "/" + mylist['path'])
    if checkpath not in pathlist:
        pathlist.append(checkpath)

for display in pathlist:
    print(display)

    #print(mylist['repo'] + "/" + mylist['path'])
    #print("###############")
    #print(mylist['repo'] + "/" + mylist['path'] + " " + mylist['modified'])
    #print("Array 0 HERE")
    #print (mylist['properties'][0])
    #print("Array 1 HERE")
    #print (mylist['properties'][1])
    #print("Array 2 HERE")
    #print (mylist['properties'][2])

