# bdn2csv

bdn2csv is a Python parser that converts SAS Business Data Network (BDN) XML Export file to CSV Import file

As the SAS BDN can be:
* imported from XML or CSV file but
* exported only to XML file,

bdn2csv transforms an XML Export file into an equivalent CSV Import file:

* for a user to edit it manually as a spreadsheet

* for a developer to process it programmatically as a table

and to import the result CSV file into SAS BDN.
