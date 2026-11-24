#!/bin/bash
set -e

K="sudo /usr/local/bin/kubectl"

echo "Checking deployments"
$K get deployments

echo "Adding canary labels to running pods"
$K label pods -l app=aceest-fitness release-track=canary --overwrite
$K label pods -l app=aceest-green release-track=canary --overwrite

echo "Switching service to both versions"
$K patch service aceest-fitness --type=json \
  -p='[{"op":"replace","path":"/spec/selector","value":{"release-track":"canary"}}]'

echo "Showing selected endpoints"
$K get endpointslice -l kubernetes.io/service-name=aceest-fitness

echo "Canary routing configured"
