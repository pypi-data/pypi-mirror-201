# pyTABS - ETABS .NET API python wrapper
# CaseModalRitz - cCaseModalRitz
__all__ = ['CaseModalRitz']

# import ETABS namespace and pyTABS error handler
from pytabs.etabs_config import *
from pytabs.error_handle import *

# import custom enumerations


# import typing


class CaseModalRitz:
    """CaseModalRitz interface"""
    def __init__(self, sap_model : etabs.cSapModel) -> None:
        # link of SapModel interface
        self.sap_model = sap_model
        # create interface for modal Ritz cases
        self.modal_ritz = etabs.cCaseModalRitz(sap_model.LoadCases.ModalRitz)
        
        # relate custom enumerations