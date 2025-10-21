# Description 

Beer stock  managment used by a bar.  
This bar has several type of beers and beer counters, each one has its own stock.  
The clients (anonym users) can order and the staff (authenticated users) can manage their stock.  

# Tools

- Django Restful Framework API
- docker

# Installation
```
docker build -t brewery .
docker run -it --rm -p 8000:8000 brewery
```
# Testing the Brewery API

## Pre-created Users (Fixtures)

The following users are already created in the Docker container using fixtures:

| Username           | Password | Role          |
|-------------------|----------|---------------|
| `marta_staff`      | test     | Staff         |
| `marta_customer`   | test     | Customer      |
| `marta_superuser`  | test     | Superuser     |

---

## 1️⃣ Generate Tokens

1. Open a shell in the Docker container:

```bash
docker exec -it <container_name_or_id> python manage.py shell
```
In the Django shell, generate tokens for the users:

```bash
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Staff
staff = User.objects.get(username='marta_staff')
staff_token, _ = Token.objects.get_or_create(user=staff)
print("Staff token:", staff_token.key)

# Customer
customer = User.objects.get(username='marta_customer')
customer_token, _ = Token.objects.get_or_create(user=customer)
print("Customer token:", customer_token.key)

# Superuser
superuser = User.objects.get(username='marta_superuser')
superuser_token, _ = Token.objects.get_or_create(user=superuser)
print("Superuser token:", superuser_token.key)
```
Copy the printed tokens for use in API requests.

2. Customer Permissions

The customer user can access the following endpoints:

| Endpoint   | URL                  | Permission  |
|------------|--------------------|------------|
| References | `/api/references/`   | Read-only  |
| Bars       | `/api/bars/`         | Read-only  |
| Orders     | `/api/orders/`       | Write allowed |

**Example `curl` calls for customer:**

```bash
# List references
curl -s -H "Authorization: Token <customer_token>" http://localhost:8000/api/references/ | jq

# List bars
curl -s -H "Authorization: Token <customer_token>" http://localhost:8000/api/bars/ | jq

# List orders
curl -s -H "Authorization: Token <customer_token>" http://localhost:8000/api/orders/ | jq
Staff-only endpoints return 404 for customer users.
```
Staff-only endpoints return 404 for customer users.


3. Staff & Superuser Permissions

Staff and superuser users can access everything above, **plus**:

| Endpoint    | URL                   | Permission |
|------------|----------------------|-----------|
| Stocks      | `/api/stocks/`        | Staff only |
| Statistics  | `/api/statistics/`    | Staff only |

**Example `curl` calls for staff:**

```bash
# List stocks
curl -s -H "Authorization: Token <staff_token>" http://localhost:8000/api/stocks/ | jq

# View statistics
curl -s -H "Authorization: Token <staff_token>" http://localhost:8000/api/statistics/ | jq
```

**Example `curl` calls for superuser:**

```bash
# List stocks
curl -s -H "Authorization: Token <superuser_token>" http://localhost:8000/api/stocks/ | jq

# View statistics
curl -s -H "Authorization: Token <superuser_token>" http://localhost:8000/api/statistics/ | jq
```

4. Notes

- All requests must include the header:
```http
Authorization: Token <your_token_here>

```

- Use `jq` to pretty-print JSON in the terminal. Install via:

```bash
brew install jq
```
- Endpoints `/api/stocks/` and `/api/statistics/` are **restricted to staff and superuser**. Customers will receive **404 or permission denied**.

