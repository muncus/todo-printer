# encoding:utf8

import todoist
import yaml

import argparse

parser = argparse.ArgumentParser(description='Get ToDoist list')
parser.add_argument('--debug', '-d', help='add debugging output')
parser.add_argument('--config', '-c', help='yaml config file with token')
parser.add_argument('--token', '-t', metavar='TOKEN', nargs=1,
                    help='api token')

args = parser.parse_args()

if args.config:
    cfg = yaml.load(file(args.config))
    args.token = cfg['token']
tdc = todoist.TodoistAPI(token=args.token)

qresults = tdc.query(["viewall"])
if args.debug:
    print qresults
project_list = qresults[0]['data']
for p in project_list:
    print p['project_name']
    for todo in p['uncompleted']:
        print u"\u2610  %s" % todo['content']

