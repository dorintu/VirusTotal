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
* If this is a site that has not yet been tested (i.e. does not exist in the URLs_Status file) - check it and add a new line to the URLs_Status file with its data
* If this is a site that has not been tested for more than 30 minutes (i.e. sysdate - their Sample_Time > 30 minutes), check it and update its data
* If this is a site that has been tested for the last half hour you will not do anything
