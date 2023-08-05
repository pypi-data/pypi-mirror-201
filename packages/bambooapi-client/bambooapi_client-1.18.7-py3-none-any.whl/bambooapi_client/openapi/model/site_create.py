"""
    Bamboo Flexibility API

     This API provides access to flexibility assets managed by Bamboo Energy: - Create and list flexibility sites & assets - Obtain activations for specific assets - Post and get measurements for specific assets   # noqa: E501

    The version of the OpenAPI document: 1.18.7
    Contact: development@bambooenergy.tech
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from bambooapi_client.openapi.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from bambooapi_client.openapi.exceptions import ApiAttributeError


def lazy_import():
    from bambooapi_client.openapi.model.microgrid import Microgrid
    globals()['Microgrid'] = Microgrid


class SiteCreate(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('site_name',): {
            'max_length': 50,
            'min_length': 3,
        },
        ('timezone',): {
            'max_length': 50,
            'min_length': 2,
        },
        ('display_name',): {
            'max_length': 50,
            'min_length': 2,
        },
        ('location',): {
            'max_length': 50,
            'min_length': 2,
        },
        ('country',): {
            'max_length': 50,
            'min_length': 2,
        },
        ('country_code',): {
            'max_length': 6,
            'min_length': 2,
        },
        ('latitude',): {
            'inclusive_maximum': 90,
            'inclusive_minimum': -90,
        },
        ('longitude',): {
            'inclusive_maximum': 180,
            'inclusive_minimum': -180,
        },
        ('elevation',): {
            'inclusive_maximum': 10000,
            'inclusive_minimum': 0,
        },
    }

    additional_properties_type = None

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'site_name': (str,),  # noqa: E501
            'flexumer_id': (int,),  # noqa: E501
            'timezone': (str,),  # noqa: E501
            'microgrid': (Microgrid,),  # noqa: E501
            'weather_id': (int,),  # noqa: E501
            'energy_injection': (bool,),  # noqa: E501
            'display_name': (str,),  # noqa: E501
            'location': (str,),  # noqa: E501
            'country': (str,),  # noqa: E501
            'country_code': (str,),  # noqa: E501
            'latitude': (float,),  # noqa: E501
            'longitude': (float,),  # noqa: E501
            'elevation': (float,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'site_name': 'site_name',  # noqa: E501
        'flexumer_id': 'flexumer_id',  # noqa: E501
        'timezone': 'timezone',  # noqa: E501
        'microgrid': 'microgrid',  # noqa: E501
        'weather_id': 'weather_id',  # noqa: E501
        'energy_injection': 'energy_injection',  # noqa: E501
        'display_name': 'display_name',  # noqa: E501
        'location': 'location',  # noqa: E501
        'country': 'country',  # noqa: E501
        'country_code': 'country_code',  # noqa: E501
        'latitude': 'latitude',  # noqa: E501
        'longitude': 'longitude',  # noqa: E501
        'elevation': 'elevation',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, site_name, flexumer_id, timezone, microgrid, *args, **kwargs):  # noqa: E501
        """SiteCreate - a model defined in OpenAPI

        Args:
            site_name (str):
            flexumer_id (int):
            timezone (str): Name of the timezone of the site, from the IANA tz database (for example \"Europe/Madrid\"). A list of names can be found at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones.
            microgrid (Microgrid):

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            weather_id (int): [optional]  # noqa: E501
            energy_injection (bool): `true` if energy can be injected from the site to the grid, i.e., the meter measurements can be negative. `false` otherwise.. [optional] if omitted the server will use the default value of False  # noqa: E501
            display_name (str): [optional]  # noqa: E501
            location (str): [optional]  # noqa: E501
            country (str): [optional]  # noqa: E501
            country_code (str): [optional]  # noqa: E501
            latitude (float): [optional]  # noqa: E501
            longitude (float): [optional]  # noqa: E501
            elevation (float): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.site_name = site_name
        self.flexumer_id = flexumer_id
        self.timezone = timezone
        self.microgrid = microgrid
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, site_name, flexumer_id, timezone, microgrid, *args, **kwargs):  # noqa: E501
        """SiteCreate - a model defined in OpenAPI

        Args:
            site_name (str):
            flexumer_id (int):
            timezone (str): Name of the timezone of the site, from the IANA tz database (for example \"Europe/Madrid\"). A list of names can be found at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones.
            microgrid (Microgrid):

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            weather_id (int): [optional]  # noqa: E501
            energy_injection (bool): `true` if energy can be injected from the site to the grid, i.e., the meter measurements can be negative. `false` otherwise.. [optional] if omitted the server will use the default value of False  # noqa: E501
            display_name (str): [optional]  # noqa: E501
            location (str): [optional]  # noqa: E501
            country (str): [optional]  # noqa: E501
            country_code (str): [optional]  # noqa: E501
            latitude (float): [optional]  # noqa: E501
            longitude (float): [optional]  # noqa: E501
            elevation (float): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.site_name = site_name
        self.flexumer_id = flexumer_id
        self.timezone = timezone
        self.microgrid = microgrid
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
