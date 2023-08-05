# pyTABS - ETABS .NET API python wrapper
# ErrorHandling - for pyTABS exceptions
__all__ = ['handle']

# import ETABS namespace (for future return codes)
from pytabs.etabs_config import *

class Error(Exception):
    """Error base class for non-exit exceptions"""
    pass


class EtabsError(Error):
    """General ETABS API Error Class"""
    def __init__(self, ret_value : int, message : str):
        self.ret_value : int = ret_value
        self.message : str = message


def handle(ret : int) -> None:
    """Handles ETABS API return.
    
    :param ret: return integer from ETABS API function
    :type ret: int
    :raises EtabsError: general ETABS API error if return int is != 0 
    """
    try:
        return_code = etabs.eReturnCode(ret)
    except ValueError:
        raise EtabsError(ret, 'UnknownError')
    
    if return_code != etabs.eReturnCode.NoError:
        try:
            message = str(etabs.eReturnCode(ret))
        except:
            message = 'UnknownError'
        raise EtabsError(ret, message)