#### Introduction

**Starting with sustainalytics 0.2.0, the package is compatible with API v2 only. If a v1-compatible version is needed, please install version 0.1.2 via this command:**

```python
pip install sustainalytics==0.1.2
```


This python package provides access to Sustainalytics API (Application Programming Interface) service which provides developers with 24x7 programmatic access to Sustainalytics data. The API has been developed based on market standards with a primary focus on secure connectivity and ease of use. It allows users to retrieve and integrate Sustainalytics data into their own internal systems and custom or third-party applications

This document is meant to provide developers with python sample code for the Sustainalytics API service.
Technical documentation can also be found on the dedicated [website](https://api.sustainalytics.com/swagger/ui/index/index.html) for the API.

![Figure1](https://github.com/Kienka/sustainalytics/raw/master/sustainalytics/Figure1.PNG)

#### Installation
<p>Install the package via pip with code below:


```python
pip install sustainalytics
```

To Upgrade:


```python
pip install --upgrade sustainalytics
```

#### Connection
A clientid and a secret key must be provided by the Sustainalytics Team in order to access the API.
See connection via python:


```python
from sustainalytics.api import API

#Access
client_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client_secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

con = API(client_id=client_id, client_secretkey=client_secret_key)

#returns Bearer
print(con.access_headers)
```

### Endpoints

#### DataService

The DataService enables the user to call the research data associated with the companies in the universe of access. Within this service there are two endpoints, as described below.

![](https://github.com/Kienka/sustainalytics/raw/master/sustainalytics/dataservice.png)

The code below shows you how to extract data from these endpoints

#### GetData 

Retrieves data from the DataService endpoint. 'identifiers' and 'productId' are **mandatory** endpoints


##### __The 'identifiers' and 'productId' arguments can be combined with only one of the other arguments:__

__identifiers__ : A list of security or entity identifiers separated by comma. You can obtain list of EntityIds from the con.get_universe_entityIds(keep_duplicates=True)

__packageIds__ : A list of package ids separated by comma. You can obtain list of PackageIds from the con.get_packageIds()

__fieldClusterIds__ : A list of field cluster ids separated by comma. You can obtain list of FieldClusterIds from the con.get_fieldClusterIds()

__fieldIds__ : A list of field ids separated by comma. You can obtain list of FieldIds from the con.get_fieldIds()

![](https://github.com/Kienka/sustainalytics/raw/master/sustainalytics/ds_params.png)


```python
#### GetData
data = con.get_data(identifiers=[], productId=[], packageIds=[], fieldClusterIds=[], fieldIds=[])
#returns data for the specified identifier(s). 'identifiers' and 'productId' are required for the function to work.
print(data)
```

#### Product Structure & Definitions

Each product is built from __data packages__ and each data package is built from __field clusters__. The __datafields__ are the smallest components of the product structure. 

The Product Structure service provides an overview  of the data fields available in the  Sustainalytics API and the unique __FieldIds__ linked to each of these data fields. Within this service there are three endpoints, as described below.

![Figure2](https://github.com/Kienka/sustainalytics/raw/master/sustainalytics/fids.png)

The code below shows you how to extract data from these endpoints


```python
#### FieldDefinitions
field_definitions = con.get_fieldDefinitions(dtype='dataframe') #by default dtype='json'
print(field_definitions)

#### FieldMappings
field_mappings = con.get_fieldMappings(dtype='dataframe') #by default dtype='json'
print(field_mappings)

#### FieldMappingDefinitions
field_mapping_definition = con.get_fieldMappingDefinitions(dtype='dataframe') #by default dtype='json'
print(field_mapping_definition)

#### Extra FieldDefinition (non-Swagger)
fullFieldDef = con.get_fullFieldDefinitions(dtype='dataframe')
print(fullFieldDef)
```

#### Reports

The ReportService endpoint allows users to retrieve a list of all available PDF report types by ReportId, ReportType, and ReportName for companies belonging to the universe of access. 

__(Please note this Endpoint is not part of the standard API product.)__

![Figure3](https://github.com/Kienka/sustainalytics/raw/master/sustainalytics/reports.png)

The code below shows you how to extract data from these endpoints


```python
####ReportService
report_info = con.get_pdfReportInfo(productId=x,dtype='dataframe')  #by default dtype='json'
where x be any integer value of existing product ids (for example, 10 for Corporate Data)
#returns all the available report fieldIDs (reportids)
print(report_info)

####ReportService(identifier)(reportid)
report_identifier_reportid = con.get_pdfReportUrl(identifier=x, reportId=y)
#returns the url to given pdf report for specified companies (if available)
print(report_identifier_reportid)
```

The function supports only 1 identifier and reportID per call.

####  Universe of Access

The UniverseOfAccess endpoint allows users to determine the list of EntityIds contained in the universe of access (all permissioned securities lists).

![Figure4](https://github.com/Kienka/sustainalytics/raw/master/sustainalytics/univ.png)


```python
####UniverseofAccess
universe = con.get_universe_access(dtype='dataframe') #by default dtype='json'
#returns all universe constituents
print(universe)
```


```python
#### Extra non-Swagger functions
fieldClusterIds = con.get_fieldClusterIds()
#returns all clusterIds
print(fieldClusterIds)

fieldIds = con.get_fieldIds()
#returns all fieldIDs
print(fieldIds)

fieldsInfo = con.get_fieldsInfo()
#returns fields info
print(fieldsInfo)

productIds = con.get_productIds()
#returns product IDs
print(productIds)

packageIds = con.get_packageIds()
#returns package IDs
print(packageIds)

packageInfo = con.get_packageInfo()
#returns package info
print(packageInfo)
```
