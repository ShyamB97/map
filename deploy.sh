#!/usr/bin/env bash
# how deploy the app on the github page (assuming my page points to this repo still).

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# 1. generate the new index html. Pass the map.py args through this script
python map.py $1 --export_html
mv map.html index.html
# 2. in a temporary folder, clone the deploy branch
cd /tmp
git clone -b deploy https://github.com/ShyamB97/map.git
# 3. copy the new index.html into depoly
cp $SCRIPT_DIR/index.html .
# 4. push deploy.
git commit -a -m "update deploy html"
git push
cd -
rm -rf /tmp/map
# 5. wait