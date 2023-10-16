# PredictHQ API Handler

## Overview

This is the implementation of the PredictHQ API handler for MindsDB.

### PredictHQ

PredictHQ is a demand intelligence solution that helps businesses correlate event data to demand. It tracks event data in 19 categories and ranks events using a proprietary ranking system. The platform provides detailed expansive coverage of public holidays, observances, school holidays, and academic holidays globally. It also tracks remembrance, awareness, and celebration days or events that are not normally days off work, like Valentine’s Day, Mother’s Day, or Father’s Day.

In summary, PredictHQ is a platform that helps businesses understand how events drive demand for their business.

For more information about the PredictHQ API, you can visit [this link](https://docs.predicthq.com/predicthq-api/overview).

To generate an API token for accessing PredictHQ API, please follow the instructions in [this link](https://www.predicthq.com/support/how-to-create-an-api-token).

## PredictHQ Handler Initialization

The PredictHQ handler is initialized with the following parameters:

- `client_id`: A required PredictHQ API client ID.
- `client_secret`: A required PredictHQ API client secret.

### Example Usage

```sql
CREATE DATABASE my_PredictHQ
With 
    ENGINE = 'PredictHQ',
    PARAMETERS = {
     "client_id": "YOUR_CLIENT_ID",
     "client_secret": "YOUR_CLIENT_SECRET"
    };
```


## Implementation

This handler was implemented as per the (Application Handler framework)[https://docs.mindsdb.com/contribute/app-handlers]
