# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

from pagarmecoreapi.api_helper import APIHelper
import pagarmecoreapi.models.get_bank_account_response

class GetTransferResponse(object):

    """Implementation of the 'GetTransferResponse' model.

    Transfer response

    Attributes:
        id (string): Id
        amount (int): Transfer amount
        status (string): Transfer status
        created_at (datetime): Transfer creation date
        updated_at (datetime): Transfer last update date
        bank_account (GetBankAccountResponse): TODO: type description here.
        metadata (dict<object, string>): Metadata

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "id":'id',
        "amount":'amount',
        "status":'status',
        "created_at":'created_at',
        "updated_at":'updated_at',
        "bank_account":'bank_account',
        "metadata":'metadata'
    }

    def __init__(self,
                 id=None,
                 amount=None,
                 status=None,
                 created_at=None,
                 updated_at=None,
                 bank_account=None,
                 metadata=None):
        """Constructor for the GetTransferResponse class"""

        # Initialize members of the class
        self.id = id
        self.amount = amount
        self.status = status
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.updated_at = APIHelper.RFC3339DateTime(updated_at) if updated_at else None
        self.bank_account = bank_account
        self.metadata = metadata


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
        id = dictionary.get('id')
        amount = dictionary.get('amount')
        status = dictionary.get('status')
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("created_at")).datetime if dictionary.get("created_at") else None
        updated_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("updated_at")).datetime if dictionary.get("updated_at") else None
        bank_account = pagarmecoreapi.models.get_bank_account_response.GetBankAccountResponse.from_dictionary(dictionary.get('bank_account')) if dictionary.get('bank_account') else None
        metadata = dictionary.get('metadata')

        # Return an object of this model
        return cls(id,
                   amount,
                   status,
                   created_at,
                   updated_at,
                   bank_account,
                   metadata)


