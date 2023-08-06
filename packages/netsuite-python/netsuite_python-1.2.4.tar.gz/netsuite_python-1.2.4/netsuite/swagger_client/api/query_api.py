# coding: utf-8

"""
    NetSuite REST API
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
import json

from netsuite.swagger_client.api_client import ApiClient
import netsuite.swagger_client.models


class QueryApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def execute_query(self, query, **kwargs):
        all_params = ['prefer', 'response_type', 'limit', 'offset']  # noqa: E
        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method customer_get" % key
                )
            params[key] = val
        del params['kwargs']

        header_params = {}
        query_params = {}
        if 'prefer' in params:
            header_params['Prefer'] = params['prefer']  # noqa: E501
        else:
            header_params['Prefer'] = 'transient'

        if 'limit' in params:
            print(params['limit'])
            if params['limit'] is not None:
                print('set')
                query_params['limit'] = params['limit']
            else:
                query_params['limit'] = 500

        if 'offset' in params:
            if params['offset'] is not None:
                query_params['offset'] = params['offset']
            else:
                query_params['offset'] = 0

        if 'response_type' in params:
            if params['response_type'] is not None:
                if hasattr(netsuite.swagger_client.models, params['response_type']):
                    response_type = params['response_type']
                else:
                    response_type = None
                    raise TypeError(f"{params['response_type']} is not a valid response type")
            return_http_only_data = True
            _preload_content = True
            # print(params['response_type'])
        else:
            response_type = None
            return_http_only_data = True
            _preload_content = False

        # Authentication setting
        auth_settings = ['oAuth2ClientCredentials']
        response = self.api_client.call_api('',
                                            'POST',
                                            header_params=header_params,
                                            query_params=query_params,
                                            auth_settings=auth_settings,
                                            body={"q": f"{query}"},
                                            response_type=response_type,
                                            _return_http_data_only=return_http_only_data,
                                            _preload_content=_preload_content)

        if response_type is not None:
            if hasattr(response, 'items'):
                return response.items
            else:
                return response
        if isinstance(response, tuple):
            return response
        if hasattr(response, 'data'):
            if isinstance(response.data, bytes):
                response = json.loads(response.data.decode('UTF-8'))
                if 'items' in response:
                    if type(response.get("items")) is list:
                        return response.get("items")
                    else:
                        items = [response.get("items")]
                        return items
                else:
                    return None
        else:
            return response


    # ns_query_api.get_model_query('Customer', 'CustomerCollection', 'customer', "WHERE customer.lastmodifieddate >= TO_DATE('19/02/2023 18:00:22', 'DD/MM/YYYY HH24:MI:SS')", settings.NETSUITE_FIELD_MAP)
    # def get_model_query(self, query_model_name: str = None, return_type: str = None,  table_name: str = None, filter_clause: Optional[str] = None, return_field_dict: Optional[dict] = None, ):
    #     if hasattr(netsuite.swagger_client.models, query_model_name):
    #         klass = getattr(netsuite.swagger_client.models, query_model_name)
    #         class_types = klass.swagger_types
    #         class_attributes = klass.attribute_map
    #     else:
    #         raise TypeError(f"{model_name} does not exist in netsuite.swagger_client.models")
    #
    #
    #     return_fields = []
    #     if return_field_dict is not None:
    #         for item in return_field_dict:
    #             value = return_field_dict.get(item)
    #             if value in class_types:
    #                 field_name = class_attributes.get(value)
    #                 if class_types.get(value) == 'NsResource':
    #                     return_fields.append(f"BUILTIN.DF({field_name}) AS {value}")
    #                 else:
    #                     return_fields.append(f"{field_name} AS {field_name}")
    #
    #     if len(return_fields) > 0:
    #         fields = ','.join(return_fields)
    #     else:
    #         fields = '*'
    #
    #     query = f"SELECT {fields} FROM {table_name}"
    #     # print(query)
    #
    #     if filter_clause is not None:
    #         query = f"{query} {filter_clause}"
    #     print(query)
    #     return self.execute_query(query=query, response_type=query_model_name)
