# VirusTotal-Domain-Scanner

Takes an CSV file (input) with domains and passes them to the VT API. then writes the following items to a CSV file (output) with the data: 
* URL
* Sample_Time - The time at which the last test was performed
* Site's_Risk - safe / risk site
* Total_Voting - how many anti-viruses voted for this URL

## Description of my Solution

The user is exposed to a function through which he can insert a path of a CSV file that contains a list of sites to test. 
The program assumes that the user will use the on-going function whenever he enters a path of a CSV file with a list of sites he wants to test.
The sites can be: new sites that have not yet been tested, or sites that have been tested before.

The program checks the sites it received in the input file according to the following logic:
* If these are sites that have not been reviewed yet (i.e. do not exist in the URLs_Status file) - check them and insert a new line into the URLs_Status file with their data
* If these sites have not been tested for more than 30 minutes (i.e. their Sample_Time - sysdate > 30 minutes), check them and update their data
* If these are sites that have been tested in the last half hour do nothing for them
