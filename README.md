# URL Shortener

This project implements a simple RESTful API for a URL shortening service. It allows users to shorten long URLs, retrieve the original URL from a short URL, update existing short URLs, delete short URLs, and view statistics about how many times a short URL has been accessed.

## Features

- **Create Short URL**: Generate a short URL for a long URL.
- **Retrieve Original URL**: Retrieve the original long URL using the short URL.
- **Update Short URL**: Update an existing short URL with a new long URL.
- **Delete Short URL**: Delete an existing short URL.
- **URL Statistics**: View statistics like the number of times a short URL has been accessed.

## API Endpoints

### 1. Create Short URL

**POST** `/shorten`

- Request body should contain the long URL to shorten.
- The response will return a `201 Created` status code with the newly created short URL.

### 2. Retrieve Original URL

**GET** `/shorten/{short_code}`

- This endpoint retrieves the original long URL using the short URL's code.
- If the short URL exists, it returns the original URL. Otherwise, it returns a `404 Not Found` error.

### 3. Update Short URL

**PUT** `/shorten/{short_code}`

- Update an existing short URL with a new long URL.
- If the short URL exists, it returns a `200 OK` status code with the updated short URL. If not, it returns a `404 Not Found` error.

### 4. Delete Short URL

**DELETE** `/shorten/{short_code}`

- This endpoint deletes an existing short URL.
- If successful, it returns a `204 No Content` status code. If the short URL does not exist, it returns a `404 Not Found` error.

### 5. Get URL Statistics

**GET** `/shorten/{short_code}/stats`

- This endpoint provides statistics for a short URL, including the number of times it has been accessed.
- If the short URL exists, it returns the statistics. Otherwise, it returns a `404 Not Found` error.

---

## Tech Stack

- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database interactions
- **Microsoft SQL Server**: Database for storing URLs
- **PyODBC**: SQL Server database connector for Python

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/url-shortening-api.git
    cd url-shortening-api
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your database (using Microsoft SQL Server):
    - Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database credentials.

4. Run the application:
    ```bash
    python app.py
    ```

The application will start running on `http://127.0.0.1:5000`.

---

