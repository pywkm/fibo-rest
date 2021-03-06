# Fibo REST

### Simple project presenting microservices-like approach to calculating Fibonacci sequences.

As an example of any time-consuming task that can be modeled in a such way.

## Usage

1. Prerequisites (needs to be installed on the system to run application)

    * Docker (ver. 17.06.0+)
    * docker-compose (ver. 1.14.0+)
    * make

1. Clone the repository

    ```shell script
    git clone git@github.com:pywkm/fibo-rest.git
    cd fibo-rest
    ```

1. Create `.env` file (you can use example one included and change desired values)
    
    ```shell script
    cp .env.example .env
    edit .env
    ```

1. Run dev server
    
    ```shell script
    make start-dev
    ```

1. If first time running, or when you want to clear DB, initialize it by:
    
    ```shell script
    make init-db
    ```
   _WARNING: Do not clear DB when app was running for a moment, and generator already cached
   calculations in the memory (caching was on). App is not intended to work properly in such case. 
   Generator service should be restarted in that scenario._


That's all, application is working, and exposing API on the `http://localhost:5555` server
(unless you changed the port in `.env` file).

To stop running containers, use command:

```shell script
make stop-dev
```

More information about available make commands:

```shell script
make help
```

### API endpoints
There are only two endpoints exposed:

* GET `/fibo/<length>`

    To retrieve sequence `<length>` long

    Exemplary request:
    * GET `http://localhost:5555/fibo/5`
    
    Exemplary response:
    * Status code: 200
    
        Payload:
        ```json
        {
            "sequence": [0, 1, 1, 2, 3]
        }     
        ```
    
    Because we are simulating the calculation Fibonacci sequence is time-consuming (which is true for very long
    sequences), GET request to that endpoint doesn't always return status code 200 (OK) and response with sequence.

    When sequence isn't cached in database, API will respond with status code 202 (Accepted) with different response
    body:

    Exemplary request:
    * GET `http://localhost:5555/fibo/55`
    
    Exemplary response:
    * Status code: 202
    
        Payload:
        ```json
        {
            "sequence": null,
            "statusUri": "/fibo/55/status",
            "eta": "2020-03-03 12:12:12.120021"
        }
        ```
     Which means calculation is triggered, and result should be accessible around `eta` on
     the `/fibo/55` endpoint. There's given uri to status endpoint, where calculation progress can
     be monitored. `eta` is given in the UTC time zone.

* GET `/fibo/<length>/status`

    To check status of (previously triggered) `<length>` long sequence calculation

    Exemplary request:
    * GET `http://localhost:5555/fibo/55/status`
    
    Exemplary response:
    * Status code: 200
    
        Payload:
        ```json
        {
            "eta": "2020-03-03 12:12:22.002200",
            "numbersCalculated": 15,
            "numbersRequired": 55
        }
     
    The `eta` may differ from original one got from `/fibo/<length>` endpoint, because it
    is updated on every status request.
    
    If calculation of particular sequence wasn't triggered yet (by request to the first endpoint),
    status endpoint will return Not Found (404) response:
     
    Exemplary request:
    * GET `http://localhost:5555/fibo/515/status`
    
    Exemplary response:
    * Status code: 404
        
        Payload:
        ```json
        {
            "message": "Calculation for sequence:515 wasn't requested yet"
        }
        ```

## Architecture

Application is built from 5 microservices:

* `api`
    * Falcon + gunicorn + pika
    * Exposed on the `GUNICORN_PORT`
    * Communicates with `database` and `rabbitmq` to
        
        a) check if sequence is already calculated and stored in the database. If so - return it
           immediately
        
        b) if wasn't calculated - send calculation request to the RabbitMQ queue
        
        c) retrieve calculation status from database (if available)

* `database`
    * PostgreSQL engine (plus static volume for data)
    * Exposed on the `DB_PORT`, rest of the credentials are in .env file 
    * Stores calculated Fibonacci numbers, and calculation statuses for requested calculations
    
* `rabbitmq`
    * RabbitMQ server
    * Only the web UI exposed outside (port 15672)
    * Provides communication between `api`, `generator` and `ingest` services

* `generator`
    * Pure Python (with pika)
    * Not accessible from outside
    * Simple application for calculating Fibonacci numbers and putting them to the RabbitMQ queue
    
* `ingest`
    * Pure Python (with pika and db driver)
    * Not accessible from outside
    * Consumes Fibo numbers from RabbitMQ queue and puts them into `database`
    
This is only the PoC. We are simulating here any time-consuming calculations that can be
cached (returned immediately) or outsourced for later execution. In fact Fibonacci sequence
calculation can be done in reasonable time up to quite big length (~1000) so here we are slowing
that down artificially with `FIBO_DIFICULTY` parameter in `.env` (microseconds required to calculate
one number), but think about image processing, hashing or prime numbers calculations - you don't get
results right away unless it is already cached on the backend.


## Local development and contributing

1. (Fork and) clone repository if you haven't already done this (see the Usage section)
1. Create virtual environment with Python3.7+ and activate it. For example with `virtualenvwrapper`:

    ```shell script
    mkvirtualenv fibo-rest -p python3.7
    ```

1. Install dependencies:

    ```shell script
    make setup-dev
    ```

1. Create branch with descriptive name
1. Make some changes in the code
1. Add and run tests (pytest). Or start with tests, as you wish.

    ```shell script
    make test
    ```

1. Run code formatter (we use black and isort):

    ```shell script
    make format
    ```

1. Run linter and static type checker to see if everything else is OK:

    ```shell script
    make lint
    ```

1. If all tests pass and linting doesn't throw an error feel free to create pull request to the 
   pywkm/fibo-rest:master branch.

1. If you've found error or have an idea for improvement don't hesitate to report the Github issue.


## TODOs (known flaws):
- [ ] Add integration test for DB storage;
- [ ] Add e2e tests;
- [ ] Make `ingest` testable;
- [ ] Add dependency injection in main app (`api`), more clean architecture in the rest of apps;
- [ ] Make `ingest` more robust/foolproof (retry on error);
- [ ] Make `messaging` more robust (reconnect consuming channel when connection was lost).
