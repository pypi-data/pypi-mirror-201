# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import pagarmecoreapi.models.get_transaction_report_file_response
import pagarmecoreapi.models.paging_response

class ListTransactionsFilesResponse(object):

    """Implementation of the 'ListTransactionsFilesResponse' model.

    Response object for listing of transactions files

    Attributes:
        data (list of GetTransactionReportFileResponse): TODO: type
            description here.
        paging (PagingResponse): Object used for returning lists of objects
            with pagination

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "data":'data',
        "paging":'paging'
    }

    def __init__(self,
                 data=None,
                 paging=None):
        """Constructor for the ListTransactionsFilesResponse class"""

        # Initialize members of the class
        self.data = data
        self.paging = paging


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        data = None
        if dictionary.get('data') != None:
            data = list()
            for structure in dictionary.get('data'):
                data.append(pagarmecoreapi.models.get_transaction_report_file_response.GetTransactionReportFileResponse.from_dictionary(structure))
        paging = pagarmecoreapi.models.paging_response.PagingResponse.from_dictionary(dictionary.get('paging')) if dictionary.get('paging') else None

        # Return an object of this model
        return cls(data,
                   paging)


