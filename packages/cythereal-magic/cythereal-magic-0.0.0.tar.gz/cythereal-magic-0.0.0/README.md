# cythereal-magic
--- # The API for accessing Cythereal MAGIC products and services.  ---  ## Authentication  **(Head to our [/auth](../auth/swagger) api to register, login, or generate a token)**  Supported Authentication Schemes:   * HTTP Basic Authentication  * API-KEY in the `X-API-KEY` request header  * JWT token in the `Authorization:\"Bearer {token}\"` request header  ---  ## Content Negotiation    There are two ways to specify the content type of the response. In order of precedence:     * The **Accept** request header can be set with the desired mime type. The most specific version will prevail. i.e. *application/json* > *application/\\**.       *Accept:\"application/json\"*     * The **format** query parameter. (MUST be in lower case)       *?format=json*    Supported Formats:     | query parameter | Accept Header            |         |    |-----------------|--------------------------|---------|    | **json**        | application/json         | Default |    | **xml**         | application/xml          |         |    | **csv**         | text/csv                 |         |    | **txt**         | text/plain               |         |    | **explain**     | application/explain+json | Custom type that returns a description of usage of the endpoint |  --- ## Requests  Supported HTTP Methods:   * **GET**  * **POST**  * **PATCH**  * **DELETE**  * **HEAD**  * **OPTIONS**  Every request supports the following query parameters:   * **explain** - (bool) - Returns a detailed explanation of what the endpoint does, as well as potential query parameters that can be used to customize the results    * **download** - (bool) - If set to a truthy value, acts as setting the 'Content-Disposition' header to *\"attachment;\"* and will download the response as a file.   * **filename** - (str) - The filename to use for a downloaded file. Ignored if no file is being downloaded.        * **format** - (str) - Used in a similar manner to the *Accept* Header. Use this to specify which format you want the response returned in. Defaults to *application/json*. Current acceptable values are:      * **json** - (application/json)     * **xml** - (application/xml)     * **csv** - (text/csv)     * **txt** - (text/plain)     * **explain** - (application/explain+json)         * Custom type that returns a description of usage of the endpoint   * **no_links** - (bool) - If set to a truthy value, links will be disabled from the response   * **uri** - (bool) - If set to a truthy value, id lists will be returned as uris instead of id strings.  ---  ## GET Conventions ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **read_mask** - A list of values (keys) to return for the resource or each resource within the list     * Comma separated string of variables     * Leaving this field blank will return the default values.     * Setting this value equal to **`*`** will include **ALL** possible keys.     * Traversal is allowed with the **`.`** operator.     * There are three special keys that can be used with all endponts         * **`*`** - This will return all possible values available         * **`_self`** - This will include the resources uri         * **`_default`** - This will include all default values (Those given with an empty read_mask)           * This would typically be used in conjunction with other 'non-default' fields       * Ex:         * `_default,family,category,_self`    * **dynamic_mask** - A list of dynamically generated values to return about the resource or each resource within the list     * Comma separated string of variables     * Operates the same as read_mask, but each variable will incur a much greater time cost.     * *May* cause timeouts     * Leaving this field blank or empty will return no dynamic variables.    * **expand_mask** - A list of relational variables to *expand* upon and return more than just the ids     * Comma separated string of variables     * Leaving this field blank will cause all relational data to be returned as a list of ids     * Ex:         * The `children` field for a file may return a list of ids normally, but with `children` set in the           `expand_mask`, it can return a list of child File objects with greater details.  ---  ## POST Conventions  This will create a new resource.  The resource data shall be provided in the request body.  The response will be either a 200 or 201, along with a uri to the newly created resource in the `Location` header.  In the case of a long running job, or reprocess, the response will be a 202 along with a **job_id** and it's corresponding **job_uri** that can be used in the */jobs/* endpoint to see the updated status  ---  ## PATCH Conventions   * The update data shall be provided in the request body.  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **update_mask** - A list of values to update with this request.     * Comma separated string of variables     * This is required to be set for any and all **PATCH** requests to be processed.     * ONLY the specified variables in the update_mask will be updated regardless of the data in the request body.     * An empty or missing *update_mask* **WILL** result in a 400 Bad Request response  ---  ## DELETE Conventions  A successful response will return 204 No Content  ### Possible query parameters:   * **force** - Forces the deletion to go through     * This is required to be set as a truthy value for any and all **DELETE** requests to be processed.     * Not specifying this on a DELETE request (without *explain* set) **WILL** return a 400 Bad Request response   ---  ## *bulk* endpoints  **Bulk** endpoints are the ones that follow the  '*/<resource\\>/bulk/*' convention. They operate in the same fashion as the single resource endpoints ('*/<resource\\>/<resource_id\\>/*') except they can process multiple resources on a single call.  They **MUST** be a **POST** request along with the accompanying request body parameter to work:    * **ids** - A list of ids to operate on (For **GET**, **PATCH**, and **DELETE** bulk requests)   * **resources** - A list of resources to operate on (For **POST** bulk requests)  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available actions)**    * **action** - This is a string and can only be one of four values:      * **GET** - Returns a list of the resources, in the same order as provided in the request body.      * **POST** - Acts the same as a post on the pluralized resource endpoint.         * Instead of an **ids** request body parameter being provided in the request body, a **resources** list of new resources must be provided.      * **PATCH** - Acts the same as a patch on a single resource.          * Follows the same **PATCH** conventions from above*      * **DELETE** - Acts the same as a delete on a single resource.          * Follows the same **DELETE** conventions from above*    * **strict** - Causes the bulk endpoint to fail if a single provided id fails     * Boolean     * If set to True, the bulk call will ONLY operate if it is successful on ALL requested resources.     * If even a single resource is non-existent/forbidden, the call will fail and no side effects will take place.  ---  ## Pagination:  Pagination can be done in combination with sorting and filtering on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Pagination query paramters:        * **page_size** - The number of results to return (default: 50)   * **page_count** - The page used in pagination (default: 1)   * **skip_count** - A specified number of values to skip before collecting values (default: 0)  ---  ## Sorting:  Sorting can be done in combination with filtering and pagination on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Sorting query parameter:   **(Check each endpoint description, or use *explain*, for a list of available sorters)**    * **order_by** - A list of variables to sort the query on     * Comma separated string of variables     * Regex Pattern - `^(-?[\\w]+,?)*$`     * Variables are sorted in ascending order by default     * Prepend the variable with a `-` to change it to descending order     * Multiple sorters can be specified, with precedence matching the order of the parameter     * Ex:         * `-object_class,create_time`  ---  ## Filtering:  Filtering can be done in combination with pagination and sorting on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Filters query parameter:   **(Check each endpoint description, or use *explain*, for a list of available filters)**    * **filters** - A string of filters used to narrow down the query results.     * Semi-colon separated string of variables     * Regex patterns:         * Single filter:             * `^\\ *(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)\\ *`              * `NOT variable__comparator(value)`          * Multiple Filters:             * `^{SINGLE_FILTER_REGEX}(\\ +(AND|OR|;)\\ +{SINGLE_FILTER_REGEX})*$`              * `NOT variable__comparator(value) AND NOT variable__comparator(value); variable__comparator(value)`      * Logical operator order of precedence:         * **AND**         * **OR**         * **;** **(Semi-colon separation denotes conjunction)**         * Example order of precedence:             * **exp1;exp2 AND exp3 OR exp4** is equivalent to **(exp1) AND ((exp2 AND exp3) OR (exp4))**      * Available Comparators:         * **eq** - Equal         * **ne** - Not Equal         * **lt** - Less than         * **lte** - Less than or equal         * **gt** - Greater than         * **gte** - Greater than or equal         * **in** - In (for list values)         * **nin** - Not In (for list values)         * **regex** - Regular Expression Match         * **iregex** - Case Insensitive Regular Expression Match      * The format for **in** and **nin** which operate on arrays is:         * **[]** - The list of values must be enclosed within brackets.         * **,** - The value separtion token is a comma.         * **<variable\\>__<comp\\>([<value1\\>,<value2\\>])**      * Examples:         * `create_time__gte(2022-01-01T13:11:02);object_class__regex(binary.*)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01) AND NOT match_count__gt(10)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01)`  ---  ## Responses  All responses **WILL** be of type `APIResponse` and contain the following fields:  * `success` | Boolean value indicating if the operation succeeded.  * `status` | Status code. Corresponds to the HTTP status code.   * `message` | A human readable message providing more details about the operation.  * `links` | A dictionary of `name`: `uri` links providing navigation and state-based actions on resources  * `errors` | Array of error objects. An error object contains the following properties:      * `reason` | Unique identifier for this error. Ex: \"FileNotFoundError\".      * `message`| Human readable error message.      * `parameter`| The parameter (if any) that caused the issue.  Successful operations **MUST** return a `SuccessResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal True  * `resource` | Properties containing the response object.     * (In the case of a single entity being returned)  **OR**  * `resources` | A list of response objects.     * (In the case of a list of entities being returned)  Failed Operations **MUST** return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal False.  Common Failed Operations that you may hit on any of the endpoint operations:  * 400 - Bad Request - The request is malformed  * 401 - Unauthorized - All endpoints require authorization  * 403 - Forbidden - The endpoint (with the given parameters) is not available to you  * 404 - Not Found - The endpoint doesn't exist, or the resource being searched for doesn't exist  ---  ## Example Inputs  Here are some example inputs that can be used for testing the service:  * `binary_id`: **ff9790d7902fea4c910b182f6e0b00221a40d616**  * `proc_rva`: **0x1000**  * `search_query`: **ransomware**  --- 

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 2.0.0 (v2)
- Package version: 0.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen
For more information, please visit [https://cythereal.com](https://cythereal.com)

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import cythereal_magic 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import cythereal_magic
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import cythereal_magic
from cythereal_magic.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = NULL # object | 
explain = NULL # object |  Shows the explain for this endpoint  (optional)
format = NULL # object |  Format of the response from this endpoint  (optional)
download = NULL # object |  Determines whether to download the response. (Content-Disposition:\"attachment\" vs \"inline\")  (optional)
filename = NULL # object | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)

try:
    # Adds a publicly accessible file to your account
    api_instance.add_file(binary_id, explain=explain, format=format, download=download, filename=filename)
except ApiException as e:
    print("Exception when calling FilesApi->add_file: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FilesApi* | [**add_file**](docs/FilesApi.md#add_file) | **POST** /files/{binary_id}/ | Adds a publicly accessible file to your account
*FilesApi* | [**add_file_tag**](docs/FilesApi.md#add_file_tag) | **POST** /files/{binary_id}/tags/{tag_id}/ | Associate an existing tag with a file
*FilesApi* | [**add_payload**](docs/FilesApi.md#add_payload) | **POST** /files/{binary_id}/payload/{payload_id}/ | Manually add a payload connection to a file
*FilesApi* | [**bulk_file_operation**](docs/FilesApi.md#bulk_file_operation) | **POST** /files/bulk/ | Allows for actions to be carried out on bulk sets of files
*FilesApi* | [**create_file_category**](docs/FilesApi.md#create_file_category) | **POST** /files/{binary_id}/categories/ | Creates a new custom category label for a file
*FilesApi* | [**create_file_family**](docs/FilesApi.md#create_file_family) | **POST** /files/{binary_id}/families/ | Creates a new custom family label for a file
*FilesApi* | [**create_file_job**](docs/FilesApi.md#create_file_job) | **POST** /files/{binary_id}/jobs/ | Send a file for reprocessing
*FilesApi* | [**create_file_note**](docs/FilesApi.md#create_file_note) | **POST** /files/{binary_id}/notes/ | Attaches a note to a file
*FilesApi* | [**delete_file_note**](docs/FilesApi.md#delete_file_note) | **DELETE** /files/{binary_id}/notes/{note_id}/ | Deletes a specified user note attached to a file
*FilesApi* | [**delete_payload_relationship**](docs/FilesApi.md#delete_payload_relationship) | **DELETE** /files/{binary_id}/payload/ | Manually remove a payload connection from a file
*FilesApi* | [**download_file**](docs/FilesApi.md#download_file) | **GET** /files/{binary_id}/download/ | Download file
*FilesApi* | [**get_file**](docs/FilesApi.md#get_file) | **GET** /files/{binary_id}/ | Retrieves information for a single file
*FilesApi* | [**get_file_campaign**](docs/FilesApi.md#get_file_campaign) | **GET** /files/{binary_id}/campaign/ | Retrieves a file&#39;s campaign information
*FilesApi* | [**get_file_note**](docs/FilesApi.md#get_file_note) | **GET** /files/{binary_id}/notes/{note_id}/ | Retrieves a single note attached to a file
*FilesApi* | [**get_file_reputation**](docs/FilesApi.md#get_file_reputation) | **GET** /files/{binary_id}/reputation/ | Retrieves the reputation status of the file
*FilesApi* | [**get_file_yara**](docs/FilesApi.md#get_file_yara) | **GET** /files/{binary_id}/yara/ | Returns a yara rule for the given file
*FilesApi* | [**list_file_categories**](docs/FilesApi.md#list_file_categories) | **GET** /files/{binary_id}/categories/ | Retrieves a file&#39;s category labels
*FilesApi* | [**list_file_children**](docs/FilesApi.md#list_file_children) | **GET** /files/{binary_id}/children/ | Lists all files that were extracted as children
*FilesApi* | [**list_file_families**](docs/FilesApi.md#list_file_families) | **GET** /files/{binary_id}/families/ | Retrieves a file&#39;s family labels
*FilesApi* | [**list_file_genomics**](docs/FilesApi.md#list_file_genomics) | **GET** /files/{binary_id}/genomics/ | Retrieves a file&#39;s genomics
*FilesApi* | [**list_file_indicators**](docs/FilesApi.md#list_file_indicators) | **GET** /files/{binary_id}/indicators/ | Lists the Indicators of Compromise associated with a file
*FilesApi* | [**list_file_labels**](docs/FilesApi.md#list_file_labels) | **GET** /files/{binary_id}/labels/ | Gets labels for a file
*FilesApi* | [**list_file_matches**](docs/FilesApi.md#list_file_matches) | **GET** /files/{binary_id}/matches/ | Gets matches for a file
*FilesApi* | [**list_file_notes**](docs/FilesApi.md#list_file_notes) | **GET** /files/{binary_id}/notes/ | Retrieves all user generated notes for file
*FilesApi* | [**list_file_parents**](docs/FilesApi.md#list_file_parents) | **GET** /files/{binary_id}/parents/ | Retrieves a file&#39;s parent files
*FilesApi* | [**list_file_procedure_genomics**](docs/FilesApi.md#list_file_procedure_genomics) | **GET** /files/{binary_id}/genomics/{rva}/ | Retrieves a procedure&#39;s genomics
*FilesApi* | [**list_file_procedures**](docs/FilesApi.md#list_file_procedures) | **GET** /files/{binary_id}/procedures/ | Lists all procedures and their information for the given file
*FilesApi* | [**list_file_similarities**](docs/FilesApi.md#list_file_similarities) | **GET** /files/{binary_id}/similarities/ | Retrieves similar file matches for the specified file
*FilesApi* | [**list_file_strings**](docs/FilesApi.md#list_file_strings) | **GET** /files/{binary_id}/strings/ | Gets strings for a file
*FilesApi* | [**list_file_tags**](docs/FilesApi.md#list_file_tags) | **GET** /files/{binary_id}/tags/ | List all user tags associated with a file
*FilesApi* | [**list_files**](docs/FilesApi.md#list_files) | **GET** /files/ | List user files based on the parameters specified
*FilesApi* | [**remove_all_file_owners**](docs/FilesApi.md#remove_all_file_owners) | **DELETE** /files/{binary_id}/owners/ | Removes all owners from file
*FilesApi* | [**remove_file**](docs/FilesApi.md#remove_file) | **DELETE** /files/{binary_id}/ | Removes a user&#39;s ownership from a single file
*FilesApi* | [**remove_file_tag**](docs/FilesApi.md#remove_file_tag) | **DELETE** /files/{binary_id}/tags/{tag_id}/ | Remove an existing tag from a file
*FilesApi* | [**search_for_file**](docs/FilesApi.md#search_for_file) | **GET** /files/search/ | Search for files based on given parameters
*FilesApi* | [**update_file**](docs/FilesApi.md#update_file) | **PATCH** /files/{binary_id}/ | Updates a single file
*FilesApi* | [**upload_file**](docs/FilesApi.md#upload_file) | **POST** /files/ | Upload new files for processing
*GenomicsApi* | [**compare_files**](docs/GenomicsApi.md#compare_files) | **GET** /genomics/compare/ | Takes in a list of files and sends back comparison results (slow)
*GroupsApi* | [**add_member**](docs/GroupsApi.md#add_member) | **POST** /groups/{id}/members/{member_id}/ | Adds the &#x60;member_id&#x60; user to the &#x60;id&#x60; group
*GroupsApi* | [**add_new_member**](docs/GroupsApi.md#add_new_member) | **POST** /groups/{id}/members/ | Adds the given user to this group
*GroupsApi* | [**bulk_group_operation**](docs/GroupsApi.md#bulk_group_operation) | **POST** /groups/bulk/ | Bulk operations on Group resources
*GroupsApi* | [**create_group**](docs/GroupsApi.md#create_group) | **POST** /groups/ | Create a new group
*GroupsApi* | [**delete_group**](docs/GroupsApi.md#delete_group) | **DELETE** /groups/{id}/ | Deletes a group
*GroupsApi* | [**get_group**](docs/GroupsApi.md#get_group) | **GET** /groups/{id}/ | Retrieves detailed information on a single group
*GroupsApi* | [**get_member**](docs/GroupsApi.md#get_member) | **GET** /groups/{id}/members/{member_id}/ | Returns the user with &#x60;member_id&#x60; with their &#x60;id&#x60; group settings
*GroupsApi* | [**group_login**](docs/GroupsApi.md#group_login) | **GET** /groups/{id}/login/ | Returns a jwt Token for this group
*GroupsApi* | [**group_logout**](docs/GroupsApi.md#group_logout) | **GET** /groups/logout/ | Converts the group jwt back into a single user jwt
*GroupsApi* | [**list_groups**](docs/GroupsApi.md#list_groups) | **GET** /groups/ | List all accessible groups
*GroupsApi* | [**list_members**](docs/GroupsApi.md#list_members) | **GET** /groups/{id}/members/ | List all members of a group
*GroupsApi* | [**remove_member**](docs/GroupsApi.md#remove_member) | **DELETE** /groups/{id}/members/{member_id}/ | Removes the &#x60;member_id&#x60; user from the &#x60;id&#x60; group
*GroupsApi* | [**update_group**](docs/GroupsApi.md#update_group) | **PATCH** /groups/{id}/ | Updates a group
*GroupsApi* | [**update_member**](docs/GroupsApi.md#update_member) | **PATCH** /groups/{id}/members/{member_id}/ | Updates the &#x60;member_id&#x60; user in the &#x60;id&#x60; group
*IndicatorsApi* | [**create_ioc**](docs/IndicatorsApi.md#create_ioc) | **POST** /indicators/ | Manually creates a new indicator of compromise
*IndicatorsApi* | [**list_ioc_files**](docs/IndicatorsApi.md#list_ioc_files) | **GET** /indicators/files/ | Lists all indicators associated with a file
*IndicatorsApi* | [**list_iocs**](docs/IndicatorsApi.md#list_iocs) | **GET** /indicators/ | Lists all indicators associated with a user account
*IndicatorsApi* | [**upload_ioc_file**](docs/IndicatorsApi.md#upload_ioc_file) | **POST** /indicators/files/ | Upload a text or csv file for IoC Extraction
*ProceduresApi* | [**bulk_procedure_operation**](docs/ProceduresApi.md#bulk_procedure_operation) | **POST** /procedures/bulk/ | Get procedures in bulk
*ProceduresApi* | [**get_procedure**](docs/ProceduresApi.md#get_procedure) | **GET** /procedures/{proc_hash}/ | Get a single procedure
*ProceduresApi* | [**list_procedure_files**](docs/ProceduresApi.md#list_procedure_files) | **GET** /procedures/{proc_hash}/files/ | Retrieves a procedure&#39;s files
*ProceduresApi* | [**list_procedure_similarities**](docs/ProceduresApi.md#list_procedure_similarities) | **GET** /procedures/{proc_hash}/similarities/ | Lists a procedure&#39;s similarities
*ProceduresApi* | [**list_procedures**](docs/ProceduresApi.md#list_procedures) | **GET** /procedures/ | Get all procedures
*ReportsApi* | [**get_archive_report**](docs/ReportsApi.md#get_archive_report) | **GET** /reports/{binary_id}/archive/ | Retrieves the report info of a container like file
*ReportsApi* | [**get_report_features**](docs/ReportsApi.md#get_report_features) | **GET** /reports/{binary_id}/features/ | Retrieves the genomic features of a file
*SearchApi* | [**count_search_results**](docs/SearchApi.md#count_search_results) | **GET** /search/count/ | Returns total count of results via search
*SearchApi* | [**search_files**](docs/SearchApi.md#search_files) | **GET** /search/ | Returns files found via search
*SupportApi* | [**report_bug**](docs/SupportApi.md#report_bug) | **POST** /support/bug/ | Allows users to report a bug within the system
*TagsApi* | [**bulk_tag_operation**](docs/TagsApi.md#bulk_tag_operation) | **POST** /tags/bulk/ | Lists information on a bulk selection of tags
*TagsApi* | [**create_tag**](docs/TagsApi.md#create_tag) | **POST** /tags/ | Create a new Project for tagging files
*TagsApi* | [**delete_tag**](docs/TagsApi.md#delete_tag) | **DELETE** /tags/{id}/ | Deletes a tag
*TagsApi* | [**delete_tags**](docs/TagsApi.md#delete_tags) | **DELETE** /tags/ | Delete selected tags
*TagsApi* | [**get_tag**](docs/TagsApi.md#get_tag) | **GET** /tags/{id}/ | Retrieves detailed information on a single tag
*TagsApi* | [**list_tagged_files**](docs/TagsApi.md#list_tagged_files) | **GET** /tags/{id}/files/ | Lists all files associated with this tag
*TagsApi* | [**list_tags**](docs/TagsApi.md#list_tags) | **GET** /tags/ | List all tags
*TagsApi* | [**remove_tags**](docs/TagsApi.md#remove_tags) | **DELETE** /tags/{id}/files/ | Removes all user tags from a file
*TagsApi* | [**update_tag**](docs/TagsApi.md#update_tag) | **PATCH** /tags/{id}/ | Updates a tag
*TagsApi* | [**update_tags**](docs/TagsApi.md#update_tags) | **PATCH** /tags/ | Updates all tags in your collection
*UsersApi* | [**deactivate_account**](docs/UsersApi.md#deactivate_account) | **DELETE** /users/me/ | Deactivate your account
*UsersApi* | [**get_account**](docs/UsersApi.md#get_account) | **GET** /users/me/ | Retrieve your account information
*UsersApi* | [**get_my_group**](docs/UsersApi.md#get_my_group) | **GET** /users/me/groups/{id}/ | Retrieve info for a group
*UsersApi* | [**leave_my_group**](docs/UsersApi.md#leave_my_group) | **DELETE** /users/me/groups/{id}/ | Leave group
*UsersApi* | [**leave_my_groups**](docs/UsersApi.md#leave_my_groups) | **DELETE** /users/me/groups/ | Leave all groups
*UsersApi* | [**list_my_groups**](docs/UsersApi.md#list_my_groups) | **GET** /users/me/groups/ | Lists your groups
*UsersApi* | [**update_account**](docs/UsersApi.md#update_account) | **PATCH** /users/me/ | Update your account information
*YaraApi* | [**create_yara**](docs/YaraApi.md#create_yara) | **POST** /yara/ | Create Yara Rule based on specific file hashes
*YaraApi* | [**yara_procedure_matches**](docs/YaraApi.md#yara_procedure_matches) | **GET** /yara/{binary_id}/matches/ | Get similar binaries based off of potential yara procedure matches


## Documentation For Models



## Documentation For Authorization

 All endpoints do not require authorization.


## Author

support@cythereal.com

