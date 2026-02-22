# Person Management Application

A console-based **Python MVC application** for managing persons and their addresses.  
The application uses a **MySQL database** for persistent storage and follows a clean **Model-View-Controller architecture**.

---

## Features

- CRUD operations and list persons
- Address management with foreign key relationship
- Input validation (email, date, numbers, etc.)
- Strong typing (`int`, `date`)
- Partial updates via DTO pattern
- Automatic database and table setup
- MySQL integration

---

## Technologies Used

- Python 3.10+
- MySQL Server 8+
- mysql-connector-python
- python-dotenv


---

# Prerequisites

Before running the application, make sure you have:

- Python 3.10 or higher installed
- MySQL Server installed and running

---

# Installation Guide

Follow these steps to run the application locally.

---

## 1. Clone the Repository

```bash
git clone
cd person-management
```

---

## 2. Install MySQL Server

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### macOS (Homebrew)

```bash
brew install mysql
brew services start mysql
```

### Windows
1. Download MySQL Installer from: https://dev.mysql.com/downloads/mysql/
2. Install MySQL Server
3. Set a root password
4. Ensure the MySQL service is running

---

## 3. Create a MySQL User (Recommended)

Login to MySQL:

```bash
mysql -u root -p
```

~~~~sql
CREATE USER 'person_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON *.* TO 'person_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
~~~~

---

## 4. Configure Environment Variables

Create a .env file in the project root directory:

```bash
touch .env
```
### Important
- Add your .env file to .gitignore.
- Do NOT commit your .env file.
- The repository contains .env.example as a template

Add your database credentials:

```env
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASS=your_db_password
```

---

## 5. Create a Virtual Environment (Recommended)

### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 6. Install Python Dependencies

If a requirements.txt file exists:

```bash
pip install -r requirements.txt
```

Otherwise install manually:

```bash
pip install mysql-connector-python python-dotenv
```

## 7. Run the Aplication

On first startup the application will:
- Create the database (if not existing)
- Create required tables
- Connect using your .env configuration

---

## Database Information
- Database name: person_management_db
- birth_date is stored as SQL DATE
- Dates are displayed on console in format: DD.MM.YYYY
- Foreign key constraints:
    - person.address_id -> address.id
    - `ON DELETE CASCADE`
    - `ON UPDATE CASCADE`

 ---

 ## Connecting with MySQL Workbench

 You can inspect the database visually:
 1. Open MySQL Workbench
 2. Create a new connection
 3. Use the same credentials from your .env
 4. Open schema person_management_db
 5. Run:
 ~~~~sql
SELECT * FROM person;
SELECT * FROM address;
~~~~

---

## Architecture

This project follows the MVC-pattern:
- **Model:** Business logic & data handling
- **View:** Console interaction & formatting
- **Controller:** Application flow & orchestration
- **DTOs:** Partial updates using Optional fields
- **DB Layer:** Centralized connection handling

---

## Security Notes

- Never commit .env
- Use a dedicated MySQL user (not root)
- Restrict privileges in production environments
