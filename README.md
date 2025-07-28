<h1 align="center">
  Manage Stocks
</h1>

## Index

<p align="center">
  <a href="#gear-requirements">Requirements</a> |
  <a href="#package-how-to-download-the-project">Download</a> |
  <a href="#wrench-how-to-use">How to Use</a> |
  <a href="#test_tube-run-tests">Run Tests</a> |
  <a href="#electric_plug-routes-use">Routes API</a> |
  <a href="#building_construction-architecture">Architecture</a> |
  <a href="#bust_in_silhouette-autor">Author</a> |
  <a href="#pencil-licença">Licence</a>
</p>

## :gear: Requirements

Global

- **Polygon API Key** (get on https://polygon.io).

Use Localhost and Run Tests

- **Python** >= 3.10
- **Poetry** >= 1.5 (latest recommended is 1.8.x)
- **GNU Make** (to run CLI shortcuts via `make`)

Use Docker

- **Docker** >= 20.10
- **Docker Compose** V2 (>= 2.2)

## :package: How to Download the Project

Open your terminal, navigate to your desired folder, and run the commands below:

```bash
  # Clone the repo
  $ git clone https://github.com/luizcampos331/manage-stocks.git

  # Access the directory
  $ cd manage-stocks
```

## :wrench: How to Use

1. Duplicate the file .env.example to .env and define STOCK_API_KEY with Polygon API Key

2. Run the application:

```bash
  # **LOCALHOST**
  # Install the project as a package
  $ make install

  # Run migrations (It is necessary to have a PostgreSQL database running. If it is running outside of Docker, update the env DATABASE_URL in the .env file.)
  $ make migrate

  # OBS: If Redis is running outside of Docker, update the env CACHE_URL in the .env file.
  # Run the project
  $ make run

  # **DOCKER**
  # Create containers and run project
  $ docker compose up -d
  $ docker exec -it manage-stocks-api-1 make migrate

  # Create and run only api
  $ docker compose up -d api

  # Create and run only db
  $ docker compose up -d postgres
  $ docker exec -it manage-stocks-api-1 make migrate

  # Create and run only cache
  $ docker compose up -d redis
```

## :test_tube: Run Tests

This project uses automated tests to ensure code stability and reliability.

```bash
  # Install the project as a package
  $ make install

  # Run only tests
  $ make test

  # Run tests with coverage
  $ make test-cov

  # The coverage report will be available at:
  # ./htmlcov/index.html
```

Technologies Used
- pytest — test framework

## :electric_plug: Routes API
## API Routes

| Method | Route | Description |
|-------|------|-----------|
| `GET` | `/` | Returns a string with the API version (e.g., `"Manage Stocks API 0.1.0"`):contentReference[oaicite:0]{index=0}. |
| `GET` | `/stock/{stock_symbol}` | Returns details about a specific stock. The path parameter `stock_symbol` must be provided (e.g., `AAPL`). |
| `POST` | `/stock/{stock_symbol}` | Records the purchase of a stock. It receives the stock symbol in the route and a JSON body with the quantity purchased. |
| `GET` | `/health` | Checks the application’s health, returning the status of subsystems such as cache and database:contentReference[oaicite:1]{index=1}. |

### Inputs

- **GET `/stock/{stock_symbol}`** – requires the path parameter `stock_symbol`, a string representing the stock ticker.
- **POST `/stock/{stock_symbol}`** – in addition to the path parameter `stock_symbol`, requires a JSON body with the following structure:
  ```json
  {
    "amount": 10
  }

  // The amount field (a number) indicates the number of shares to be purchased
  ```

- **GET `/health`** and **GET `/`** – do not require additional parameters.

### Outputs
- **GET `GET /`** – returns a string with the API version, such as "Manage Stocks API 0.1.0"
6dc725dbffa7.ngrok-free.app

- **GET `/stock/{stock_symbol}`** – returns a JSON object with various information about the requested stock. An example for AAPL includes:
    - status – indicates whether the request was successful ("OK").
    - purchased_amount and purchased_status – show whether a purchase has been recorded.
    - request_data – the date of the query.
    - company_code and company_name – the company’s code and name.
    - stock_values – an object with open, high, low and close (opening, highest, lowest and closing prices)
    - performance_data – an object with performance data over different time windows (five days, one month, three months, year‑to‑date, one year)
    - competitors – a list of competitors with name and market_cap (market capitalization value)

- **GET `POST /stock/{stock_symbol}`** – returns a JSON similar to GET /stock/{stock_symbol}. After the purchase, the fields purchased_amount and purchased_status reflect the recorded quantity and updated status. The specification notes that the route returns a 200 OK status code on success
6dc725dbffa7.ngrok-free.app

- **GET `GET /health`** – returns a JSON object with status (e.g., "ok"), a details object showing the status of subsystems (cache, database, etc.), and a request_id for tracking

### Example `curl` Requests

```bash
    # Get details about a stock
    ticker="AAPL"
    curl -X GET "https://6dc725dbffa7.ngrok-free.app/stock/$ticker" \
    -H "accept: application/json"

    # Record the purchase of a stock (for example, buy 10 shares)
    ticker="AAPL"
    curl -X POST "https://6dc725dbffa7.ngrok-free.app/stock/$ticker" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{"amount": 10}'

    # Check the health status of the application
    curl -X GET "https://6dc725dbffa7.ngrok-free.app/health" -H "accept: application/json"

    # Get the API version
    curl -X GET "https://6dc725dbffa7.ngrok-free.app/" -H "accept: application/json"
```

### Swagger
The API’s Swagger interface is available at http://localhost:8000/docs. There you can view all routes, parameters and test calls directly from the browser. The OpenAPI JSON file that defines the routes and models is available at http://localhost:8000/openapi.json

These resources become available after running the project locally.

## :building_construction: Architecture

This repository follows a layered architecture inspired by Clean Architecture, which separates responsibilities to facilitate testing, evolution, and maintenance. The code structure is located inside the app/ directory, organized into four main layers:

```
├── app/
│   ├── application/
│   │   └── use_cases/
│   │       ├── get_stock_details_use_case.py
│   │       └── register_stock_purchase_use_case.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── entity.py
│   │   │   ├── stock.py
│   │   │   └── stock_transaction.py
│   │   └── services/
│   │       └── get_last_market_day_service.py
│   ├── infra/
│   │   ├── database/
│   │   │   └── sqlalchemy_database_config.py
│   │   ├── repositories/
│   │   │   ├── models/
│   │   │   │   ├── sqlalchemy_stock_model.py
│   │   │   │   └── sqlalchemy_transaction_stock_model.py
│   │   │   ├── stock_repository.py
│   │   │   └── stock_transaction_repository.py
│   │   ├── gateways/
│   │   │   ├── stock_values_gateway.py
│   │   │   └── stock_web_scraping_gateway.py
│   │   ├── services/
│   │   │   ├── cache.py
│   │   │   └── logger.py
│   │   └── queries/
│   │       └── query.py
│   └── presentation/
│       └── http/
│           ├── app.py
│           ├── routes.py
│           ├── handlers/
│           │   ├── http_exception_handler.py
│           │   └── validation_exception_handler.py
│           └── middlewares/
│               └── loggin_middleware.py
├── migrations/                        # Alembic migration files
├── tests/                             # automated tests using pytest
├── .env.example                       # example of environment variables
├── Dockerfile                         # API image build configuration
├── docker-compose.yml                 # defines API, PostgreSQL, and Redis services
├── Makefile                           # install, run, and test shortcuts
├── pyproject.toml                     # Poetry dependencies and configuration
└── README.md
```

### Presentation Layer

The presentation layer exposes the HTTP API using FastAPI. The app/presentation/http/app.py file instantiates the FastAPI application, sets title, description, version, and metadata, applies middlewares (request logging, CORS), and registers exception handlers and routes. The routes are defined in app/presentation/http/routes.py and delegate the logic to use cases, keeping the outer layer free of business rules. FastAPI provides high performance, async/await support, and automatic Swagger/Redoc generation, simplifying testing and integration.

### Application Layer

This layer contains the use cases, responsible for orchestrating operations from the domain and infrastructure layers. Each class receives its dependencies via dependency injection (dependency inversion principle), enabling easy swapping of implementations. For example:
- **GetStockDetailsUseCase:** fetches the last market day, reads the stock record, retrieves quotes from Polygon (external gateway), scrapes performance and competitors data, and uses Redis to cache the response. The cache TTL (900 s) avoids redundant requests.
- **RegisterStockPurchaseUseCase:** stores a stock purchase. If the stock exists, it increases the balance; otherwise, it creates a new record, saves the transaction, and invalidates the cache. These classes are located in app/application/use_cases/ and are unaware of frameworks or infrastructure details; they operate only through interfaces.

### Domain Layer

This layer contains pure domain entities and business rules. A root entity (Entity) defines common fields like id, created_at, updated_at, and deleted_at. Domain entities such as Stock and StockTransaction extend this base and encapsulate behaviors (e.g., increment_balance). Domain services, such as get_last_market_day_service, also reside here and implement pure logic (e.g., calculating the last market day considering weekends).

### Infrastructure Layer

Provides concrete implementations for interfaces used by upper layers:
- **Database:** Uses asynchronous SQLAlchemy with PostgreSQL. The sqlalchemy_database_config.py module reads environment variables, creates the engine, and provides an async sessionmaker. Models (under app/infra/repositories/models/) map tables to entities.
- **Repositories:** Interfaces like StockRepository define methods like find_by_symbol, create, and update; the SqlalchemyStockRepository implementation performs queries and maps records to domain objects.
- **External Gateways:**
    - **PolygonStockValuesGateway** calls the Polygon API to retrieve stock open, high, low, and close prices.
    - **MarketWatchStockWebScrapingGateway** uses httpx and BeautifulSoup to extract company name, performance over different time windows, and a list of competitors from a finance site.
- **Cache:** RedisCache abstracts caching operations with Redis, allowing get, set, delete, and ping.
- **Health Queries:** SqlalchemyQuery.ping() executes a SELECT 1 to verify database availability and is used by the /health endpoint.

### Support and Tooling

- **Dependency Management:** The project uses Poetry, which integrates natively with pyproject.toml, creates and manages virtual environments, and locks dependencies.
- **Server:** make run uses uvicorn[standard], which includes uvloop and httptools for high performance and auto-reload. For containerized environments, a Dockerfile and docker-compose simplify running the API, database, and cache.
- **Linting and Formatting:** The project uses Ruff, a fast tool combining linting and formatting, configured via pyproject.toml and integrated with CI/CD.
- **Makefile:** Provides commands to install dependencies, run the application, apply migrations with Alembic, run tests (pytest), and generate code coverage.
- **Tests:** Tests are located in tests/, using pytest and pytest-asyncio. They simulate the application lifecycle using httpx.AsyncClient or FastAPI TestClient to test routes without starting the server.

## :bust_in_silhouette: Author:
Luiz Eduardo Campos da Silva</br>
LinkedIn: <a href="https://www.linkedin.com/in/luiz-campos">@luiz-campos</a></br>
Github: <a href="https://www.github.com/luizcampos331">@luizcampos331</a>

## :pencil: Licence
Copyright © 2025 <a href="https://www.github.com/luizcampos331">Luiz Campos</a></br>
This project is licensed under <a href="LICENSE">MIT</a>
