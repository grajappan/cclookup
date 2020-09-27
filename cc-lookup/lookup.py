#!/usr/bin/env python3
"""Lookup Country.

Usage:
  lookup.py (--countryCode=<XX>)

Options:
  -h --help     Show this screen.
  --countryCode Input the comma separated country code

"""
from docopt import docopt
import json
import requests
import os.path
import sys
def lookup(cc):
    countryName = ''
    with open('./data.json','r') as json_file:
        cdict = json.load(json_file)
        for k, v in cdict['data'].items():
            if k == cc:
                for i in v:
                    if i == 'name':
                        countryName=v['name'] 
    #Can use this way as well countryName = cdict['data'].get(cc).get('name')
    if countryName != '':
        return (countryName)
    else:
        return ("Country code not valid")

def fetch():
    countrylist = 'https://www.travel-advisory.info/api'
    try:
        res = requests.get(countrylist)
    except Exception as e:
        print ("Error occurred while retrieving the country code. Error details:\n{}".format(e))
        sys.exit(1) 
    f = open('./data.json','w')
    f.write(json.dumps(res.json()))
    f.close()
            
def apiConvert(cc):
    if os.path.isfile('./data.json'):
        ret = lookup(cc)
    else:
        fetch()
        ret = (lookup(cc))
    return ret

def apiDiag():
    try:
        res = requests.get('https://www.travel-advisory.info/api')
    except Exception as e:
        return ("Unable to get diagnostics")
    rdict = res.json()
    for k, v in rdict.items():
        if k == 'api_status':
            return {k:v}


def health():
    try:
        res = requests.get('https://www.travel-advisory.info/api')
    except Exception as e:
        return 404
    rdict = res.json()
    for k, v in rdict.items():
        if k == 'api_status':
            for i, j in v.items():
                if i == 'reply':
                    for a, b in j.items(): 
                        if a == 'code':
                            return b

if __name__ == '__main__':
    args = docopt(__doc__)
    cc = [cc.strip() for cc in args['--countryCode'].split(',')]
    for i in cc:
        if len(i) > 0:
            if os.path.isfile('./data.json'):
                print(lookup(i))
            else:
                fetch()
                print(lookup(i))
        else:
            print("Please enter the proper country code")
            exit
    
