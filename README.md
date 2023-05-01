## Portfolio Assignment: API Spec

URL: https://josephri-fp.ue.r.appspot.com/

## Change log

      - Spring CS 493: Cloud Application Development
      - Last Update: June 8 , Oregon State University
- Change log
- Data Model
- Create a Boat
- Create a Load
- View Boat/Boats
- View a Specific Boat
- View Loads
- View a Specific Load
- Edit a Boat (PUT)
- Edit a Boat (PATCH)
- Edit a Load (PUT)
- Edit a Load (PATCH)
- Add a Load to a Boat
- Remove a Load from the Boat
- Delete a Boat
- Delete a Load
   
  - Initial version. June 08 , Page Change Date


## Data Model

- User
    Property Type Required? Valid Values

```
JWT JSON Web Token Yes JWT generated by
Google Oauth
```
```
Unique ID String Yes Sub of JWT
```
- Boat
    Property Type Required Valid Values

```
ID String Yes Automatically created
by DataStore.
```
```
Name String Yes Name of the boat.
E.g. “VIII Rings”
```
```
Type String Yes Can be any string,
should be descriptive.
E.g. “yacht”
```
```
Length Integer Yes Any integer is
acceptable. Allowance
of integers as string
but not
recommended.
```
```
Loads String No ID of Load Model.
```
```
Owner Unique ID of User
Model (String)
```
```
Yes Must be a User Model
that has already been
created.
```

- Load
    Property Type Required Valid Values

```
ID String Yes Automatically
created by
DataStore.
```
```
Weight Integer Yes Any integer is
acceptable.
Allowance of integers
as string but not
recommended.
```
```
Content String Yes Content of the load.
```
```
Delivery Date String Yes String in the format
of “mm/dd/yyyy”.
```
```
Boats String No ID of boat model.
```
- The Boat and Load are the two non-user entities. The boat has the ability to have zero or more
    loads on it, but the load can only be on one boat at a given time. To put a load on another boat
    it will require unlinking the load from the boat and placing it on another boat.
- The unique identifier for the users in my data model is the sub of the json web token. If a
    request needs to supply a user identifier the JWT must be supplied. While the JWT is generated
    the Unique ID is also generated. The User is only related to the Boat in which the boat is owned
    by the User, this is accomplished by having the boat have an owner property.


## Create a Boat

Allows you to create a new boat.

```
POST /boats/
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

Request Body
Required

Request Body Format
JSON

Request JSON Attributes
**Name Type Description Required?**
name String The name of the boat. Yes
type String The type of the boat. E.g., Sailboat, Catamaran, etc. Yes
length Integer Length of the boat in feet. Yes

Request Body Example
{
"name": "Sea Witch",
"type": "Catamaran",
"length": 28
}

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 201 Created
Failure 401 Unauthorized Error If the request has an invalid or missing JWT this status
code is returned.

```
Failure 405 Method Not
Allowed
```
```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

- Datastore will automatically generate an ID and store it with the entity being created. This value
    needs to be sent in the response body as shown in the example.


_Success_
Status: 201 Created

