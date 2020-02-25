# fibo-rest

### Exemplary project presenting microservices-like approach to calculating fibonacci sequence.

## Usage

1. Clone the repository
    
    ```shell script
    git clone git@github.com:pywkm/fibo-rest.git
    cd fibo-rest
    ```
1. Make `.env` file (you can use example one included and change desired values)
    
    ```shell script
    cp .env.example .env
    ```

1. Run dev server
    
    ```shell script
    make start-dev
    ```

That's all, application is working, and exposing API on the `http://localhost:5555` server
(if you hadn't change port in `.env` file).

### API endpoints
There are only two endpoints exposed:

* GET `/api/fibo/<length>`

    To retrieve sequence `<length>` long

    Exemplary request:
    * GET `http://localhost/api/fibo/5`
    
    Exemplary response:
    * Status code: 200
    
        Payload:
        ```json
        [0, 1, 1, 2, 3]
        ```
    
    Because we are simulating, that calculating fibonacci sequences is time consuming (which is true for very long
    sequences in fact), GET request to that endpoint doesn't always return status code 200 (OK) and response with sequence.

    When sequence isn't already calculated (and cached in database), API will respond with status code 202 (Accepted):

    Exemplary request:
    * GET `http://localhost/api/fibo/55`
    
    Exemplary response:
    * Status code: 202
    
        Payload:
        ```json
        {
            "statusUri": "/api/fibo/55/status",
            "estimatedTime": "2020-03-03 12:12:12"
        }
        ```
     Which means calculation is triggered, and result should be accessible around `estimatedTime` on the `/api/fibo/55`
     endpoint. There's url to status endpoint, where calculation progress can be monitored.

* GET `/api/fibo/<length>/status`

    To check status of (previously triggered) `<length>` long calculation

    Exemplary request:
    * GET `http://localhost/api/fibo/55/status`
    
    Exemplary response:
    * Status code: 200
    
        Payload:
        ```json
        {
            "estimatedTime": "2020-03-03 12:12:22",
            "numbersCalculated": 15,
            "numbersRequired": 55
        }
     
     The `estimatedTime` may differ from original one got from `/api/fibo/<length>` endpoint, because it is updated "live".
     
     If calculation of particular wasn't sequence wasn't triggered yet (by request to the first endpoint), status will
     return Not Found response:
     
         Exemplary request:
    * GET `http://localhost/api/fibo/515/status`
    
    Exemplary response:
    * Status code: 404

## Architecture

Application is built from 5 microservices:

* `api`
    * Falcon + gunicorn
    * exposed on the `GUNICORN_PORT`
    * communicates with `database` and `rabbitmq` to
        
        a) check if sequence is already calculated and stored in the database. If so - return it immediately
        
        b) if wasn't calculated - send calculation request to the RabbitMQ queue
        
        c) retrieve calculation status from database (if available)

* `database`
    * PostgreSQL engine (plus static volume for data)
    * exposed on the `DB_PORT_EXPOSE` (doesn't have to be defined - won't be exposed outside the internal network)
    * storage of calculated Fibonacci numbers, and calculation statuses for requested calculations
    
* `rabbitmq`
    * RabbitMQ backend
    * Not accessible from outside
    * Provides communication between `api`, `generator` and `ingest` services

* `generator`
    * Pure Python
    * Not accessible from outside
    * Simple application for calculating Fibonacci numbers and putting them to the RabbitMQ queue
    
* `ingest`
    * Pure Python
    * Not accessible from outside
    * Consumes Fibo numbers from RabbitMQ queue and puts them into `database`
    
This is just only the POC. We are simulating here any time consuming calculations, that can be cached (returned immediately)
or outsourced for later execution. In fact Fibonacci sequence calculation can be done in reasonable time up to quite big length (~1000)
so here we are slowing that down with `FIBO_DIFICULTY` parameter (microseconds required to calculate one number), but think about
image processing, or prime numbers calculations - you don't get results right away unless it is already cached on the backend.


## Local development and contributing

1. (Fork and) clone repository if you didn't already do this (see the Usage section)
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
1. If tests and linting doesn't throw an error you can create pull request to the pywkm:master branch