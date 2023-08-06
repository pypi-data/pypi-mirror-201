# secapi
This module provides an API that can be used to query metadata from sec
filings. These metadata can then be used to create a link to the actual filings
which can then be parsed.

## Technical information
The module was developed with python 2.7.18 and only uses build-in python packages as well
as the packages typing, requests, ratelimiter and [OpenDateRange](https://github.com/tlie03/OpenDateRange).

## Installation
``$ pip install secapi-tl``

## What functionalities does the API provide?
### Query filing metadata
The most important function ist the `get_filings` function
which takes one required and four optional search parameters.
The required parameter is the ticker symbol of the company 
whose filings are requested. If none of the optional arguments is 
set all filings of the given company will be returned.
The following arguments are optional.
* date_from : only filings that have been filed on this date or a current date
will be returned
* date_to : only filings that have been filed on this date or a former date
will be returned
* form_types : filters all filings based on a list of form types, so only filings
with a form type from the list will be returned
* filings_information: returns only the metadata points for each filing that
are included in the given list. This can be used to reduce the amount of data
and to get rid of irrelevant data.
A list of all possible data points can be found below

The return value will be a list of dictionaries. Each dictionary represents
one filing and holds multiple metadata points. Two of these metadata points
are the ticker symbol and the cik which are always part of the metadata.
By default, all other metadata points are contained in the dictionary, but
they can also be specifically selected via the filing_information parameter.
Below is a list of all possible metadata points:
* accessionNumber
* filingDate
* reportDate
* acceptanceDateTime
* act
* form
* fileNumber
* filmNumber
* items
* size
* isXBRL
* isInlineXBRL
* primaryDocument
* primaryDocDescription

These metadata can be used to create the links to the actual filings.
The process of finding a way to build the links from the metadata can be quite difficult, 
and requires a lot of experimentation.

### How to make requests to the sec server
The sec has restricted the access to their servers .Thereby it is not allowed
to do more than 10 requests per second. To ensure that the amount of requests stays
within the boundaries set by the sec this package provides the `Request.sec_request`
function which can be used to do requests to the sec servers. The
function has a ratelimiter which ensures that the function can only be executed
10 times per second. Due to the sleep and retry property of the function
the user does not have to worry about the number of function calls he makes.
Furthermore, all code segments in this package that make requests
to the sec servers use the same function as well. Thereby the request limit
can not be exceeded when alle requests are made with the `Request.sec_request`
function. Because of that it is necessary that a user of this API uses
this function for all requests to the sec servers otherwise problems can occur.

The `Request.sec_request` function takes in three parameters which are:
* url : the url that will be requested
* header : the header of the request which by default only contains a User-Agent
* retries : the number of retries which is 5 by default

### Utility functions
* `get_cik` can be used to get the cik that belongs to a ticker symbol
* `is_registered` can be used to proof if a company is registered at the sec

Both functions take the ticker symbol of the company as an argument
