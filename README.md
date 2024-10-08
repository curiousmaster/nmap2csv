## NAME
nmap2csv.py

## DESCRIPTION
This script parses Nmap output and converts it into CSV format.

## USAGE
```
nmap_to_csv.py [-d] [FILE]
nmap_to_csv.py [--delimiter] [FILE]
nmap_to_csv.py [-h | --help]
nmap ... | nmap_to_csv.py [-d]
```

## OPTIONS
```
-d, --delimiter  Optional. Add an empty line between each new block of IP addresses.
-h, --help       Show this help message and exit.
FILE             Optional. Specifies the file containing Nmap output.
                 If not provided, the script reads from stdin.
```

## VERSION
* Aug 1, 2024 / v1.0
