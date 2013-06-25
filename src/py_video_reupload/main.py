import os
import sys
import threading
import hashlib
import json
import re
import time
import subprocess
import argparse
import http.client as httplib
from you_get.downloader import *
from io import StringIO
from urllib.parse import urlparse

class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        
def parseJSONFromURL(url):
    """ Parse JSON from GET response """
    
    parsedUrl = urlparse(url)

    if parsedUrl.scheme == "https":
        conn = httplib.HTTPSConnection(parsedUrl.netloc)
    else:
        conn = httplib.HTTPConnection(parsedUrl.netloc)
        
    conn.request("GET", parsedUrl.path+'?'+parsedUrl.query)
    response = conn.getresponse()
    
    return json.loads(response.read().decode('utf-8'))
    

class app:
    videoHandlers = {'youtube.com': youtube, 'vimeo.com': vimeo, 'dailymotion.com': dailymotion, 'blip.tv': blip}
    outputDir = ""
    hooks = dict()
    info = dict()
    threads = dict()
    
    def __init__(self, args):
        self.args = args

    def getVideoMeta(self, url, host):
        """ Get video meta data if avaliable """
    
        if host == "youtube.com":
            videoID = re.findall('watch\?v=([0-9A-Za-z\-\_]+)', url)
            meta = parseJSONFromURL('https://gdata.youtube.com/feeds/api/videos/'+videoID[0]+'?v=2&alt=jsonc')
            return {'title': meta['data']['title'], 'description': meta['data']['description']}
            
        return None

    def main(self):
        """ Main loop """
    
        # execute main loop
        if "gui" in self.args:
            if self.args['gui'] == 'qt4':
                import py_video_reupload.qtgui
                gui = py_video_reupload.qtgui.main(self)
                

    def getVideoInfo(self, url):
        """ Get video file size """
        
        # parse url and get correct handler name
        domainName = urlparse(url).netloc.replace("www.", "").lower()
        
        # check if handler exists
        if domainName in self.videoHandlers:
            handler = self.videoHandlers[domainName]
        else:
            raise Exception('Invalid video handler')
            
        output = StringIO()
        
        with RedirectStdStreams(stdout=output):
            handler.download(str(url), info_only = True)
            
        matches = re.findall("\(([0-9]+) Bytes\)", output.getvalue())
        self.videoSize = matches[0]
        
        if len(matches) == 0:
            return None
        
        return {'size': self.videoSize, 'meta': self.getVideoMeta(url, domainName), 'link': url, 'domain': domainName}
        
    #### Working threads
        
    def startDownload(self, info):
        """ Start downloading """
        
        self.info = info
        
        self.threads['_startDownloadCheck'] = threading.Thread(target=self._startDownloadCheck)
        self.threads['_startDownloadCheck'].start()
        
        self.threads['_startDownloadFile'] = threading.Thread(target=self._startDownloadFile)
        self.threads['_startDownloadFile'].start()
        
    
    def _startDownloadCheck(self):
        """ Update progress bars etc. """
        
        while True:
            time.sleep(0.5)
            
            try:
                fileName = os.listdir(self.outputDir)[0]
                fileSize = os.path.getsize(self.outputDir+"/"+fileName)
                self.hooks['downloadCheck'](str(fileSize), str(self.info['size']))
                
                # finish
                if int(fileSize) >= int(self.info['size']):
                    return True
                    
            except Exception as e:
                print(e)
        
    def _startDownloadFile(self):
        """ File download thread """
    
        handler = self.videoHandlers[self.info['domain']]
        self.outputDir = '/tmp/'+hashlib.md5(self.info['link'].encode('utf-8')).hexdigest() 
        
        print(self.outputDir)
        
        if not os.path.isdir(self.outputDir):
            os.mkdir(self.outputDir)
            
        print('you-get '+self.info['link']+' -o '+self.outputDir)
        subprocess.getoutput('you-get --output-dir='+self.outputDir+' '+self.info['link'])
        
    #### End of working threads
    
        
    def exit(self, a='', b='', c=''):
        """ Stop all threads and exit application """
        
        print("Stopping threads...")
    
        for t in self.threads:
            self.threads[t]._stop()
    
        print("Exiting.")
        sys.exit(0)

        
def main():
    parser = argparse.ArgumentParser(description='Video file reupload', prog='py-video-reupload')
    parser.add_argument('--gui', nargs='?', default='qt4', type=str, help='select gui to use, eg. qt4 or shell')
    args = vars(parser.parse_args())
    a = app(args)
    a.main()
