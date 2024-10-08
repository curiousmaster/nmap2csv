#!/usr/bin/env python3
#======================================================================
# NAME
#       nmap_to_csv.py
#
# DESCRIPTION
#    This script parses Nmap output and converts it into a CSV format.
#
# USAGE
#    nmap_to_csv.py [-d] [FILE]
#    nmap_to_csv.py [--delimiter] [FILE]
#    nmap_to_csv.py [-h | --help]
#    nmap ... | nmap_to_csv.py [-d]
#
# OPTIONS
#    -d, --delimiter  Optional. Add an empty line between each new block of IP addresses.
#    -h, --help       Show this help message and exit.
#    FILE             Optional. Specifies the file containing Nmap output.
#                     If not provided, the script reads from stdin.
#
# AUTHOR
#   Stefan Benediktsson
#
# VERSION
#   Aug 1, 2024 / v1.0 / Stefan Benediktsson
#======================================================================

import re
import sys
import ipaddress
import argparse


#----------------------------------------------------------------------
#    FUNCTION: parse_nmap_output()
#
#    Parses Nmap output and extracts IP addresses, hostnames, port numbers,
#    protocols, states, and descriptions.
#
#    Parameters:
#        nmap_output (str): The Nmap output to parse.
#
#    Returns:
#        list: A list of tuples containing parsed information for each port.
#              Each tuple contains IP, HOSTNAME, PORT, PROTO, STATE, DESCRIPTION
#----------------------------------------------------------------------
def parse_nmap_output(nmap_output):
    hosts = re.split(r'\n(?=Nmap scan report for)', nmap_output.strip())

    results = []

    for host in hosts:
        host_info = host.split('\n')
        ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', host_info[0])
        ip_address = ip_match.group() if ip_match else ""
        hostname_match = re.match(r'Nmap scan report for (.+?) \(', host_info[0])
        if hostname_match:
            hostname = hostname_match.group(1)
        else:
            hostname = "unknown"

        port_lines = [line for line in host_info if re.match(r'^\d+/(.+?)\s+(.+?)\s+(.+)', line)]

        if port_lines:
            for line in port_lines:
                port_match = re.match(r'^(\d+)/(.*?)\s+(.+?)\s+(.+)', line)
                port_number = port_match.group(1)
                port_proto = port_match.group(2)
                port_state = port_match.group(3)
                port_description = port_match.group(4)
                results.append((ip_address, hostname, port_number, port_proto, port_state, port_description))
        elif ip_address:
                results.append((ip_address, hostname, "-", "-", "-", "-"))

    return results


#----------------------------------------------------------------------
#    FUNCTION: print_to_stdout()
#
#    Prints the parsed Nmap data in CSV format to stdout.
#
#    Parameters:
#        data (list): A list of tuples containing parsed Nmap information.
#                     Each tuple contains (IP, HOSTNAME, PORT, PROTO, STATE, DESCRIPTION).
#        add_empty_lines (bool): Whether to add empty lines between each new block of IP addresses.
#----------------------------------------------------------------------
def print_to_stdout(data, add_empty_lines):

    print("IP,HOSTNAME,PORT,PROTO,STATE,DESCRIPTION")
    last_ip = None
    for line in data:
        if add_empty_lines and last_ip and line[0] != last_ip:
            print()
        print(','.join(line))
        last_ip = line[0]


#----------------------------------------------------------------------
# Main function to execute the script.
#----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="This script parses Nmap output and converts it into a CSV format.")
    parser.add_argument('-d', '--delimiter', action='store_true', help='Add an empty line between each new block of IP addresses.')
    parser.add_argument('file', nargs='?', help='Specifies the file containing Nmap output. If not provided, the script reads from stdin.')

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            nmap_output = file.read()
    else:
        nmap_output = sys.stdin.read()

    parsed_data = parse_nmap_output(nmap_output)

    # Sort the parsed data by IP address and then by port number
    sorted_data = sorted(parsed_data, key=lambda x: (ipaddress.ip_address(x[0]), int(x[2]) if x[2].isdigit() else -1))

    print_to_stdout(sorted_data, args.delimiter)

if __name__ == "__main__":
    main()
