# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import pagarmecoreapi.models.get_phone_response

class GetPhonesResponse(object):

    """Implementation of the 'GetPhonesResponse' model.

    TODO: type model description here.

    Attributes:
        home_phone (GetPhoneResponse): TODO: type description here.
        mobile_phone (GetPhoneResponse): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "home_phone":'home_phone',
        "mobile_phone":'mobile_phone'
    }

    def __init__(self,
                 home_phone=None,
                 mobile_phone=None):
        """Constructor for the GetPhonesResponse class"""

        # Initialize members of the class
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone


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
        home_phone = pagarmecoreapi.models.get_phone_response.GetPhoneResponse.from_dictionary(dictionary.get('home_phone')) if dictionary.get('home_phone') else None
        mobile_phone = pagarmecoreapi.models.get_phone_response.GetPhoneResponse.from_dictionary(dictionary.get('mobile_phone')) if dictionary.get('mobile_phone') else None

        # Return an object of this model
        return cls(home_phone,
                   mobile_phone)


