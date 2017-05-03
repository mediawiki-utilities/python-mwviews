"""
Aggregates page view counts from hourly page view files into a single pageview file

Usage:
    aggregate (-h|--help)
    aggregate <hour-file>...
              [--namespaces=<path>]
              [--projects=<prefixes>]

Options:
    -h --help               Prints this documentation
    <hour-file>             Path to an pageviews hourly file to process
    --namespace=<path>      Path of a file produced by
                            `fetch_global_namespaces` for processing
                            namespace prefixes (e.g. "Talk:...")
    --projects=<prefixes>   A "|" separated list of project prefixes that
                            should be included in the output
                            (e.g. "en|en.mw")
"""
import docopt

def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    print("Hello Aggregate!")
