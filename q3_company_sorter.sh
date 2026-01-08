#!/bin/bash

URL="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"

# Download the data, ignore the header (tail), parse with awk, and sort
# FPAT matches either non-comma strings OR strings inside quotes
curl -s "$URL" | \
tail -n +2 | \
awk -v FPAT='([^,]*)|("[^"]+")' '{ 
    # Remove quotes from location if present for cleaner output
    gsub(/"/, "", $5); 
    
    # Print Name, Location, Founding Year
    printf "%s, %s, %s\n", $2, $5, $8 
}' | \
sort -t, -k3n
