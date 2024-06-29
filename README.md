# Description 

Beer stock  managment used by a bar.  
This bar has several type of beers and it has more beer counter, each one has their own stock.  
The clients (anonym users) can order and the staff (authenticated users) can manage their stock.  

# Tools

- Django Resftul API
- docker

# Installation
```
docker build -t brewery .
docker run -it --rm -p 8000:8000 brewery
```
Accounts to test the app:   
- username: marta_staff, pw: test   
- username: marta_customer, pw: test   
- username: marta_superuser, pw: test   