# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class UpdateSubscriptionDueDaysRequest(object):

    """Implementation of the 'UpdateSubscriptionDueDaysRequest' model.

    TODO: type model description here.

    Attributes:
        boleto_due_days (int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "boleto_due_days":'boleto_due_days'
    }

    def __init__(self,
                 boleto_due_days=None):
        """Constructor for the UpdateSubscriptionDueDaysRequest class"""

        # Initialize members of the class
        self.boleto_due_days = boleto_due_days


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
        boleto_due_days = dictionary.get('boleto_due_days')

        # Return an object of this model
        return cls(boleto_due_days)


