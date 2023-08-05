# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

from pagarmecoreapi.api_helper import APIHelper
import pagarmecoreapi.models.pix_additional_information

class CreateCheckoutPixPaymentRequest(object):

    """Implementation of the 'CreateCheckoutPixPaymentRequest' model.

    Checkout pix payment request

    Attributes:
        expires_at (datetime): Expires at
        expires_in (int): Expires in
        additional_information (list of PixAdditionalInformation): Additional
            information

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "expires_at":'expires_at',
        "expires_in":'expires_in',
        "additional_information":'additional_information'
    }

    def __init__(self,
                 expires_at=None,
                 expires_in=None,
                 additional_information=None):
        """Constructor for the CreateCheckoutPixPaymentRequest class"""

        # Initialize members of the class
        self.expires_at = APIHelper.RFC3339DateTime(expires_at) if expires_at else None
        self.expires_in = expires_in
        self.additional_information = additional_information


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
        expires_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("expires_at")).datetime if dictionary.get("expires_at") else None
        expires_in = dictionary.get('expires_in')
        additional_information = None
        if dictionary.get('additional_information') != None:
            additional_information = list()
            for structure in dictionary.get('additional_information'):
                additional_information.append(pagarmecoreapi.models.pix_additional_information.PixAdditionalInformation.from_dictionary(structure))

        # Return an object of this model
        return cls(expires_at,
                   expires_in,
                   additional_information)


