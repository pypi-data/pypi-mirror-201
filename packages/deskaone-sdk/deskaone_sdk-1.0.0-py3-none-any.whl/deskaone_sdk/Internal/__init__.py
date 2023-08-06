import json
from requests.exceptions import ConnectionError, ConnectTimeout, ProxyError, ReadTimeout, JSONDecodeError, TooManyRedirects
import requests
from deskaone_sdk.Exceptions import Error


class Internal:
    
    def __init__(self, *args, **kwargs) -> None:
        """A Internal Requests.
        
        Basic Usage::

            Internal(
                URL     = str,
                PARAMS  = str,
                HEADERS = dict
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        """
        self.URL        = kwargs.get('URL')
        self.PARAMS     = kwargs.get('PARAMS')
        self.HEADERS    = kwargs.get('HEADERS')
        self.Session    = requests.Session()        
    
    def Setup(self, *args, **kwargs):
        """A Internal Requests.
        
        Basic Usage::

            Internal(
                URL     = str,
                PARAMS  = str | JSON | URLENCODE,
                HEADERS = dict
            ).Setup(
                IPPORT  = str | None, example 127.0.0.1:8080
                TYPEIP  = str | HTTP | HTTPS | SOCKS4 | SOKCS5 | None, example SOCKS5 
                METHODS = str | POST | GET | PUT, | default GET
                TIMEOUT = int | default 15 seconds
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        
        IPPORT format 127.0.0.1:8000
        
        TYPEIP SOCKS5/SOCKS4/HTTP/HTTPS  default HTTP
        
        MODE POST/PUT/GET default GET
        
        Basic Return::

            return text: str
            
        """
        
        self.TYPEIP     = kwargs.get('TYPEIP')
        self.IPPORT     = kwargs.get('IPPORT')
        self.METHODS    = 'GET' if kwargs.get('METHODS') is None else kwargs.get('METHODS')
        self.TIMEOUT    = 15 if kwargs.get('TIMEOUT') is None else kwargs.get('TIMEOUT')
        
        if self.TYPEIP is not None and self.IPPORT is not None:
            NONE = False
            if self.TYPEIP.upper() == 'HTTP' or self.TYPEIP.upper() == 'HTTPS':Proxies = dict(http=f"http://{self.IPPORT}", https=f"http://{self.IPPORT}")
            elif self.TYPEIP.upper() == 'SOCKS4':Proxies = dict(http=f"socks4://{self.IPPORT}", https=f"socks4://{self.IPPORT}")
            elif self.TYPEIP.upper() == 'SOCKS5':Proxies = dict(http=f"socks5://{self.IPPORT}", https=f"socks5://{self.IPPORT}")
            else:NONE = True
            if NONE is False:self.Session.proxies     = Proxies
            
        try:
            if self.METHODS == 'POST':Result = self.Session.post(self.URL, data=self.PARAMS, headers=self.HEADERS, timeout=self.TIMEOUT)
            elif self.METHODS == 'PUT':Result = self.Session.put(self.URL, data=self.PARAMS, headers=self.HEADERS, timeout=self.TIMEOUT)
            else:
                if self.PARAMS is None:Result = self.Session.get(self.URL, headers=self.HEADERS, timeout=self.TIMEOUT)
                else:Result = self.Session.get(self.URL, params=self.PARAMS, headers=self.HEADERS, timeout=self.TIMEOUT)
            self.Session.close()
            
            try:return dict(json.loads(Result.text))
            except:return str(Result.text)
        except ProxyError as e:raise Error(f'ProxyError')
        except ConnectTimeout as e:raise Error(f'ConnectTimeout')
        except ConnectionError as e:raise Error(f'ConnectionError')
        except ReadTimeout as e:raise Error(f'ReadTimeout')
        except JSONDecodeError:raise Error(f'JSONDecodeError')
        except TooManyRedirects as e:raise Error(f'TooManyRedirects')
        except Exception as e:raise Exception(str(e))