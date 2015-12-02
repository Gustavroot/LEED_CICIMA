#!/bin/bash

userD=`whoami`

#----
cd /home/$userD/LEEDcicima/
git pull origin master
git push origin master
