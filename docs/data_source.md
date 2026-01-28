Available API for PSE:
https://api.raporty.pse.pl/app/home

Server: https://api.raporty.pse.pl/api

API with the prices we are looking for:
https://api.raporty.pse.pl/api/rce-pln

**Parameters:** 

$select string (query) - A comma separated list of fields to return in the response.

$filter string (query) - An OData expression (an expression that returns a boolean value) using the entity's fields to retrieve a subset of the results.

$orderby string (query) - Uses a comma-separated list of expressions to sort response items. Add 'desc' for descending order, otherwise it's ascending by default.

$first integer (query)  - An integer value that specifies the number of items to return. Default is 100.

$after string (query) - An opaque string that specifies the cursor position after which results should be returned.

**Responses**
Code - Description

200 - OK

Media type: application.json

{
  "value": [
    {
      "dtime": "string",
      "dtime_utc": "string",
      "period": "string",
      "period_utc": "string",
      "rce_pln": 0,
      "business_date": "string",
      "publication_ts": "string",
      "publication_ts_utc": "string"
    }
  ],
  "nextLink": "string"
}

400	- BadRequest
	
403	- Forbidden

404	- NotFound

**SAMPLE OF THE API RESPONSE**

**Curl**

curl -X 'GET' \
  'https://api.raporty.pse.pl/api/rce-pln' \
  -H 'accept: application/json'

**Request URL**

https://api.raporty.pse.pl/api/rce-pln

**Server response**

