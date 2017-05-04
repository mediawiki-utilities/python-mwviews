"""
Aggregates page view counts from hourly page view files
into a single pageview file

Usage:
    aggregate (-h|--help)
    aggregate <hour-file>...
              [--projects=<prefixes>]
              [--output=<path>]
              [--debug]
              [--verbose]

Options:
    -h --help               Prints this documentation
    <hour-file>             Path to an pageviews hourly file to process
    --projects=<prefixes>   A "|" separated list of project prefixes that
                            should be included in the output
                            (e.g. "en|en.mw")
    --output=<path>         A file to write output to [default: <stdout>]
"""
import gzip
import logging
import sys
import urllib
from itertools import groupby

import docopt

from . import util
from ..page_view_count import PageViewCount

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    logging.basicConfig(
        level=logging.WARNING if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    hour_files = [open_hour_file(p) for p in args['<hour-file>']]
    logger.info("Reading from {0} files".format(len(hour_files)))

    if args['--projects'] is not None:
        project_prefixes = set(p.strip()
                               for p in args['--projects'].split("|"))
    else:
        project_prefixes = None

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(args['--output'], "w")

    verbose = args['--verbose']

    run(hour_files, project_prefixes, output, verbose)


def run(hour_files, project_prefixes, output, verbose):
    page_view_counts = [(PageViewCount.from_line(line)
                         for line in hf)
                        for hf in hour_files]

    grouped_page_view_counts = groupby(
        util.collate(*page_view_counts),
        key=lambda pvc: (pvc.project, pvc.page_name))

    for (project, page_name), pvcs in grouped_page_view_counts:
        aggregate_views = 0
        aggregate_bytes = 0
        for pvc in pvcs:
            aggregate_views += pvc.views
            aggregate_bytes += pvc.bytes_returned

        aggregate_pvc = PageViewCount(
            project, page_name, aggregate_views, aggregate_bytes)

        output.write(aggregate_pvc.to_line())
        output.write("\n")

        if verbose:
            sys.stderr.write(".")
            sys.stderr.flush()

    if verbose:
        sys.stderr.write("\n")
        sys.stderr.flush()


def open_hour_file(path):
    if path[-3:] == ".gz":
        return gzip.open(path, mode="rt", encoding="utf-8", errors="replace")
    else:
        return open(path, mode="rt", encoding="utf-8", errors="replace")
