import os
import urllib
from urllib.parse import urlparse
import pickle
import datetime
import requests
import morphqs.logging.loghandler as loghandler

logger = loghandler.get_logger(__name__)
class RequestsApi():
    def __init__(self, **kwargs, ):
        self.base_url = os.environ.get('baseurl')
        
        # Session management starting process. 
        urlData = urlparse(self.base_url)
        self.maxSessionTime = 30 * 60
        sessionFileAppendix = '_session.dat'
        logger.debug("SESSION MGMT")
        logger.debug(urlData)
        logger.debug(self.maxSessionTime)
        logger.debug(sessionFileAppendix)
        #instancename = urllib.parse.quote(os.environ.get("instancename"))
    
        self.sessionFile =urlData.netloc + sessionFileAppendix
        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])
        self.session_handling()
        
    @staticmethod
    def modification_date(filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)
    
    def session_handling(self):
        wasReadFromCache = None
        if not wasReadFromCache:
            self.bearer_token = os.environ.get('bearertoken')
            logger.debug('##############################')
            logger.debug("Session handling: from env")
            logger.debug(self.bearer_token)
            logger.debug(self.base_url)
            logger.debug('##############################')
            self.headers = {"accept": "application/json", "authorization": f"Bearer {self.bearer_token}"}
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            self.session.verify = False

            
            self.saveSessionToCache()
    def saveSessionToCache(self):
        with open(self.sessionFile, "wb") as f:
            pickle.dump(self.session, f)
        f.close()
            
    def request(self, method, url, **kwargs):
        return self.session.request(self.base_url+url, **kwargs)
    def get(self, url, **kwargs):
        return self.session.get(self.base_url+url, **kwargs)
    def post(self, url, **kwargs):
        logger.debug(self.base_url+url)
        return self.session.post(self.base_url+url, **kwargs)
    def put(self, url, **kwargs):
        return self.session.put(self.base_url+url, **kwargs)
    def delete(self, url, **kwargs):
        return self.session.delete(self.base_url+url, **kwargs)
    def close(self):
        logger.warning('Closing session')
        return self.session.close()
    
    
    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value,dict):
                node = destination.setdefault(key, {})
                RequestsApi.__deep_merge(value,node)
            else:
                destination[key] = value
        return destination

