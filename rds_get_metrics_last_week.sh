#!/bin/bash

RDS=$1

metrics=$(aws cloudwatch get-metric-statistics --region us-east-1 --metric-name DatabaseConnections --start-time 2023-05-18T00:00:00 --end-time 2023-05-25T00:00:00 --period 3600 --namespace AWS/RDS --statistics Average --dimensions Name=DBInstanceIdentifier,Value=$RDS | grep Average | grep -v '0.0')

if [[ -n $metrics ]]; then
  echo "There were connections in the last week"
else
  echo "No connections to the DB in the last week"
fi
