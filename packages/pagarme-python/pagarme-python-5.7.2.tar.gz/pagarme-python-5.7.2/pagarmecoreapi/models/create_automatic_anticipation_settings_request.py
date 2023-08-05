# -*- coding: utf-8 -*-

"""
    pagarmecoreapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class CreateAutomaticAnticipationSettingsRequest(object):

    """Implementation of the 'CreateAutomaticAnticipationSettingsRequest' model.

    TODO: type model description here.

    Attributes:
        enabled (bool): TODO: type description here.
        mtype (string): TODO: type description here.
        volume_percentage (int): TODO: type description here.
        delay (int): TODO: type description here.
        days (list of int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "enabled":'enabled',
        "mtype":'type',
        "volume_percentage":'volume_percentage',
        "delay":'delay',
        "days":'days'
    }

    def __init__(self,
                 enabled=None,
                 mtype=None,
                 volume_percentage=None,
                 delay=None,
                 days=None):
        """Constructor for the CreateAutomaticAnticipationSettingsRequest class"""

        # Initialize members of the class
        self.enabled = enabled
        self.mtype = mtype
        self.volume_percentage = volume_percentage
        self.delay = delay
        self.days = days


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
        enabled = dictionary.get('enabled')
        mtype = dictionary.get('type')
        volume_percentage = dictionary.get('volume_percentage')
        delay = dictionary.get('delay')
        days = dictionary.get('days')

        # Return an object of this model
        return cls(enabled,
                   mtype,
                   volume_percentage,
                   delay,
                   days)


