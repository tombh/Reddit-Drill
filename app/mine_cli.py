from mine_json import Miner
import argparse


parser = argparse.ArgumentParser(description='Create JSON for the JIT graph visualiser from a Reddit story or comment.')
parser.add_argument('url', help='Valid Reddit URL')
args = parser.parse_args()

miner = Miner(args.url)
tree = miner.populate()

#write out the results
pprint('writing...')

f_debug = open(os.getcwd() + 'drill.json', 'w')
f_debug.write(json.dumps(tree))

pprint('fin')

