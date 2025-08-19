# Authentication and Survey Application

This is a Flask web application that provides user authentication (signup and login) and allows logged-in users to fill out a lab survey.

## Overview

The application consists of the following main features:

* **User Authentication:**
    * Signup: Allows new users to create an account.
    * Login: Allows existing users to log in to the system.
    * Logout: Allows logged-in users to securely log out.
* **Dashboard:** A protected page accessible after login, displaying a welcome message.
* **Lab Survey:** A form for users to provide feedback about lab sessions.
* **Database:** Utilizes MySQL to store user information and survey responses.

## Technologies Used

* Python
* Flask (web framework)
* MySQL (`mysql.connector`)
* Werkzeug (for password hashing)

## Setup Instructions

1.  **Clone the repository** (if you have one):
    ```bash
    git clone [your_repository_url]
    cd [your_project_directory]
    ```

2.  **Install dependencies:**
    ```bash
    pip install Flask mysql-connector-python Werkzeug
    ```

3.  **Set up the MySQL database:**
    * Ensure you have MySQL installed and running.
    * Create the `auth_survey_app` database. You can use the following SQL command:
        ```sql
        CREATE DATABASE auth_survey_app;
        ```
    * Create the `users` and `survey_responses` tables. The SQL commands for these are in the project files or as discussed previously.

4.  **Configure database connection:**
    * Open the `app.py` file.
    * Update the `get_db_connection()` function with your MySQL server details (host, user, password).

5.  **Run the Flask application:**
    ```bash
    cd [your_project_directory]
    set FLASK_APP=app.py
    flask run
    ```
    (On Linux/macOS, use `export FLASK_APP=app.py` instead of `set`).
    Alternatively, you can use:
    ```bash
    python app.py
    ```

6.  **Access the application:**
    * Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

* Navigate to `/signup` to create a new user account.
* Navigate to `/login` to log in with an existing account.
* Once logged in, you will be redirected to the `/dashboard`.
* From the dashboard, you can access the `/survey` page to fill out the lab survey.
* Use the "Logout" link to securely log out of the application.

## File Structure