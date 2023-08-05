# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import pagarmecoreapi.models.update_pricing_scheme_request

class UpdateSubscriptionItemRequest(object):

    """Implementation of the 'UpdateSubscriptionItemRequest' model.

    Request for updating a subscription item

    Attributes:
        description (string): Description
        status (string): Status
        pricing_scheme (UpdatePricingSchemeRequest): Request for updating a
            pricing scheme
        name (string): Item name
        cycles (int): Number of cycles that the item will be charged
        quantity (int): Quantity
        minimum_price (int): Minimum price

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "description":'description',
        "status":'status',
        "pricing_scheme":'pricing_scheme',
        "name":'name',
        "cycles":'cycles',
        "quantity":'quantity',
        "minimum_price":'minimum_price'
    }

    def __init__(self,
                 description=None,
                 status=None,
                 pricing_scheme=None,
                 name=None,
                 cycles=None,
                 quantity=None,
                 minimum_price=None):
        """Constructor for the UpdateSubscriptionItemRequest class"""

        # Initialize members of the class
        self.description = description
        self.status = status
        self.pricing_scheme = pricing_scheme
        self.name = name
        self.cycles = cycles
        self.quantity = quantity
        self.minimum_price = minimum_price


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
        description = dictionary.get('description')
        status = dictionary.get('status')
        pricing_scheme = pagarmecoreapi.models.update_pricing_scheme_request.UpdatePricingSchemeRequest.from_dictionary(dictionary.get('pricing_scheme')) if dictionary.get('pricing_scheme') else None
        name = dictionary.get('name')
        cycles = dictionary.get('cycles')
        quantity = dictionary.get('quantity')
        minimum_price = dictionary.get('minimum_price')

        # Return an object of this model
        return cls(description,
                   status,
                   pricing_scheme,
                   name,
                   cycles,
                   quantity,
                   minimum_price)


