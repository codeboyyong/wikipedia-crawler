#!/usr/bin/bash 
# -*- coding: utf-8 -*-
 
# Define the variable containing the file path
my_file="./inputs/target_urls.txt"
# echo "processing urls in $my_file"

# Read the file content line by line and print each line
# while IFS= read -r line; do
#      # if [[ $line =~ ^# ]]; then
#      #    continue  # Skip this line and continue with the next one
#      # fi
#      echo "processing $line"
#      python3 wikipedia-crawler.py "$line"
# done < ./inputs/target_urls.txt


cat $my_file |grep http| while read line 
do
     echo "processing $line"
      # do something with $line here
      python3 wikipedia-crawler.py "$line"
done

