"""
Fetches a JSON file containing information about all namespace names and aliases
across all wikis using action=query&meta=siteinfo.  This file is used later to 
parse page names into (namespace, title) pairs.

Usage:
    fetch_global_namespaces (-h|--help)
    fetch_global_namespaces [<dbname-file>]
                            [--api-agent=<username>]
                            [--output=<path>]
                            [--debug] 
                            [--verbose]

Options:
    -h, --help             Prints this documentation
    <dbname-file>          Path to json file to process. If no file is 
                           provided, uses stdin
   --api-agent=<username>  Username for API session. Please provide name and
                           email, in quotes
                           (e.g. "John Doe johndoe@johndoe.com"). If api agent 
                           not specified, MWAPI warning will be printed.
   --output=<path>         A file to write output to. [default: <stdout>]
    --debug                Print debug logging to stderr
    --verbose              Print dots and stuff to stderr  
"""
import docopt
import logging
import mwapi
import sys
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    logging.basicConfig(
        level=logging.WARNING if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    if args['<dbname-file>']:
        dbname_file = open(args['<dbname-file>'], "r")
    else:
        logger.info("Reading from <stdin>")
        dbname_file = sys.stdin

    api_agent = args['--api-agent']

    if args['--output'] == '<stdout>':
        output = sys.stdout
    else:
        output = open(args['--output'], "w")

    verbose = args['--verbose']

    run(dbname_file, api_agent, output, verbose)

def run(dbname_file, api_agent, output, verbose):
    canonical_namespaces = defaultdict(lambda : defaultdict(dict))
    namespace_id_to_entry = defaultdict(lambda : defaultdict(dict))

    for line in dbname_file:

        wikidb_dict = json.loads(line)

        if verbose:
            sys.stderr.write("Processing: " + str(wikidb_dict) + "\n")
            sys.stderr.flush()

        if api_agent:
            user_agent_string = "user_agent=" + api_agent
        else:
            user_agent_string = None

        try:
            api_namespaces =\
            mwapi.Session(wikidb_dict['wikiurl'],user_agent_string).\
            get(action="query", meta="siteinfo", 
            siprop="namespaces|namespacealiases")
        except mwapi.errors.APIError as e:
            logger.warn("{0}. Skipping {1}".
                format(e, wikidb_dict['dbname']))
            continue
        except mwapi.errors.ConnectionError as e:
            logger.warn("{0}. Skipping {1}".
                format(e, wikidb_dict['dbname']))
            continue


        api_namespace_entries = api_namespaces['query']['namespaces']
        
        for namespace_id in api_namespace_entries:
            current_entry = api_namespace_entries[namespace_id]
            namespace = current_entry['*']

            if 'canonical' not in current_entry:
                current_entry['canonical'] = namespace

            del(current_entry['*'])

            canonical_namespaces[wikidb_dict['dbname']][namespace] =\
                current_entry
            namespace_id_to_entry[wikidb_dict['dbname']][current_entry['id']] =\
                current_entry

        alias_api_entries = api_namespaces['query']['namespacealiases']

        for aliases in alias_api_entries:
            canonical_namespaces[wikidb_dict['dbname']][aliases['*']] =\
                namespace_id_to_entry[wikidb_dict['dbname']][aliases['id']]


    output.write(json.dumps(canonical_namespaces))

