# Average name of Rice UG

## The average name (2019) is `aani san`, and with the `-l` option it's `aaniennneeret sannenaeiairrezeiais`.

This script computes the average name of current Rice undergrads (taken from `search.rice.edu`). It defines the average name as the name comprised of the most common letter for each position in the name. So really it's more of a "mode" sort of calculation. 

To reconcile long/short names, whitespace is padded to the end of short names up until the length of the longest name. Use the `-l` flag to compute the average name without this padding (longer names will have more weight over the latter portions of the average name).  

