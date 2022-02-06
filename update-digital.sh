#!/bin/bash
cp /Volumes/_Serato_/database\ V2 serato-db/database\ V2
echo "Copied Serato database from Proteus successfully"
python serato.py
echo "Parsed Serato database successfully"
scp digital.md tidepool@tidepool:/home/tidepool/www/collection/
