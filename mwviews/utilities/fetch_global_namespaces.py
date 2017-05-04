"""
Fetches a JSON file containing information about all namespace
names and aliases across all wikis using action=sitematrix and
action=query&meta=siteinfo.  This file is used later by
`aggregate` to parse page names into (namespace, title)
pairs.

Usage:
    fetch_global_namespaces (-h|--help)
    fetch_global_namespaces <api-host>

Options:
    -h --help   Prints this documentation
    <api-host>  URL for the MediaWiki host to query for
                action=sitematrix
"""
import docopt

def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    print("Hello Fetch Global Namespaces!")

