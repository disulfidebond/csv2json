# csv2json
convert csv files to json

## Usage
Type *python csvToJson.py* to run.  Options will appear in commandline to guide you through the file conversion.

Currently, the following options are required/supported:
* All values for the JSON must be in the header file
* only 1 level of recursion is supported, i.e. if the header has 
  * Name,FirstName,LastName,NickName,
  * You are limited to one of:
    * 'Name' : { 'FirstName' : ..., 'LastName': ...,}
    * 'Name' : [ 'FirstName', 'LastName', 'Nickname']
    * 'Name' : { 'Nickname' : ..., 'LastName': ...}
* After creating the framework from the header, the script will automagically run through all rows of the csv file using the settings that were established, and populate the JSON file accordingly.
