# honey_token_http
Honey_token_http

Honey_token_http is a simple web server written in Python 3 for the purpose of simplifying the use and management of honey tokens.

The main python file uses http_server and Pandas to log and respond to token requests.  What makes this unique is that the server responds with an HTTP 200 response regardless of the query URL and responds with a 1 pixel by 1 pixel transparent PNG.  The URL is logged as a token ID and also looked up from the token_catalog file.  If the token id exists in the token_catalog file then the corresponding host and description are added to the log file for alerting purposes.

Note that since this is based on the http.server module you should not expose the system externally <B>nor run it with administrative credentials</B>.  It can run perfectly fien as an ordinary user.  The http.server python module does not contain much in the way of security.  Should you need something more secure consider using flask or another python http server which contains more robust security.

The token_catalog file is a simple text file of comma delimited consisting of three fields - token id, hostname, and alert message.  

usage: honey_token_http.py [-h] [-o OUTFILE] [-s HNAME] [-p PORT] [-c CATALOGFILE]

Simple HTTP server for collecting Honey Tokens

options:
  -h, --help      show this help message and exit
  
  -o OUTFILE      output log file
  
  -s HNAME        source host name or IP
  
  -p PORT         source port
  
  -c CATALOGFILE  token catalog file, must be comma delimited with fields of Token ID, Hostname, and Alert Message
  
To use honey_token_http, execute it on a host with desired port.  Then distribute the tokens on hosts with network access to the running honey_token_http address and port via http://honey_token_http-hostname/token_id.png.  Each time the server is accessed two entries will be put in the output log file.  One will be the request information and the second will be the token_id, hostname, and alert message.  This allows you to leverage Security Onion or a similar alerting platform to easily monitor and alert on new token uses within your organization.

honey_token_http is Copyright 2022, Tim Crothers.  It is released open source using the GNU General Public License (GPL).  All rights reserved.
