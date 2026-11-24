#!/bin/bash
set -e

sudo /usr/local/bin/kubectl patch service aceest-fitness \
  --type=json \
  -p='[{"op":"replace","path":"/spec/selector","value":{"app":"aceest-fitness"}}]'

sudo /usr/local/bin/kubectl get service aceest-fitness \
  -o jsonpath='{.spec.selector}'
echo
