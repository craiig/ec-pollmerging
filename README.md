Election's Canada publishes voting data in a somewhat weird format, sometimes occasionally splitting polls that represent the same geographic region into two or more polls. This code downloads all the polling data, merges together those rows and generates a similar csv file to the original. A new column is added showing you which poll numbers were merged.

This should help when trying to do things like mapping data for each polling region, where the polling region maps omit all of this A,B,C suffix nonsense.

Tested with data sourced from this URL:
http://www.elections.ca/scripts/resval/ovr_41ge.asp

Usage:
make getzips (downloads the data and unzips)
make (merges the new rows)

Known issues:
* Hacky code
* Bad Unicode handling :( :( i.e. if you're wondering why some of the french names are broken this is why. If you really need unicode support for this, get in contact.
