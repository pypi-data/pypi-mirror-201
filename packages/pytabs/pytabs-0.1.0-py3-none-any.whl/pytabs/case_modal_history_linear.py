# pyTABS - ETABS .NET API python wrapper
# CaseModalHistoryLinear - cCaseModalHistoryLinear
__all__ = ['CaseModalHistoryLinear']

# import ETABS namespace and pyTABS error handler
from pytabs.etabs_config import *
from pytabs.error_handle import *

# import custom enumerations


# import typing


class CaseModalHistoryLinear:
    """CaseModalHistoryLinear interface"""
    def __init__(self, sap_model : etabs.cSapModel) -> None:
        # link of SapModel interface
        self.sap_model = sap_model
        # create interface for modal history linear cases
        self.modal_history_linear = etabs.cCaseModalHistoryLinear(sap_model.LoadCases.ModHistLinear)
        
        # relate custom enumerations