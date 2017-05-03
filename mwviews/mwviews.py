import mwcli

router = mwcli.Router(
    "mwviews",
    "This script provides access to a set of utilities for processing view counts.",
    {'aggregate': "Aggregate view counts from hourly view files",
     'fetch_global_namespaces': "Fetches a dataset of namespace names for all wikis"}
)

main = router.main
