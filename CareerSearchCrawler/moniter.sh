#!/bin/bash

while [ 1 -eq 1 ];do
    date
    sudo scrapy crawl $1
done
