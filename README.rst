Simple account-information retrieval API
========================================

This is a simple stand-alone server that allows an authenticated user
to retreive their userid and syncNode from the firefox sync account database.
We plan to use it internally for caching-proxying some authentication data
into AWS.

It exposes a single API endpoint:


**GET** **/whoami**

    Returns a JSON mapping of account data for the user identified in the
    *Authorization* header.  The mapping will have the following entries:

    - userid:   integer, internal numeric user identifier
    - syncNode:  string, the user's currently-assigned sync node

    Possible errors:

    - 401: the provided auth credentials were not correct
    - 503: there was an error getting the information

