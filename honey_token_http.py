# Honey Token HTTP
# Simple Python based HTTP server to log Honey Token use
# (c) Tim Crothers - badsecurity@gmail.com
# v1.0 - Sep 19, 2022
# Released under GNU General Public License (GPL)

from http.server import BaseHTTPRequestHandler, HTTPServer
import pandas as pd
import argparse
import logging

parser = argparse.ArgumentParser(description ='Simple HTTP server for collecting Honey Tokens')

parser.add_argument('-o', dest = 'outfile', action ='store', help ='output log file')
parser.add_argument('-s', dest = 'hName', action ='store', help ='source host name or IP')
parser.add_argument('-p', dest = 'Port', action='store', help ='source port')
parser.add_argument('-c', dest = 'catalogfile', action='store', help='token catalog file, must be comma delimited with fields of Token ID, Hostname, and Alert Message')

args = parser.parse_args()

if args.hName == None:
    hName = "localhost"
else:
    hName = args.hName
    
if args.Port == None:
    Port = 8080
else:
    Port = int(args.Port)
    
if args.outfile == None:
    outfile = 'honey_token_http.log'
else:
    outfile = args.outfile
    
if args.catalogfile == None:
    catalogfile = 'token_catalog.csv'
else:
    catalogfile = args.catalogfile

logging.basicConfig(filename=outfile, level=logging.INFO, format='%(asctime)s%(message)s', datefmt='%m/%d/%Y,%H:%M:%S,')

TokenRecords = pd.read_csv(catalogfile, names=['Token_ID','Host','Alert_Message'])

class wser (BaseHTTPRequestHandler):
    def do_GET (self):
        self.send_response (200)
        self.send_header ("Content-type", "text/html")
        self.end_headers ()
        self.wfile.write (bytes ("<html><body>", "utf-8"))
        self.wfile.write (bytes ("<img src=""data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAAtJREFUGFdjYAACAAAFAAGq1chRAAAAAElFTkSuQmCC"">", "utf-8"))
        self.wfile.write (bytes ("</body></html>", "utf-8"))
        client_ip = self.client_address[0]
        token = self.path.split(".")[0]
        token = token[1:]
        print("Host ",client_ip,"requested token",token)
        
        logmesg = token+','+client_ip+',requested'
        logging.info(logmesg)
        
        i = 0
        tokenfound = False
        
        while i < len(TokenRecords):
            if token == str(TokenRecords.at[i, 'Token_ID']):
                message = "ALERT: Token "+token+" on host "+str(TokenRecords.at[i,'Host'])+" with alert message: "+str(TokenRecords.at[i,"Alert_Message"])+"!"
                logmesg = token+","+str(TokenRecords.at[i,'Host'])+","+str(TokenRecords.at[i,"Alert_Message"])
                tokenfound = True
            i+=1
        
        if tokenfound != True:
            message = "ALERT: Unknown Token "+token
            logmesg = token+",unknown,unknown"
        
        print(message)
        logging.info(logmesg)
    
    def do_OPTIONS (self):
        self.send_response (200)
        print('OPTIONS called')
        
    def do_POST (self):
        self.send_response (200)
        print('POST called')
    
    def do_HEAD (self):
        self.send_response (200)
        print('HEAD called')
        
    def do_PUT (self):
        self.send_response (200)
        print('PUT called')
        
    def do_DELETE (self):
        self.send_response (200)
        print('DELETE called')
        
    def do_CONNECT (self):
        self.send_response (200)
        print('CONNECT called')
        
    def do_TRACE (self):
        self.send_response (200)
        print('TRACE called')
        
                    
if __name__ == "__main__":
    webser = HTTPServer((hName, Port), wser)
    print("Server started http://%s:%s" % (hName, Port))

    try:
        webser.serve_forever()
    except KeyboardInterrupt:
        pass

    webser.server_close()
    print("Server stopped.")    
