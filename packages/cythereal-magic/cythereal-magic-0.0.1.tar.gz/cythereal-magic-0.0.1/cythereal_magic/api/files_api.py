# coding: utf-8

"""
    MAGIC™ API

    --- # The API for accessing Cythereal MAGIC products and services.  ---  ## Authentication  **(Head to our [/auth](../auth/swagger) api to register, login, or generate a token)**  Supported Authentication Schemes:   * HTTP Basic Authentication  * API-KEY in the `X-API-KEY` request header  * JWT token in the `Authorization:\"Bearer {token}\"` request header  ---  ## Content Negotiation    There are two ways to specify the content type of the response. In order of precedence:     * The **Accept** request header can be set with the desired mime type. The most specific version will prevail. i.e. *application/json* > *application/\\**.       *Accept:\"application/json\"*     * The **format** query parameter. (MUST be in lower case)       *?format=json*    Supported Formats:     | query parameter | Accept Header            |         |    |-----------------|--------------------------|---------|    | **json**        | application/json         | Default |    | **xml**         | application/xml          |         |    | **csv**         | text/csv                 |         |    | **txt**         | text/plain               |         |    | **explain**     | application/explain+json | Custom type that returns a description of usage of the endpoint |  --- ## Requests  Supported HTTP Methods:   * **GET**  * **POST**  * **PATCH**  * **DELETE**  * **HEAD**  * **OPTIONS**  Every request supports the following query parameters:   * **explain** - (bool) - Returns a detailed explanation of what the endpoint does, as well as potential query parameters that can be used to customize the results    * **download** - (bool) - If set to a truthy value, acts as setting the 'Content-Disposition' header to *\"attachment;\"* and will download the response as a file.   * **filename** - (str) - The filename to use for a downloaded file. Ignored if no file is being downloaded.        * **format** - (str) - Used in a similar manner to the *Accept* Header. Use this to specify which format you want the response returned in. Defaults to *application/json*. Current acceptable values are:      * **json** - (application/json)     * **xml** - (application/xml)     * **csv** - (text/csv)     * **txt** - (text/plain)     * **explain** - (application/explain+json)         * Custom type that returns a description of usage of the endpoint   * **no_links** - (bool) - If set to a truthy value, links will be disabled from the response   * **uri** - (bool) - If set to a truthy value, id lists will be returned as uris instead of id strings.  ---  ## GET Conventions ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **read_mask** - A list of values (keys) to return for the resource or each resource within the list     * Comma separated string of variables     * Leaving this field blank will return the default values.     * Setting this value equal to **`*`** will include **ALL** possible keys.     * Traversal is allowed with the **`.`** operator.     * There are three special keys that can be used with all endponts         * **`*`** - This will return all possible values available         * **`_self`** - This will include the resources uri         * **`_default`** - This will include all default values (Those given with an empty read_mask)           * This would typically be used in conjunction with other 'non-default' fields       * Ex:         * `_default,family,category,_self`    * **dynamic_mask** - A list of dynamically generated values to return about the resource or each resource within the list     * Comma separated string of variables     * Operates the same as read_mask, but each variable will incur a much greater time cost.     * *May* cause timeouts     * Leaving this field blank or empty will return no dynamic variables.    * **expand_mask** - A list of relational variables to *expand* upon and return more than just the ids     * Comma separated string of variables     * Leaving this field blank will cause all relational data to be returned as a list of ids     * Ex:         * The `children` field for a file may return a list of ids normally, but with `children` set in the           `expand_mask`, it can return a list of child File objects with greater details.  ---  ## POST Conventions  This will create a new resource.  The resource data shall be provided in the request body.  The response will be either a 200 or 201, along with a uri to the newly created resource in the `Location` header.  In the case of a long running job, or reprocess, the response will be a 202 along with a **job_id** and it's corresponding **job_uri** that can be used in the */jobs/* endpoint to see the updated status  ---  ## PATCH Conventions   * The update data shall be provided in the request body.  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **update_mask** - A list of values to update with this request.     * Comma separated string of variables     * This is required to be set for any and all **PATCH** requests to be processed.     * ONLY the specified variables in the update_mask will be updated regardless of the data in the request body.     * An empty or missing *update_mask* **WILL** result in a 400 Bad Request response  ---  ## DELETE Conventions  A successful response will return 204 No Content  ### Possible query parameters:   * **force** - Forces the deletion to go through     * This is required to be set as a truthy value for any and all **DELETE** requests to be processed.     * Not specifying this on a DELETE request (without *explain* set) **WILL** return a 400 Bad Request response   ---  ## *bulk* endpoints  **Bulk** endpoints are the ones that follow the  '*/<resource\\>/bulk/*' convention. They operate in the same fashion as the single resource endpoints ('*/<resource\\>/<resource_id\\>/*') except they can process multiple resources on a single call.  They **MUST** be a **POST** request along with the accompanying request body parameter to work:    * **ids** - A list of ids to operate on (For **GET**, **PATCH**, and **DELETE** bulk requests)   * **resources** - A list of resources to operate on (For **POST** bulk requests)  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available actions)**    * **action** - This is a string and can only be one of four values:      * **GET** - Returns a list of the resources, in the same order as provided in the request body.      * **POST** - Acts the same as a post on the pluralized resource endpoint.         * Instead of an **ids** request body parameter being provided in the request body, a **resources** list of new resources must be provided.      * **PATCH** - Acts the same as a patch on a single resource.          * Follows the same **PATCH** conventions from above*      * **DELETE** - Acts the same as a delete on a single resource.          * Follows the same **DELETE** conventions from above*    * **strict** - Causes the bulk endpoint to fail if a single provided id fails     * Boolean     * If set to True, the bulk call will ONLY operate if it is successful on ALL requested resources.     * If even a single resource is non-existent/forbidden, the call will fail and no side effects will take place.  ---  ## Pagination:  Pagination can be done in combination with sorting and filtering on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Pagination query paramters:        * **page_size** - The number of results to return (default: 50)   * **page_count** - The page used in pagination (default: 1)   * **skip_count** - A specified number of values to skip before collecting values (default: 0)  ---  ## Sorting:  Sorting can be done in combination with filtering and pagination on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Sorting query parameter:   **(Check each endpoint description, or use *explain*, for a list of available sorters)**    * **order_by** - A list of variables to sort the query on     * Comma separated string of variables     * Regex Pattern - `^(-?[\\w]+,?)*$`     * Variables are sorted in ascending order by default     * Prepend the variable with a `-` to change it to descending order     * Multiple sorters can be specified, with precedence matching the order of the parameter     * Ex:         * `-object_class,create_time`  ---  ## Filtering:  Filtering can be done in combination with pagination and sorting on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Filters query parameter:   **(Check each endpoint description, or use *explain*, for a list of available filters)**    * **filters** - A string of filters used to narrow down the query results.     * Semi-colon separated string of variables     * Regex patterns:         * Single filter:             * `^\\ *(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)\\ *`              * `NOT variable__comparator(value)`          * Multiple Filters:             * `^{SINGLE_FILTER_REGEX}(\\ +(AND|OR|;)\\ +{SINGLE_FILTER_REGEX})*$`              * `NOT variable__comparator(value) AND NOT variable__comparator(value); variable__comparator(value)`      * Logical operator order of precedence:         * **AND**         * **OR**         * **;** **(Semi-colon separation denotes conjunction)**         * Example order of precedence:             * **exp1;exp2 AND exp3 OR exp4** is equivalent to **(exp1) AND ((exp2 AND exp3) OR (exp4))**      * Available Comparators:         * **eq** - Equal         * **ne** - Not Equal         * **lt** - Less than         * **lte** - Less than or equal         * **gt** - Greater than         * **gte** - Greater than or equal         * **in** - In (for list values)         * **nin** - Not In (for list values)         * **regex** - Regular Expression Match         * **iregex** - Case Insensitive Regular Expression Match      * The format for **in** and **nin** which operate on arrays is:         * **[]** - The list of values must be enclosed within brackets.         * **,** - The value separtion token is a comma.         * **<variable\\>__<comp\\>([<value1\\>,<value2\\>])**      * Examples:         * `create_time__gte(2022-01-01T13:11:02);object_class__regex(binary.*)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01) AND NOT match_count__gt(10)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01)`  ---  ## Responses  All responses **WILL** be of type `APIResponse` and contain the following fields:  * `success` | Boolean value indicating if the operation succeeded.  * `status` | Status code. Corresponds to the HTTP status code.   * `message` | A human readable message providing more details about the operation.  * `links` | A dictionary of `name`: `uri` links providing navigation and state-based actions on resources  * `errors` | Array of error objects. An error object contains the following properties:      * `reason` | Unique identifier for this error. Ex: \"FileNotFoundError\".      * `message`| Human readable error message.      * `parameter`| The parameter (if any) that caused the issue.  Successful operations **MUST** return a `SuccessResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal True  * `resource` | Properties containing the response object.     * (In the case of a single entity being returned)  **OR**  * `resources` | A list of response objects.     * (In the case of a list of entities being returned)  Failed Operations **MUST** return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal False.  Common Failed Operations that you may hit on any of the endpoint operations:  * 400 - Bad Request - The request is malformed  * 401 - Unauthorized - All endpoints require authorization  * 403 - Forbidden - The endpoint (with the given parameters) is not available to you  * 404 - Not Found - The endpoint doesn't exist, or the resource being searched for doesn't exist  ---  ## Example Inputs  Here are some example inputs that can be used for testing the service:  * `binary_id`: **ff9790d7902fea4c910b182f6e0b00221a40d616**  * `proc_rva`: **0x1000**  * `search_query`: **ransomware**  ---   # noqa: E501

    OpenAPI spec version: 2.0.0 (v2)
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cythereal_magic.api_client import ApiClient


class FilesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_file(self, binary_id, **kwargs):  # noqa: E501
        """Adds a publicly accessible file to your account  # noqa: E501

           Adds a publicly accessible file to your account           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_file(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_file_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.add_file_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def add_file_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Adds a publicly accessible file to your account  # noqa: E501

           Adds a publicly accessible file to your account           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_file_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `add_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def add_file_tag(self, binary_id, tag_id, **kwargs):  # noqa: E501
        """Associate an existing tag with a file  # noqa: E501

           Associate an existing tag with a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_file_tag(binary_id, tag_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object tag_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_file_tag_with_http_info(binary_id, tag_id, **kwargs)  # noqa: E501
        else:
            (data) = self.add_file_tag_with_http_info(binary_id, tag_id, **kwargs)  # noqa: E501
            return data

    def add_file_tag_with_http_info(self, binary_id, tag_id, **kwargs):  # noqa: E501
        """Associate an existing tag with a file  # noqa: E501

           Associate an existing tag with a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_file_tag_with_http_info(binary_id, tag_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object tag_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'tag_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_file_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `add_file_tag`")  # noqa: E501
        # verify the required parameter 'tag_id' is set
        if self.api_client.client_side_validation and ('tag_id' not in params or
                                                       params['tag_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `tag_id` when calling `add_file_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501
        if 'tag_id' in params:
            path_params['tag_id'] = params['tag_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/tags/{tag_id}/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def add_payload(self, binary_id, payload_id, **kwargs):  # noqa: E501
        """Manually add a payload connection to a file  # noqa: E501

           Manually add a payload connection to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_payload(binary_id, payload_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object payload_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_payload_with_http_info(binary_id, payload_id, **kwargs)  # noqa: E501
        else:
            (data) = self.add_payload_with_http_info(binary_id, payload_id, **kwargs)  # noqa: E501
            return data

    def add_payload_with_http_info(self, binary_id, payload_id, **kwargs):  # noqa: E501
        """Manually add a payload connection to a file  # noqa: E501

           Manually add a payload connection to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_payload_with_http_info(binary_id, payload_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object payload_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'payload_id', 'explain', 'format', 'download', 'filename', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_payload" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `add_payload`")  # noqa: E501
        # verify the required parameter 'payload_id' is set
        if self.api_client.client_side_validation and ('payload_id' not in params or
                                                       params['payload_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `payload_id` when calling `add_payload`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501
        if 'payload_id' in params:
            path_params['payload_id'] = params['payload_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/payload/{payload_id}/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def bulk_file_operation(self, **kwargs):  # noqa: E501
        """Allows for actions to be carried out on bulk sets of files  # noqa: E501

           Allows for actions to be carried out on bulk sets of files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_file_operation(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param object dynamic_mask: Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param object force: MUST be true for any `DELETE` method to take place
        :param object order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param object page_count:
        :param object page_size:
        :param object read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :param object skip_count:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.bulk_file_operation_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.bulk_file_operation_with_http_info(**kwargs)  # noqa: E501
            return data

    def bulk_file_operation_with_http_info(self, **kwargs):  # noqa: E501
        """Allows for actions to be carried out on bulk sets of files  # noqa: E501

           Allows for actions to be carried out on bulk sets of files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_file_operation_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param object dynamic_mask: Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param object force: MUST be true for any `DELETE` method to take place
        :param object order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param object page_count:
        :param object page_size:
        :param object read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :param object skip_count:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['explain', 'format', 'download', 'filename', 'action', 'dynamic_mask', 'expand_mask', 'filters', 'force', 'order_by', 'page_count', 'page_size', 'read_mask', 'skip_count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method bulk_file_operation" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'action' in params:
            query_params.append(('action', params['action']))  # noqa: E501
        if 'dynamic_mask' in params:
            query_params.append(('dynamic_mask', params['dynamic_mask']))  # noqa: E501
        if 'expand_mask' in params:
            query_params.append(('expand_mask', params['expand_mask']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/bulk/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_file_category(self, binary_id, **kwargs):  # noqa: E501
        """Creates a new custom category label for a file  # noqa: E501

           Creates a new custom category label for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_category(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_file_category_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_file_category_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def create_file_category_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Creates a new custom category label for a file  # noqa: E501

           Creates a new custom category label for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_category_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_file_category" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `create_file_category`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/categories/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_file_family(self, binary_id, **kwargs):  # noqa: E501
        """Creates a new custom family label for a file  # noqa: E501

           Creates a new custom family label for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_family(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_file_family_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_file_family_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def create_file_family_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Creates a new custom family label for a file  # noqa: E501

           Creates a new custom family label for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_family_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_file_family" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `create_file_family`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/families/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_file_job(self, binary_id, job, **kwargs):  # noqa: E501
        """Send a file for reprocessing  # noqa: E501

           Send a file for reprocessing           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_job(binary_id, job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object job: The job to reprocess for this file (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :param object reprocess: If true, the file will be set for reprocessing
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_file_job_with_http_info(binary_id, job, **kwargs)  # noqa: E501
        else:
            (data) = self.create_file_job_with_http_info(binary_id, job, **kwargs)  # noqa: E501
            return data

    def create_file_job_with_http_info(self, binary_id, job, **kwargs):  # noqa: E501
        """Send a file for reprocessing  # noqa: E501

           Send a file for reprocessing           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_job_with_http_info(binary_id, job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object job: The job to reprocess for this file (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :param object reprocess: If true, the file will be set for reprocessing
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'job', 'explain', 'format', 'download', 'filename', 'force', 'reprocess']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_file_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `create_file_job`")  # noqa: E501
        # verify the required parameter 'job' is set
        if self.api_client.client_side_validation and ('job' not in params or
                                                       params['job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `job` when calling `create_file_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501
        if 'job' in params:
            query_params.append(('job', params['job']))  # noqa: E501
        if 'reprocess' in params:
            query_params.append(('reprocess', params['reprocess']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/jobs/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_file_note(self, binary_id, **kwargs):  # noqa: E501
        """Attaches a note to a file  # noqa: E501

           Attaches a note to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_note(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_file_note_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_file_note_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def create_file_note_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Attaches a note to a file  # noqa: E501

           Attaches a note to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_file_note_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_file_note" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `create_file_note`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/notes/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_file_note(self, binary_id, note_id, **kwargs):  # noqa: E501
        """Deletes a specified user note attached to a file  # noqa: E501

           Deletes a specified user note attached to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_file_note(binary_id, note_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object note_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_file_note_with_http_info(binary_id, note_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_file_note_with_http_info(binary_id, note_id, **kwargs)  # noqa: E501
            return data

    def delete_file_note_with_http_info(self, binary_id, note_id, **kwargs):  # noqa: E501
        """Deletes a specified user note attached to a file  # noqa: E501

           Deletes a specified user note attached to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_file_note_with_http_info(binary_id, note_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object note_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'note_id', 'explain', 'format', 'download', 'filename', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_file_note" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `delete_file_note`")  # noqa: E501
        # verify the required parameter 'note_id' is set
        if self.api_client.client_side_validation and ('note_id' not in params or
                                                       params['note_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `note_id` when calling `delete_file_note`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501
        if 'note_id' in params:
            path_params['note_id'] = params['note_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/notes/{note_id}/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_payload_relationship(self, binary_id, **kwargs):  # noqa: E501
        """Manually remove a payload connection from a file  # noqa: E501

           Manually remove a payload connection from a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_payload_relationship(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :param object force2: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_payload_relationship_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_payload_relationship_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def delete_payload_relationship_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Manually remove a payload connection from a file  # noqa: E501

           Manually remove a payload connection from a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_payload_relationship_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :param object force2: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'force', 'force2']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_payload_relationship" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `delete_payload_relationship`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501
        if 'force2' in params:
            query_params.append(('force', params['force2']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/payload/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def download_file(self, binary_id, **kwargs):  # noqa: E501
        """Download file  # noqa: E501

           Download file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.download_file(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object zipped: If true, the returned download will be in an encrypted zip file (password=infected)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.download_file_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.download_file_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def download_file_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Download file  # noqa: E501

           Download file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.download_file_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object zipped: If true, the returned download will be in an encrypted zip file (password=infected)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'zipped']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method download_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `download_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'zipped' in params:
            query_params.append(('zipped', params['zipped']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/download/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves information for a single file  # noqa: E501

           Retrieves information for a single file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object dynamic_mask: Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def get_file_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves information for a single file  # noqa: E501

           Retrieves information for a single file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object dynamic_mask: Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'dynamic_mask', 'expand_mask', 'read_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `get_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'dynamic_mask' in params:
            query_params.append(('dynamic_mask', params['dynamic_mask']))  # noqa: E501
        if 'expand_mask' in params:
            query_params.append(('expand_mask', params['expand_mask']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file_campaign(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's campaign information  # noqa: E501

           Retrieves a file's campaign information           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_campaign(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_campaign_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_campaign_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def get_file_campaign_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's campaign information  # noqa: E501

           Retrieves a file's campaign information           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_campaign_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `get_file_campaign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/campaign/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file_note(self, binary_id, note_id, **kwargs):  # noqa: E501
        """Retrieves a single note attached to a file  # noqa: E501

           Retrieves a single note attached to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_note(binary_id, note_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object note_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_note_with_http_info(binary_id, note_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_note_with_http_info(binary_id, note_id, **kwargs)  # noqa: E501
            return data

    def get_file_note_with_http_info(self, binary_id, note_id, **kwargs):  # noqa: E501
        """Retrieves a single note attached to a file  # noqa: E501

           Retrieves a single note attached to a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_note_with_http_info(binary_id, note_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object note_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'note_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file_note" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `get_file_note`")  # noqa: E501
        # verify the required parameter 'note_id' is set
        if self.api_client.client_side_validation and ('note_id' not in params or
                                                       params['note_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `note_id` when calling `get_file_note`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501
        if 'note_id' in params:
            path_params['note_id'] = params['note_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/notes/{note_id}/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file_reputation(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves the reputation status of the file  # noqa: E501

           Retrieves the reputation status of the file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_reputation(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_reputation_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_reputation_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def get_file_reputation_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves the reputation status of the file  # noqa: E501

           Retrieves the reputation status of the file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_reputation_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file_reputation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `get_file_reputation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/reputation/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file_yara(self, binary_id, **kwargs):  # noqa: E501
        """Returns a yara rule for the given file  # noqa: E501

           Returns a yara rule for the given file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_yara(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_yara_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_yara_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def get_file_yara_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Returns a yara rule for the given file  # noqa: E501

           Returns a yara rule for the given file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_yara_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file_yara" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `get_file_yara`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/yara/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_categories(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's category labels  # noqa: E501

           Retrieves a file's category labels           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_categories(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_categories_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_categories_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_categories_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's category labels  # noqa: E501

           Retrieves a file's category labels           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_categories_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_categories" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_categories`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/categories/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_children(self, binary_id, **kwargs):  # noqa: E501
        """Lists all files that were extracted as children  # noqa: E501

           Lists all files that were extracted as children           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_children(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_children_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_children_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_children_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Lists all files that were extracted as children  # noqa: E501

           Lists all files that were extracted as children           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_children_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_children" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_children`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/children/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_families(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's family labels  # noqa: E501

           Retrieves a file's family labels           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_families(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_families_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_families_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_families_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's family labels  # noqa: E501

           Retrieves a file's family labels           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_families_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_families" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_families`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/families/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_genomics(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's genomics  # noqa: E501

           Retrieves a file's genomics           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_genomics(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_genomics_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_genomics_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_genomics_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's genomics  # noqa: E501

           Retrieves a file's genomics           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_genomics_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_genomics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_genomics`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/genomics/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_indicators(self, binary_id, **kwargs):  # noqa: E501
        """Lists the Indicators of Compromise associated with a file  # noqa: E501

           Lists the Indicators of Compromise associated with a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_indicators(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_indicators_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_indicators_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_indicators_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Lists the Indicators of Compromise associated with a file  # noqa: E501

           Lists the Indicators of Compromise associated with a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_indicators_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_indicators" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_indicators`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/indicators/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_labels(self, binary_id, **kwargs):  # noqa: E501
        """Gets labels for a file  # noqa: E501

           Gets labels for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_labels(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_labels_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_labels_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_labels_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Gets labels for a file  # noqa: E501

           Gets labels for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_labels_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_labels" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_labels`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/labels/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_matches(self, binary_id, **kwargs):  # noqa: E501
        """Gets matches for a file  # noqa: E501

           Gets matches for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_matches(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object max_threshold: Only similarity matches at value equal or below max_threshold will be considered
        :param object min_threshold: Only similarity matches at value equal or above min_threshold will be considered
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_matches_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_matches_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_matches_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Gets matches for a file  # noqa: E501

           Gets matches for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_matches_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object max_threshold: Only similarity matches at value equal or below max_threshold will be considered
        :param object min_threshold: Only similarity matches at value equal or above min_threshold will be considered
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'expand_mask', 'max_threshold', 'min_threshold']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_matches" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_matches`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'expand_mask' in params:
            query_params.append(('expand_mask', params['expand_mask']))  # noqa: E501
        if 'max_threshold' in params:
            query_params.append(('max_threshold', params['max_threshold']))  # noqa: E501
        if 'min_threshold' in params:
            query_params.append(('min_threshold', params['min_threshold']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/matches/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_notes(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves all user generated notes for file  # noqa: E501

           Retrieves all user generated notes for file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_notes(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_notes_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_notes_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_notes_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves all user generated notes for file  # noqa: E501

           Retrieves all user generated notes for file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_notes_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_notes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_notes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/notes/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_parents(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's parent files  # noqa: E501

           Retrieves a file's parent files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_parents(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_parents_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_parents_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_parents_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves a file's parent files  # noqa: E501

           Retrieves a file's parent files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_parents_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_parents" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_parents`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/parents/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_procedure_genomics(self, binary_id, rva, **kwargs):  # noqa: E501
        """Retrieves a procedure's genomics  # noqa: E501

           Retrieves a procedure's genomics           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_procedure_genomics(binary_id, rva, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object rva: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_procedure_genomics_with_http_info(binary_id, rva, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_procedure_genomics_with_http_info(binary_id, rva, **kwargs)  # noqa: E501
            return data

    def list_file_procedure_genomics_with_http_info(self, binary_id, rva, **kwargs):  # noqa: E501
        """Retrieves a procedure's genomics  # noqa: E501

           Retrieves a procedure's genomics           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_procedure_genomics_with_http_info(binary_id, rva, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object rva: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'rva', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_procedure_genomics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_procedure_genomics`")  # noqa: E501
        # verify the required parameter 'rva' is set
        if self.api_client.client_side_validation and ('rva' not in params or
                                                       params['rva'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `rva` when calling `list_file_procedure_genomics`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501
        if 'rva' in params:
            path_params['rva'] = params['rva']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/genomics/{rva}/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_procedures(self, binary_id, **kwargs):  # noqa: E501
        """Lists all procedures and their information for the given file  # noqa: E501

           Lists all procedures and their information for the given file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_procedures(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_procedures_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_procedures_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_procedures_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Lists all procedures and their information for the given file  # noqa: E501

           Lists all procedures and their information for the given file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_procedures_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_procedures" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_procedures`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/procedures/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_similarities(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves similar file matches for the specified file  # noqa: E501

           Retrieves similar file matches for the specified file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_similarities(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object max_threshold: Only similarity matches at value equal or below max_threshold will be considered
        :param object min_threshold: Only similarity matches at value equal or above min_threshold will be considered
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_similarities_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_similarities_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_similarities_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Retrieves similar file matches for the specified file  # noqa: E501

           Retrieves similar file matches for the specified file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_similarities_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object max_threshold: Only similarity matches at value equal or below max_threshold will be considered
        :param object min_threshold: Only similarity matches at value equal or above min_threshold will be considered
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'max_threshold', 'min_threshold']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_similarities" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_similarities`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'max_threshold' in params:
            query_params.append(('max_threshold', params['max_threshold']))  # noqa: E501
        if 'min_threshold' in params:
            query_params.append(('min_threshold', params['min_threshold']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/similarities/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_strings(self, binary_id, **kwargs):  # noqa: E501
        """Gets strings for a file  # noqa: E501

           Gets strings for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_strings(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_strings_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_strings_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_strings_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Gets strings for a file  # noqa: E501

           Gets strings for a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_strings_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_strings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_strings`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/strings/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_file_tags(self, binary_id, **kwargs):  # noqa: E501
        """List all user tags associated with a file  # noqa: E501

           List all user tags associated with a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_tags(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_file_tags_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_file_tags_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def list_file_tags_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """List all user tags associated with a file  # noqa: E501

           List all user tags associated with a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_file_tags_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_file_tags" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `list_file_tags`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/tags/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_files(self, **kwargs):  # noqa: E501
        """List user files based on the parameters specified  # noqa: E501

           List user files based on the parameters specified           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_files(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object dynamic_mask: Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param object order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param object page_count:
        :param object page_size:
        :param object read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :param object skip_count:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_files_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_files_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_files_with_http_info(self, **kwargs):  # noqa: E501
        """List user files based on the parameters specified  # noqa: E501

           List user files based on the parameters specified           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_files_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object dynamic_mask: Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :param object filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param object order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param object page_count:
        :param object page_size:
        :param object read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :param object skip_count:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['explain', 'format', 'download', 'filename', 'dynamic_mask', 'expand_mask', 'filters', 'order_by', 'page_count', 'page_size', 'read_mask', 'skip_count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_files" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'dynamic_mask' in params:
            query_params.append(('dynamic_mask', params['dynamic_mask']))  # noqa: E501
        if 'expand_mask' in params:
            query_params.append(('expand_mask', params['expand_mask']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_all_file_owners(self, binary_id, **kwargs):  # noqa: E501
        """Removes all owners from file  # noqa: E501

           Removes all owners from file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_all_file_owners(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.remove_all_file_owners_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_all_file_owners_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def remove_all_file_owners_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Removes all owners from file  # noqa: E501

           Removes all owners from file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_all_file_owners_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_all_file_owners" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `remove_all_file_owners`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/owners/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_file(self, binary_id, **kwargs):  # noqa: E501
        """Removes a user's ownership from a single file  # noqa: E501

           Removes a user's ownership from a single file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_file(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.remove_file_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_file_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def remove_file_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Removes a user's ownership from a single file  # noqa: E501

           Removes a user's ownership from a single file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_file_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `remove_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_file_tag(self, binary_id, tag_id, **kwargs):  # noqa: E501
        """Remove an existing tag from a file  # noqa: E501

           Remove an existing tag from a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_file_tag(binary_id, tag_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object tag_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.remove_file_tag_with_http_info(binary_id, tag_id, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_file_tag_with_http_info(binary_id, tag_id, **kwargs)  # noqa: E501
            return data

    def remove_file_tag_with_http_info(self, binary_id, tag_id, **kwargs):  # noqa: E501
        """Remove an existing tag from a file  # noqa: E501

           Remove an existing tag from a file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_file_tag_with_http_info(binary_id, tag_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object tag_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object force: MUST be true for any `DELETE` method to take place
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'tag_id', 'explain', 'format', 'download', 'filename', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_file_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `remove_file_tag`")  # noqa: E501
        # verify the required parameter 'tag_id' is set
        if self.api_client.client_side_validation and ('tag_id' not in params or
                                                       params['tag_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `tag_id` when calling `remove_file_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501
        if 'tag_id' in params:
            path_params['tag_id'] = params['tag_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/tags/{tag_id}/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def search_for_file(self, **kwargs):  # noqa: E501
        """Search for files based on given parameters  # noqa: E501

           Search for files based on given parameters           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_for_file(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.search_for_file_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.search_for_file_with_http_info(**kwargs)  # noqa: E501
            return data

    def search_for_file_with_http_info(self, **kwargs):  # noqa: E501
        """Search for files based on given parameters  # noqa: E501

           Search for files based on given parameters           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_for_file_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['explain', 'format', 'download', 'filename']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_for_file" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/search/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_file(self, binary_id, **kwargs):  # noqa: E501
        """Updates a single file  # noqa: E501

           Updates a single file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `{FIELD_MASK_PATTERN}`
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_file_with_http_info(binary_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_file_with_http_info(binary_id, **kwargs)  # noqa: E501
            return data

    def update_file_with_http_info(self, binary_id, **kwargs):  # noqa: E501
        """Updates a single file  # noqa: E501

           Updates a single file           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_with_http_info(binary_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object binary_id: (required)
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `{FIELD_MASK_PATTERN}`
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['binary_id', 'explain', 'format', 'download', 'filename', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'binary_id' is set
        if self.api_client.client_side_validation and ('binary_id' not in params or
                                                       params['binary_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `binary_id` when calling `update_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'binary_id' in params:
            path_params['binary_id'] = params['binary_id']  # noqa: E501

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/{binary_id}/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def upload_file(self, **kwargs):  # noqa: E501
        """Upload new files for processing  # noqa: E501

           Multiple files may be uploaded at once up to 100MB.    Tags and notes can also be attached at the time of upload.           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_file(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object extract: If true, all extracted files from an archive will be top level and the archive thrown away
        :param object recursive: If true, all archives found in the upload will be stripped and thrown
        :param object retain_wrapper: If true with extract, then the archive will not be thrown away
        :param object skip_unpack: If true, Cythereal's default unpacker stage will be skipped
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.upload_file_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.upload_file_with_http_info(**kwargs)  # noqa: E501
            return data

    def upload_file_with_http_info(self, **kwargs):  # noqa: E501
        """Upload new files for processing  # noqa: E501

           Multiple files may be uploaded at once up to 100MB.    Tags and notes can also be attached at the time of upload.           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_file_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object explain:  Shows the explain for this endpoint 
        :param object format:  Format of the response from this endpoint 
        :param object download:  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\") 
        :param object filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param object extract: If true, all extracted files from an archive will be top level and the archive thrown away
        :param object recursive: If true, all archives found in the upload will be stripped and thrown
        :param object retain_wrapper: If true with extract, then the archive will not be thrown away
        :param object skip_unpack: If true, Cythereal's default unpacker stage will be skipped
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['explain', 'format', 'download', 'filename', 'extract', 'recursive', 'retain_wrapper', 'skip_unpack']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_file" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'extract' in params:
            query_params.append(('extract', params['extract']))  # noqa: E501
        if 'recursive' in params:
            query_params.append(('recursive', params['recursive']))  # noqa: E501
        if 'retain_wrapper' in params:
            query_params.append(('retain_wrapper', params['retain_wrapper']))  # noqa: E501
        if 'skip_unpack' in params:
            query_params.append(('skip_unpack', params['skip_unpack']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/files/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