{
  "value": [
    {
      "dtime": "2024-06-14 00:15:00",
      "period": "00:00 - 00:15",
      "rce_pln": 876.1,
      "dtime_utc": "2024-06-13 22:15:00",
      "period_utc": "22:00 - 22:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 00:30:00",
      "period": "00:15 - 00:30",
      "rce_pln": 876.1,
      "dtime_utc": "2024-06-13 22:30:00",
      "period_utc": "22:15 - 22:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 00:45:00",
      "period": "00:30 - 00:45",
      "rce_pln": 876.1,
      "dtime_utc": "2024-06-13 22:45:00",
      "period_utc": "22:30 - 22:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 01:00:00",
      "period": "00:45 - 01:00",
      "rce_pln": 876.1,
      "dtime_utc": "2024-06-13 23:00:00",
      "period_utc": "22:45 - 23:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 01:15:00",
      "period": "01:00 - 01:15",
      "rce_pln": 577.43,
      "dtime_utc": "2024-06-13 23:15:00",
      "period_utc": "23:00 - 23:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 01:30:00",
      "period": "01:15 - 01:30",
      "rce_pln": 577.43,
      "dtime_utc": "2024-06-13 23:30:00",
      "period_utc": "23:15 - 23:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 01:45:00",
      "period": "01:30 - 01:45",
      "rce_pln": 577.43,
      "dtime_utc": "2024-06-13 23:45:00",
      "period_utc": "23:30 - 23:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 02:00:00",
      "period": "01:45 - 02:00",
      "rce_pln": 577.43,
      "dtime_utc": "2024-06-14 00:00:00",
      "period_utc": "23:45 - 24:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 02:15:00",
      "period": "02:00 - 02:15",
      "rce_pln": 449.14,
      "dtime_utc": "2024-06-14 00:15:00",
      "period_utc": "00:00 - 00:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 02:30:00",
      "period": "02:15 - 02:30",
      "rce_pln": 449.14,
      "dtime_utc": "2024-06-14 00:30:00",
      "period_utc": "00:15 - 00:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 02:45:00",
      "period": "02:30 - 02:45",
      "rce_pln": 449.14,
      "dtime_utc": "2024-06-14 00:45:00",
      "period_utc": "00:30 - 00:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 03:00:00",
      "period": "02:45 - 03:00",
      "rce_pln": 449.14,
      "dtime_utc": "2024-06-14 01:00:00",
      "period_utc": "00:45 - 01:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 03:15:00",
      "period": "03:00 - 03:15",
      "rce_pln": 446.4,
      "dtime_utc": "2024-06-14 01:15:00",
      "period_utc": "01:00 - 01:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 03:30:00",
      "period": "03:15 - 03:30",
      "rce_pln": 446.4,
      "dtime_utc": "2024-06-14 01:30:00",
      "period_utc": "01:15 - 01:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 03:45:00",
      "period": "03:30 - 03:45",
      "rce_pln": 446.4,
      "dtime_utc": "2024-06-14 01:45:00",
      "period_utc": "01:30 - 01:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 04:00:00",
      "period": "03:45 - 04:00",
      "rce_pln": 446.4,
      "dtime_utc": "2024-06-14 02:00:00",
      "period_utc": "01:45 - 02:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 04:15:00",
      "period": "04:00 - 04:15",
      "rce_pln": 448.9,
      "dtime_utc": "2024-06-14 02:15:00",
      "period_utc": "02:00 - 02:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 04:30:00",
      "period": "04:15 - 04:30",
      "rce_pln": 448.9,
      "dtime_utc": "2024-06-14 02:30:00",
      "period_utc": "02:15 - 02:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 04:45:00",
      "period": "04:30 - 04:45",
      "rce_pln": 448.9,
      "dtime_utc": "2024-06-14 02:45:00",
      "period_utc": "02:30 - 02:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 05:00:00",
      "period": "04:45 - 05:00",
      "rce_pln": 448.9,
      "dtime_utc": "2024-06-14 03:00:00",
      "period_utc": "02:45 - 03:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 05:15:00",
      "period": "05:00 - 05:15",
      "rce_pln": 471.88,
      "dtime_utc": "2024-06-14 03:15:00",
      "period_utc": "03:00 - 03:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 05:30:00",
      "period": "05:15 - 05:30",
      "rce_pln": 471.88,
      "dtime_utc": "2024-06-14 03:30:00",
      "period_utc": "03:15 - 03:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 05:45:00",
      "period": "05:30 - 05:45",
      "rce_pln": 471.88,
      "dtime_utc": "2024-06-14 03:45:00",
      "period_utc": "03:30 - 03:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 06:00:00",
      "period": "05:45 - 06:00",
      "rce_pln": 471.88,
      "dtime_utc": "2024-06-14 04:00:00",
      "period_utc": "03:45 - 04:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 06:15:00",
      "period": "06:00 - 06:15",
      "rce_pln": 498.01,
      "dtime_utc": "2024-06-14 04:15:00",
      "period_utc": "04:00 - 04:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 06:30:00",
      "period": "06:15 - 06:30",
      "rce_pln": 498.01,
      "dtime_utc": "2024-06-14 04:30:00",
      "period_utc": "04:15 - 04:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 06:45:00",
      "period": "06:30 - 06:45",
      "rce_pln": 498.01,
      "dtime_utc": "2024-06-14 04:45:00",
      "period_utc": "04:30 - 04:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 07:00:00",
      "period": "06:45 - 07:00",
      "rce_pln": 498.01,
      "dtime_utc": "2024-06-14 05:00:00",
      "period_utc": "04:45 - 05:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 07:15:00",
      "period": "07:00 - 07:15",
      "rce_pln": 536.97,
      "dtime_utc": "2024-06-14 05:15:00",
      "period_utc": "05:00 - 05:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 07:30:00",
      "period": "07:15 - 07:30",
      "rce_pln": 536.97,
      "dtime_utc": "2024-06-14 05:30:00",
      "period_utc": "05:15 - 05:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 07:45:00",
      "period": "07:30 - 07:45",
      "rce_pln": 536.97,
      "dtime_utc": "2024-06-14 05:45:00",
      "period_utc": "05:30 - 05:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 08:00:00",
      "period": "07:45 - 08:00",
      "rce_pln": 536.97,
      "dtime_utc": "2024-06-14 06:00:00",
      "period_utc": "05:45 - 06:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 08:15:00",
      "period": "08:00 - 08:15",
      "rce_pln": 509.52,
      "dtime_utc": "2024-06-14 06:15:00",
      "period_utc": "06:00 - 06:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 08:30:00",
      "period": "08:15 - 08:30",
      "rce_pln": 509.52,
      "dtime_utc": "2024-06-14 06:30:00",
      "period_utc": "06:15 - 06:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 08:45:00",
      "period": "08:30 - 08:45",
      "rce_pln": 509.52,
      "dtime_utc": "2024-06-14 06:45:00",
      "period_utc": "06:30 - 06:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 09:00:00",
      "period": "08:45 - 09:00",
      "rce_pln": 509.52,
      "dtime_utc": "2024-06-14 07:00:00",
      "period_utc": "06:45 - 07:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 09:15:00",
      "period": "09:00 - 09:15",
      "rce_pln": 442.55,
      "dtime_utc": "2024-06-14 07:15:00",
      "period_utc": "07:00 - 07:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 09:30:00",
      "period": "09:15 - 09:30",
      "rce_pln": 442.55,
      "dtime_utc": "2024-06-14 07:30:00",
      "period_utc": "07:15 - 07:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 09:45:00",
      "period": "09:30 - 09:45",
      "rce_pln": 442.55,
      "dtime_utc": "2024-06-14 07:45:00",
      "period_utc": "07:30 - 07:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 10:00:00",
      "period": "09:45 - 10:00",
      "rce_pln": 442.55,
      "dtime_utc": "2024-06-14 08:00:00",
      "period_utc": "07:45 - 08:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 10:15:00",
      "period": "10:00 - 10:15",
      "rce_pln": 368.76,
      "dtime_utc": "2024-06-14 08:15:00",
      "period_utc": "08:00 - 08:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 10:30:00",
      "period": "10:15 - 10:30",
      "rce_pln": 368.76,
      "dtime_utc": "2024-06-14 08:30:00",
      "period_utc": "08:15 - 08:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 10:45:00",
      "period": "10:30 - 10:45",
      "rce_pln": 368.76,
      "dtime_utc": "2024-06-14 08:45:00",
      "period_utc": "08:30 - 08:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 11:00:00",
      "period": "10:45 - 11:00",
      "rce_pln": 368.76,
      "dtime_utc": "2024-06-14 09:00:00",
      "period_utc": "08:45 - 09:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 11:15:00",
      "period": "11:00 - 11:15",
      "rce_pln": 361.77,
      "dtime_utc": "2024-06-14 09:15:00",
      "period_utc": "09:00 - 09:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 11:30:00",
      "period": "11:15 - 11:30",
      "rce_pln": 361.77,
      "dtime_utc": "2024-06-14 09:30:00",
      "period_utc": "09:15 - 09:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 11:45:00",
      "period": "11:30 - 11:45",
      "rce_pln": 361.77,
      "dtime_utc": "2024-06-14 09:45:00",
      "period_utc": "09:30 - 09:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 12:00:00",
      "period": "11:45 - 12:00",
      "rce_pln": 361.77,
      "dtime_utc": "2024-06-14 10:00:00",
      "period_utc": "09:45 - 10:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 12:15:00",
      "period": "12:00 - 12:15",
      "rce_pln": 374.61,
      "dtime_utc": "2024-06-14 10:15:00",
      "period_utc": "10:00 - 10:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 12:30:00",
      "period": "12:15 - 12:30",
      "rce_pln": 374.61,
      "dtime_utc": "2024-06-14 10:30:00",
      "period_utc": "10:15 - 10:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 12:45:00",
      "period": "12:30 - 12:45",
      "rce_pln": 374.61,
      "dtime_utc": "2024-06-14 10:45:00",
      "period_utc": "10:30 - 10:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 13:00:00",
      "period": "12:45 - 13:00",
      "rce_pln": 374.61,
      "dtime_utc": "2024-06-14 11:00:00",
      "period_utc": "10:45 - 11:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 13:15:00",
      "period": "13:00 - 13:15",
      "rce_pln": 444.55,
      "dtime_utc": "2024-06-14 11:15:00",
      "period_utc": "11:00 - 11:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 13:30:00",
      "period": "13:15 - 13:30",
      "rce_pln": 444.55,
      "dtime_utc": "2024-06-14 11:30:00",
      "period_utc": "11:15 - 11:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 13:45:00",
      "period": "13:30 - 13:45",
      "rce_pln": 444.55,
      "dtime_utc": "2024-06-14 11:45:00",
      "period_utc": "11:30 - 11:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 14:00:00",
      "period": "13:45 - 14:00",
      "rce_pln": 444.55,
      "dtime_utc": "2024-06-14 12:00:00",
      "period_utc": "11:45 - 12:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 14:15:00",
      "period": "14:00 - 14:15",
      "rce_pln": 448.51,
      "dtime_utc": "2024-06-14 12:15:00",
      "period_utc": "12:00 - 12:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 14:30:00",
      "period": "14:15 - 14:30",
      "rce_pln": 448.51,
      "dtime_utc": "2024-06-14 12:30:00",
      "period_utc": "12:15 - 12:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 14:45:00",
      "period": "14:30 - 14:45",
      "rce_pln": 448.51,
      "dtime_utc": "2024-06-14 12:45:00",
      "period_utc": "12:30 - 12:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 15:00:00",
      "period": "14:45 - 15:00",
      "rce_pln": 448.51,
      "dtime_utc": "2024-06-14 13:00:00",
      "period_utc": "12:45 - 13:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 15:15:00",
      "period": "15:00 - 15:15",
      "rce_pln": 488.29,
      "dtime_utc": "2024-06-14 13:15:00",
      "period_utc": "13:00 - 13:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 15:30:00",
      "period": "15:15 - 15:30",
      "rce_pln": 488.29,
      "dtime_utc": "2024-06-14 13:30:00",
      "period_utc": "13:15 - 13:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 15:45:00",
      "period": "15:30 - 15:45",
      "rce_pln": 488.29,
      "dtime_utc": "2024-06-14 13:45:00",
      "period_utc": "13:30 - 13:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 16:00:00",
      "period": "15:45 - 16:00",
      "rce_pln": 488.29,
      "dtime_utc": "2024-06-14 14:00:00",
      "period_utc": "13:45 - 14:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 16:15:00",
      "period": "16:00 - 16:15",
      "rce_pln": 473.03,
      "dtime_utc": "2024-06-14 14:15:00",
      "period_utc": "14:00 - 14:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 16:30:00",
      "period": "16:15 - 16:30",
      "rce_pln": 473.03,
      "dtime_utc": "2024-06-14 14:30:00",
      "period_utc": "14:15 - 14:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 16:45:00",
      "period": "16:30 - 16:45",
      "rce_pln": 473.03,
      "dtime_utc": "2024-06-14 14:45:00",
      "period_utc": "14:30 - 14:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 17:00:00",
      "period": "16:45 - 17:00",
      "rce_pln": 473.03,
      "dtime_utc": "2024-06-14 15:00:00",
      "period_utc": "14:45 - 15:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 17:15:00",
      "period": "17:00 - 17:15",
      "rce_pln": 483.5,
      "dtime_utc": "2024-06-14 15:15:00",
      "period_utc": "15:00 - 15:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 17:30:00",
      "period": "17:15 - 17:30",
      "rce_pln": 483.5,
      "dtime_utc": "2024-06-14 15:30:00",
      "period_utc": "15:15 - 15:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 17:45:00",
      "period": "17:30 - 17:45",
      "rce_pln": 483.5,
      "dtime_utc": "2024-06-14 15:45:00",
      "period_utc": "15:30 - 15:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 18:00:00",
      "period": "17:45 - 18:00",
      "rce_pln": 483.5,
      "dtime_utc": "2024-06-14 16:00:00",
      "period_utc": "15:45 - 16:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 18:15:00",
      "period": "18:00 - 18:15",
      "rce_pln": 886.78,
      "dtime_utc": "2024-06-14 16:15:00",
      "period_utc": "16:00 - 16:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 18:30:00",
      "period": "18:15 - 18:30",
      "rce_pln": 886.78,
      "dtime_utc": "2024-06-14 16:30:00",
      "period_utc": "16:15 - 16:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 18:45:00",
      "period": "18:30 - 18:45",
      "rce_pln": 886.78,
      "dtime_utc": "2024-06-14 16:45:00",
      "period_utc": "16:30 - 16:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 19:00:00",
      "period": "18:45 - 19:00",
      "rce_pln": 886.78,
      "dtime_utc": "2024-06-14 17:00:00",
      "period_utc": "16:45 - 17:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 19:15:00",
      "period": "19:00 - 19:15",
      "rce_pln": 719.18,
      "dtime_utc": "2024-06-14 17:15:00",
      "period_utc": "17:00 - 17:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 19:30:00",
      "period": "19:15 - 19:30",
      "rce_pln": 719.18,
      "dtime_utc": "2024-06-14 17:30:00",
      "period_utc": "17:15 - 17:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 19:45:00",
      "period": "19:30 - 19:45",
      "rce_pln": 719.18,
      "dtime_utc": "2024-06-14 17:45:00",
      "period_utc": "17:30 - 17:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 20:00:00",
      "period": "19:45 - 20:00",
      "rce_pln": 719.18,
      "dtime_utc": "2024-06-14 18:00:00",
      "period_utc": "17:45 - 18:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 20:15:00",
      "period": "20:00 - 20:15",
      "rce_pln": 783.9,
      "dtime_utc": "2024-06-14 18:15:00",
      "period_utc": "18:00 - 18:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 20:30:00",
      "period": "20:15 - 20:30",
      "rce_pln": 783.9,
      "dtime_utc": "2024-06-14 18:30:00",
      "period_utc": "18:15 - 18:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 20:45:00",
      "period": "20:30 - 20:45",
      "rce_pln": 783.9,
      "dtime_utc": "2024-06-14 18:45:00",
      "period_utc": "18:30 - 18:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 21:00:00",
      "period": "20:45 - 21:00",
      "rce_pln": 783.9,
      "dtime_utc": "2024-06-14 19:00:00",
      "period_utc": "18:45 - 19:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 21:15:00",
      "period": "21:00 - 21:15",
      "rce_pln": 734.65,
      "dtime_utc": "2024-06-14 19:15:00",
      "period_utc": "19:00 - 19:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 21:30:00",
      "period": "21:15 - 21:30",
      "rce_pln": 734.65,
      "dtime_utc": "2024-06-14 19:30:00",
      "period_utc": "19:15 - 19:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 21:45:00",
      "period": "21:30 - 21:45",
      "rce_pln": 734.65,
      "dtime_utc": "2024-06-14 19:45:00",
      "period_utc": "19:30 - 19:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 22:00:00",
      "period": "21:45 - 22:00",
      "rce_pln": 734.65,
      "dtime_utc": "2024-06-14 20:00:00",
      "period_utc": "19:45 - 20:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 22:15:00",
      "period": "22:00 - 22:15",
      "rce_pln": 584.58,
      "dtime_utc": "2024-06-14 20:15:00",
      "period_utc": "20:00 - 20:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 22:30:00",
      "period": "22:15 - 22:30",
      "rce_pln": 584.58,
      "dtime_utc": "2024-06-14 20:30:00",
      "period_utc": "20:15 - 20:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 22:45:00",
      "period": "22:30 - 22:45",
      "rce_pln": 584.58,
      "dtime_utc": "2024-06-14 20:45:00",
      "period_utc": "20:30 - 20:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 23:00:00",
      "period": "22:45 - 23:00",
      "rce_pln": 584.58,
      "dtime_utc": "2024-06-14 21:00:00",
      "period_utc": "20:45 - 21:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 23:15:00",
      "period": "23:00 - 23:15",
      "rce_pln": 472.72,
      "dtime_utc": "2024-06-14 21:15:00",
      "period_utc": "21:00 - 21:15",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 23:30:00",
      "period": "23:15 - 23:30",
      "rce_pln": 472.72,
      "dtime_utc": "2024-06-14 21:30:00",
      "period_utc": "21:15 - 21:30",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-14 23:45:00",
      "period": "23:30 - 23:45",
      "rce_pln": 472.72,
      "dtime_utc": "2024-06-14 21:45:00",
      "period_utc": "21:30 - 21:45",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-15 00:00:00",
      "period": "23:45 - 24:00",
      "rce_pln": 472.72,
      "dtime_utc": "2024-06-14 22:00:00",
      "period_utc": "21:45 - 22:00",
      "business_date": "2024-06-14",
      "publication_ts": "2024-06-13 17:05:05",
      "publication_ts_utc": "2024-06-13 15:05:05.000000"
    },
    {
      "dtime": "2024-06-15 00:15:00",
      "period": "00:00 - 00:15",
      "rce_pln": 548.73,
      "dtime_utc": "2024-06-14 22:15:00",
      "period_utc": "22:00 - 22:15",
      "business_date": "2024-06-15",
      "publication_ts": "2024-06-14 14:24:05.631",
      "publication_ts_utc": "2024-06-14 12:24:05.631000"
    },
    {
      "dtime": "2024-06-15 00:30:00",
      "period": "00:15 - 00:30",
      "rce_pln": 548.73,
      "dtime_utc": "2024-06-14 22:30:00",
      "period_utc": "22:15 - 22:30",
      "business_date": "2024-06-15",
      "publication_ts": "2024-06-14 14:24:05.631",
      "publication_ts_utc": "2024-06-14 12:24:05.631000"
    },
    {
      "dtime": "2024-06-15 00:45:00",
      "period": "00:30 - 00:45",
      "rce_pln": 548.73,
      "dtime_utc": "2024-06-14 22:45:00",
      "period_utc": "22:30 - 22:45",
      "business_date": "2024-06-15",
      "publication_ts": "2024-06-14 14:24:05.631",
      "publication_ts_utc": "2024-06-14 12:24:05.631000"
    },
    {
      "dtime": "2024-06-15 01:00:00",
      "period": "00:45 - 01:00",
      "rce_pln": 548.73,
      "dtime_utc": "2024-06-14 23:00:00",
      "period_utc": "22:45 - 23:00",
      "business_date": "2024-06-15",
      "publication_ts": "2024-06-14 14:24:05.631",
      "publication_ts_utc": "2024-06-14 12:24:05.631000"
    }
  ],
  "nextLink": "https://api.raporty.pse.pl/api/rce-pln?$after=W3siRW50aXR5TmFtZSI6InJjZS1wbG4iLCJGaWVsZE5hbWUiOiJkdGltZV91dGMiLCJGaWVsZFZhbHVlIjoiMjAyNC0wNi0xNCAyMzowMDowMCIsIkRpcmVjdGlvbiI6MH1d"
}

**Response Headers**

 content-type: application/json; charset=utf-8 
 date: Wed,28 Jan 2026 05:14:45 GMT 
 x-azure-ref: 20260128T051445Z-15f8bd58b94hwsb7hC1FRA6pv800000020a00000000012bp 
 x-cache: CONFIG_NOCACHE 
 x-firefox-spdy: h2 
 x-ms-correlation-id: 150658ee-7bde-4b6b-9a5b-fd9b78dd9274 
 x-ms-middleware-request-id: 00000000-0000-0000-0000-000000000000 

**Filter for seeking a day data**

dtime ge '2025-10-26T00:00:00Z' and dtime lt '2025-10-27T00:00:00Z'

**Useful values set**

dtime,period,rce_pln,dtime_utc,business_date
