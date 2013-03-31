#!/bin/bash
rm -rf ./CareerSearch
thrift --gen py:new_style links.thrift
cp -r ./gen-py/CareerSearch .
rm -rf ./gen-py/
