#!/bin/bash
sudo kill `ps aux | grep aws_mgt | grep -v "grep" | head -3 | awk '{print $2}'`