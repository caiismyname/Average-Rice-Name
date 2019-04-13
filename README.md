# Average name of Rice UG

- The average name (2019) is `Aani San`. 
- With the `-l` option it's `Aaniennneeret Sannenaeiairrezeiais`.
- Using the smoothing option (`-s`), the average name is `Aaaiie Saaaenn`
- Using smoothing with true mean (`-s -a`), the average name is `Ijijkjj Kkjkkk`.

This script computes the average name of current Rice undergrads (taken from `search.rice.edu`). It defines the average name as the name comprised of the most common letter for each position in the name. So really it's more of a "mode" sort of calculation. 

To reconcile long/short names, two options are given:
- Whitespace is padded to the end of short names up until the length of the longest name. Use the `-l` flag to compute the average name without this padding (longer names will have more weight over the latter portions of the average name).  
- All names are stretched to the length of the longest name, the average is computed, and a name of the average length is extracted. Use `-s` to use this stretching option. This option also has the choice of defining average as frequency (no additional flag) or true mathematical mean on the ASCII values (`-a` flag). 

This project was inspired by [u/altiarblade's post on reddit](https://www.reddit.com/r/nba/comments/bcm86k/oc_what_was_the_average_name_of_an_nba_player_in/).
