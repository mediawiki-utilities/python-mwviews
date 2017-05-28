"""
Fetches a JSON file containing information about all namespace
names and aliases across all wikis using
action=query&meta=siteinfo.  This file is used later
to parse page names into (namespace, title)
pairs.

Usage:
    fetch_global_namespaces (-h|--help)
    fetch_global_namespaces [<dbname-file>]
                            [--api-agent=<username>]
                            [--debug] 
                            [--verbose]

Options:
    -h, --help             Prints this documentation
    <dbname-file>          Path to json file to process. If no file is 
                           provided, uses stdin
   --api-agent=<username>  Username for API session. [default: Unknown]
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
        dbname_file = args['<dbname-file>']
    else:
        logger.info("Reading from <stdin>")
        dbname_file = sys.stdin

    api_agent = args['--api-agent']
    verbose = args['--verbose']

    run(dbname_file, api_agent, verbose)

def run(dbname_file, api_agent, verbose):

    canonical_namespaces = defaultdict(lambda : defaultdict(dict))
    temp_namespace_id_to_information = defaultdict(lambda : defaultdict(dict))

    for line in dbname_file:

        wikidb_dictionary = json.loads(line)

        if verbose:
            sys.stderr.write("Processing: " + str(wikidb_dictionary) + "\n")
            sys.stderr.flush()

        try:
            namespace_api_information =\
            mwapi.Session(wikidb_dictionary['wikiurl'], user_agent=api_agent).\
            get(action="query", meta="siteinfo", 
            siprop="namespaces|namespacealiases")
        except mwapi.errors.APIError as e:
            logger.warn("{0}. Skipping {1}".
                format(e, wikidb_dictionary['dbname']))
            continue
        except mwapi.errors.ConnectionError as e:
            logger.warn("{0}. Skipping {1}".
                format(e, wikidb_dictionary['dbname']))
            continue


        namespace_api_entries = namespace_api_information['query']['namespaces']
        for namespace_id in namespace_api_entries:
            current_information = namespace_api_entries[namespace_id]
            namespace = current_information['*']
            if 'canonical' not in current_information:
                current_information['canonical'] = namespace
            del(current_information['*'])
            canonical_namespaces[wikidb_dictionary['dbname']][namespace] =\
                current_information
            temp_namespace_id_to_information\
                [wikidb_dictionary['dbname']]\
                [current_information['id']] = current_information

        namespace_alias_api_entries =\
            namespace_api_information['query']['namespacealiases']

        for namespace_aliases in namespace_alias_api_entries:
            canonical_namespaces[wikidb_dictionary\
                ['dbname']]\
                [namespace_aliases['*']] = temp_namespace_id_to_information\
                                               [wikidb_dictionary['dbname']]\
                                               [namespace_aliases['id']]


    sys.stdout.write(json.dumps(canonical_namespaces))