{
"id": "abc123",
"name": "Sea Witch",
"type": "Catamaran",
"length": 28,
“loads”: “NULL”,
"owner": "Owner Sub JWT",
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error

```
{
"Error": "Unauthorized Error”
}
Status: 405 Method Not Allowed
```
```
{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable
```
```
{
“Error”: “Not Acceptable”
}
```

## Create a Load

Allows you to create a new load.

```
POST /loads/
```
Request

Request Parameters

Request Body
Required

Request Body Format
JSON

Request JSON Attributes
**Name Type Description Required?**
weight Integer Weight of the load Yes
content String Contents in load Yes
delivery_date Integer Date of delivery Yes

Request Body Example
{
"weight": 28,
"content": "Eggs",
"delivery_date": “11/19/2020”
}

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 201 Created
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

- Datastore will automatically generate an ID and store it with the entity being created. This value
    needs to be sent in the response body as shown in the example.

_Success_
Status: 201 Created


### {

"id": "abc123",
"weight": 88,
"content": "Eggs",
"delivery_date": “11/21/2021,
“boat”: “NULL”,
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error

```
{
"Error": "Unauthorized Error”
}
Status: 405 Method Not Allowed
```
```
{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable
```
```
{
“Error”: “Not Acceptable”
}
```

## View Boat/Boats

Allows you to view your boats

```
GET /boats/
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

Request Body
None

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 401 Unauthorized Error If the request has an invalid or missing JWT this status
code is returned.

```
Failure 405 Method Not
Allowed
```
```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK

```
{
“boats”: [
"id": "abc123",
"name": "Sea Witch",
"type": "Catamaran",
"length": 28,
"owner": "Owner Sub JWT"
“loads”: “NULL”,
“self”: Entity Link
]
}
```

_Failure_
Status: 401 Unauthorized Error

```
{
"Error": "Unauthorized Error”
}
Status: 405 Method Not Allowed
```
```
{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable
```
```
{
“Error”: “Not Acceptable”
}
```

## View a Specific Boat

View a specific boat that you own.

```
GET /boats/<Boat_id>
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

```
Name Type Description Required?
Boat_id String ID of the Boat Yes
```
Request Body
None

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 401 Unauthorized Error If the request has an invalid or missing JWT this status
code is returned.

```
Failure 403 Forbidden Valid JWT but the boat does not belong to the user.
Failure 404 Not Found Boat was not found
Failure 405 Method Not
Allowed
```
```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK
{
"id": "abc123",
"name": "Sea Witch",
"type": "Catamaran",
"length": 28,
“loads”: “NULL”,
"owner": "Owner Sub JWT",
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error

```
{
"Error": "Unauthorized Error”
```

### }

Status: 403 Forbidden

{
"Error": "Forbidden”
}
Status: 404 Not Found

{
"Error": "Not Found”
}
Status: 405 Method Not Allowed

{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## View Loads

Allows you to view all loads

```
GET /loads/
```
Request

Request Parameters

Request Body
None

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK

```
{
“loads”: [
"id": "abc123",
"weight": 88,
"content": "Eggs",
"delivery_date": “11/21/2021,
“boat”: “NULL”,
“self”: Entity URL
}
```
_Failure_
Status: 405 Method Not Allowed

```
{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable
```
```
{
```

“Error”: “Not Acceptable”
}


## View a Specific Load.....................................................................................................................................

View a specific load

```
GET /loads/<load_id>
```
Request

Request Parameters
**Name Type Description Required?**
load_id String ID of the load Yes

Request Body
None

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 404 Not Found Load was not found
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK
{
"id": "abc123",
"weight": 88,
"content": "Eggs",
"delivery_date": “11/21/2021,
“boat”: “NULL”,
“self”: Entity URL
}
_Failure_
Status: 404 Not Found

```
{
"Error": "Not Found”
}
Status: 405 Method Not Allowed
```
```
{
“Error”: “Method Not Allowed”
}
```

Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Edit a Boat (PUT)

Edit all the attributes of a boat.

```
PUT /boats/<Boat_id>
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

```
Name Type Description Required?
Boat_id String ID of the Boat Yes
```
Request Body
**Name Type Description Required?**
name String The name of the boat. Yes
type String The type of the boat. E.g., Sailboat, Catamaran, etc. Yes
length Integer Length of the boat in feet. Yes

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 401 Unauthorized Error If the request has an invalid or missing JWT this status
code is returned.

```
Failure 405 Method Not
Allowed
```
```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples
_Success_
Status: 200 OK
{
"id": "abc123",
"name": "Sea Witch",
"type": "Catamaran",
"length": 28,
“loads”: “NULL”,
"owner": "Owner Sub JWT",
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error

```
{
```

"Error": "Unauthorized Error”
}
Status: 405 Method Not Allowed

{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Edit a Boat (PATCH)......................................................................................................................................

Edit only one of the attributes of a boat at a time.

```
PUT /boats/<Boat_id>
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

```
Name Type Description Required?
Boat_id String ID of the Boat Yes
```
Request Body
**Name Type Description Required?**
name String The name of the boat. Optional
type String The type of the boat. E.g., Sailboat, Catamaran, etc. Optional
length Integer Length of the boat in feet. Optional

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 401 Unauthorized Error If the request has an invalid or missing JWT this status
code is returned.

```
Failure 405 Method Not
Allowed
```
```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples
_Success_
Status: 200 OK
{
"id": "abc123",
"name": "Sea Witch",
"type": "Catamaran",
"length": 28,
“loads”: “NULL”,
"owner": "Owner Sub JWT",
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error

```
{
```

"Error": "Unauthorized Error”
}
Status: 405 Method Not Allowed

{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Edit a Load (PUT)

Edit all the attributes of a load.

```
PUT /loads/<Load_id>
```
Request

Request Parameters
**Name Type Description Required?**
Load_id String ID of the Load Yes

Request Body
**Name Type Description Required?**
weight Integer Weight of the load Yes
content String Contents in load Yes
delivery_date Integer Date of delivery Yes

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK
{
"id": "abc123",
"weight": 88,
"content": "Eggs",
"delivery_date": “11/21/2021,
“boat”: “NULL”,
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error

```
{
"Error": "Unauthorized Error”
}
Status: 405 Method Not Allowed
```

### {

“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Edit a Load (PATCH)

Edit only one of the attributes of a load at a time.

```
PUT /loads/<Load_id>
```
Request

Request Parameters
**Name Type Description Required?**
Load_id String ID of the Load Yes

Request Body
**Name Type Description Required?**
weight Integer Weight of the load Optional
content String Contents in load Optional
delivery_date Integer Date of delivery Optional

Response

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK
{
"id": "abc123",
"weight": 88,
"content": "Eggs",
"delivery_date": “11/21/2021,
“boat”: “NULL”,
“self”: Entity URL
}
_Failure_
Status: 405 Method Not Allowed

```
{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable
```
```
{
“Error”: “Not Acceptable”
```

### }


## Add a Load to a Boat

Allows you to add a load to a boat.

```
PUT /boats/:boat_id/loads/:load_id
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

```
Name Type Description Required?
Boat_id String ID of the Boat Yes
Load_id String ID of the Load Yes
```
Request Body
None

Response
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 401 Unauthorized Error Missing or invalid JWTs
Failure 403 Forbidden JWT is valid but boat_id is owned by someone else, or
JWT is valid but no boat with this boat_id exists.
Failure 404 Not Found Boat or Load not found. Or Load is already on the boat.
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 200 OK
{
"id": "abc123",
"name": "Sea Witch",
"type": "Catamaran",
"length": 28,
“loads”: “NULL”,
"owner": "Owner Sub JWT",
“self”: Entity URL
}
_Failure_
Status: 401 Unauthorized Error
{
“Error”: “Unauthorized Error”
}
Status: 403 Forbidden
{


“Error”: “Forbidden”
}
Status: 404
{
“Error”: “Boat Not Found”||”Load Not Found”||”Load is already on the boat”
}
Status: 405 Method Not Allowed

{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Remove a Load from the Boat

Allows you to delete a load from the boat.

```
DELETE /boats/:boat_id/loads/:load_id
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

```
Name Type Description Required?
Boat_id String ID of the Boat Yes
Load_id String ID of the Load Yes
```
Request Body
None

Response
JSON

Response Body Format
JSON

Response Statuses
**Outcome Status Code Notes**
Success 200 OK
Failure 401 Unauthorized Error Missing or invalid JWTs
Failure 403 Forbidden JWT is valid but boat_id is owned by someone else, or
JWT is valid but no boat with this boat_id exists.
Failure 404 Not Found Boat or Load not found.
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
Response Examples

_Success_
Status: 200 OK
_Failure_
Status: 401 Unauthorized Error
{
“Error”: “Unauthorized Error”
}
Status: 403 Forbidden
{
“Error”: “Forbidden”
}
Status: 404
{
“Error”: “Boat Not Found”||”Load Not Found”
}
Status: 405 Method Not Allowed


### {

“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Delete a Boat

Allows you to delete a boat.

```
DELETE /boats/:boat_id
```
Request

Request Parameters
JWT must be included in the Header as an Authorization.

```
Name Type Description Required?
Boat_id String ID of the Boat Yes
```
Request Body
None

Response
No body

Response Body Format
Success: No body

Failure: JSON

Response Statuses
**Outcome Status Code Notes**
Success 204 No Content
Failure 401 Unauthorized Error Missing or invalid JWTs
Failure 403 Forbidden JWT is valid but boat_id is owned by someone else, or
JWT is valid but no boat with this boat_id exists.
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 204 No Content
_Failure_
Status: 401 Unauthorized Error
{
“Error”: “Unauthorized Error”
}
Status: 403 Forbidden
{
“Error”: “Forbidden”
}
Status: 405 Method Not Allowed

```
{
“Error”: “Method Not Allowed”
```

### }

Status: 406 Not Acceptable

{
“Error”: “Not Acceptable”
}


## Delete a Load

Allows you to delete a Load.

```
DELETE /loads/:load_id
```
Request

Request Parameters
**Name Type Description Required?**
Load_id String ID of the Load Yes

Request Body
None

Response
No body

Response Body Format
Success: No body

Failure: JSON

Response Statuses
**Outcome Status Code Notes**
Success 204 No Content
Failure 405 Method Not
Allowed

```
Wrong HTTP Verb used.
```
```
Failure 406 Not Acceptable Another type other than ‘application/json’ was used.
```
Response Examples

_Success_
Status: 204 No Content
_Failure_
Status: 401 Unauthorized Error
{
“Error”: “Unauthorized Error”
}
Status: 405 Method Not Allowed

```
{
“Error”: “Method Not Allowed”
}
Status: 406 Not Acceptable
```
```
{
“Error”: “Not Acceptable”
}
```
