"""
Fetches a JSON file containing information about all namespace
names and aliases across all wikis using
action=query&meta=siteinfo.  This file is used later by
to parse page names into (namespace, title)
pairs.

Usage:
    fetch_global_namespaces (-h|--help)
    fetch_global_namespaces [<dbname-file>]
                            [--debug] 
                            [--verbose]

Options:
    -h, --help     Prints this documentation
    <dbname-file>  Path to json file to process. If no file is 
                   provided, uses stdin
    --debug        Print debug logging to stderr
    --verbose      Print dots and stuff to stderr  
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


    verbose=args['--verbose']

    run(dbname_file, verbose)

def run(dbname_file, verbose):

    canonical_namespaces = defaultdict(lambda : defaultdict(dict))
    temp_namespace_id_to_information = defaultdict(lambda : defaultdict(dict))

    for line in dbname_file:

        wikidb_dictionary = json.loads(line)
        namespace_information_from_api = mwapi.Session(wikidb_dictionary['wikiurl']).get(action="query", meta="siteinfo", siprop="namespaces|namespacealiases")

        # tem



        for namespace_id in namespace_information_from_api['query']['namespaces']:
            current_information = namespace_information_from_api['query']['namespaces'][namespace_id]
            namespace = current_information['*']
            if 'canonical' not in current_information:
                current_information['canonical'] = namespace
            del(current_information['*'])
            canonical_namespaces[wikidb_dictionary['dbname']][namespace] = current_information
            temp_namespace_id_to_information[wikidb_dictionary['dbname']][current_information['id']] = current_information


        for namespace_aliases in namespace_information_from_api['query']['namespacealiases']:
            canonical_namespaces[wikidb_dictionary['dbname']][namespace_aliases['*']] = temp_namespace_id_to_information[wikidb_dictionary['dbname']][namespace_aliases['id']]

    # for entry in canonical_namespaces:
    #     print (canonical_namespaces[entry])


    sys.stdout.write(json.dumps(canonical_namespaces))





# """
# Prints page_names with ids.

# Usage:
#     page_title_and_id_linker (-h|--help)
#     page_title_and_id_linker <date> [<dbname-file>]
#                             [--dump-host=<url>]
#                             [--debug] 
#                             [--verbose]


# Options:
#     -h, --help         This help message is printed
#     <dbname-file>      Path to json file to process. If no file is 
#                        provided, uses stdin
#     <date>             Date when the sql were files were produced. 
#                        Format: yyyymmdd
#     --dump-host=<url>  If the host is different than the default 
#                        Wikimedia host:
#                        [default: https://dumps.wikimedia.org]
#     --debug            Print debug logging to stderr
#     --verbose          Print dots and stuff to stderr  
# """



# import logging
# import requests
# import sys
# import re
# import json
# import mwxml
# import gzip
# from collections import defaultdict

# import docopt

# logger = logging.getLogger(__name__)

# def main(argv=None):
#     args = docopt.docopt(__doc__, argv=argv)
#     logging.basicConfig(
#         level=logging.WARNING if not args['--debug'] else logging.DEBUG,
#         format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
#     )

#     if args['<dbname-file>']:
#         dbname_file = args['<dbname-file>']
#     else:
#         logger.info("Reading from <stdin>")
#         dbname_file = sys.stdin

#     if re.match(r"^\d{8}$",args['<date>']):
#         date = args['<date>']
#     else:
#         raise RuntimeError("Please provide a data in the format: yyyymmdd")

#     dump_host = args['--dump-host']
#     verbose=args['--verbose']

#     run(dbname_file, date, dump_host, verbose)


# def run(dbname_file, date, dump_host, verbose):
#     for line in dbname_file:

#         wikidb_dictionary = json.loads(line)

#         redirects = defaultdict(dict)
#         non_redirects = defaultdict(dict)
#         namespace_names = {}

#         sub_directory = wikidb_dictionary['dbname'] + "/" + date
#         stub_file_name = wikidb_dictionary['dbname'] + "-" + date + "-" +\
#             "stub-meta-current.xml.gz"

#         stub_file_dump = requests.get(dump_host + "/" +
#             sub_directory + "/" + stub_file_name, stream=True)
#         if stub_file_dump.status_code != 200:
#             logger.warn("{0} could not be downloaded. {1}"
#                 .format(stub_file_name, "HTTP code: " + 
#                 str(stub_file_dump.status_code)))
#             continue

#         #Now we process the stream, parsing xml using mwxml 

#         f = gzip.open(stub_file_dump.raw,"rb")
#         stub_file_dump_object = mwxml.Dump.from_file(f)

#         # Extract namespace names
#         for namespace in stub_file_dump_object.site_info.namespaces:
#             namespace_names[namespace.id] = namespace.name


#         for stub_file_page in stub_file_dump_object:
#             print("HERE")
#             namespace_and_title_string =\
#                 create_namespace_and_title_string(namespace_names, 
#                                                   stub_file_page.namespace, 
#                                                   stub_file_page.title)
#             if stub_file_page.redirect == None:
#                 non_redirects[namespace_and_title_string] = stub_file_page.id
#                 print_linking(wikidb_dictionary['dbname'], 
#                               namespace_and_title_string, 
#                               False, 
#                               stub_file_page.id)
#             else:
#                 redirects[namespace_and_title_string] = stub_file_page.redirect

#         print("DONE")
#         for namespace_and_title in redirects:
#             print("ANALYZING REDIRECTS")
#             if redirects[namespace_and_title] in non_redirects:
#                 print_linking(wikidb_dictionary['dbname'], 
#                               namespace_and_title, 
#                               True, 
#                               non_redirects[redirects[namespace_and_title]])
#             else:
#                 logger.warn("The redirect \"" + redirects[namespace_and_title] +
#                     "\" for \"" + namespace_and_title +"\" does not appear to "
#                     + "be a page.")


# def print_linking(dbname, namespace_and_title, redirect, page_id):
#     sys.stdout.write(json.dumps(
#         {
#             'dbname' : dbname,
#             'namespace_and_title': namespace_and_title,
#             'redirect': redirect,
#             'page_id': page_id
#         }) + "\n")


# def create_namespace_and_title_string(namespace_names, namespace, title):
#     if namespace == 0:
#         return title
#     else:
#         return namespace_names[namespace] + ":" + title





