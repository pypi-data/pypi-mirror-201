#!/bin/sh
distribution_json=$(distro -j)
echo $distribution_json | python -c "import sys, json; print(json.load(sys.stdin)['id'])"
