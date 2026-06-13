# Deadline-guard spot baseline for cant-late-la-loose-large-frontier-cs-cbl-la-ll

This baseline uses spot capacity when it is currently available and deadline slack remains healthy. It waits through early spot outages, then locks to on-demand once remaining work plus restart overhead approaches the deadline. It does not inspect hidden traces or tune to public fixture answers.
