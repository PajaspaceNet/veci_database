# veci_database
A simple Flask + PostgreSQL CRUD app with dynamic forms and a mini relational schema.”

## Details

A simple CRUD demo app for managing your personal stuff using Flask, PostgreSQL, and Pandas.  
Includes dynamic form logic — for example, if an item is marked as porcelain, an extra form section appears to fill in porcelain-specific details.

## Features

- ✅ Flask backend
- ✅ PostgreSQL database
- ✅ Pandas for data manipulation
- ✅ Dynamic conditional forms (checkbox logic)
- ✅ Relational structure (multiple linked tables)
- ✅ Basic CRUD operations: Create, Read, Delete

## How to run

1. **Clone this repo**
   ```bash
   git clone https://github.com/yourusername/veci.git
   cd veci
   ```
2.  #### Set up your PostgreSQL database

    Create a new PostgreSQL database.

    Run the SQL script schema.sql to create tables.
3. #### Install Python dependencies
4. 
   ```bash
   pip install -r requirements.txt
   ```
4. #### Set up conection to your db
 
```python
db_config = {
    "host": "localhost",
    "database": "veci_db",
    "user": "yourusername",
    "password": "yourpassword",
    "port": 5432
}
 ```
5. #### Run 

```bash
   python app.py
```

6. #### open in your browser 
 http://localhost:5009 

7. #### Enjoy
8. ## SEE SCREENSHOTS
#### CRUD table possibilities
<img width="1012" height="538" alt="ukazka_CRUD a vystupu" src="https://github.com/user-attachments/assets/cec5b28a-e496-41c7-955d-87e5ee307407" />

*******************************************************************************************************************
*******************************************************************************************************************

#### preview of dynamic table , you choose porcelan 

<img width="753" height="320" alt="ukazka dynamicke tabulky" src="https://github.com/user-attachments/assets/e477bb04-631c-4a28-a58d-024218848f7b" />





Happy Coding 


