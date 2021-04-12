#!/bin/bash
if [ $1 == "midgard" ]
  then
  echo "generating api client for $1"
    curl -X POST   https://generator3.swagger.io/api/generate   -H 'content-type: application/json'   -d '{
    "options" : {
      "additionalProperties" : {
        "packageName": "midgard_client"
      }
    },
    "specURL" : "'$2'",
    "lang" : "python",
    "type" : "CLIENT",
    "codegenVersion" : "V3"
  }' --output midgard.zip
    unzip -o midgard.zip -d ../midgard_client
    rm midgard.zip
else
  echo "generating api client for $1"
  curl -X POST   https://generator3.swagger.io/api/generate   -H 'content-type: application/json'   -d '{
      "options" : {
        "additionalProperties" : {
          "packageName": "thornode_client"
        }
      },
      "specURL" : "'$2'",
      "lang" : "python",
      "type" : "CLIENT",
      "codegenVersion" : "V2"
    }' --output thornode.zip
    unzip -o thornode.zip -d ../thornode_client
    rm thornode.zip
fi