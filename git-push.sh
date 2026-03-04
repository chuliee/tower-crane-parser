#!/bin/bash

today=`date +%y%m%d`

git add .
git commit -m "[Auto] Update $today"
git push origin main