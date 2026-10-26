# GameVault

GameVault is a Django web application for managing a personal video game collection. It allows users to organize games by genre and platform, track their progress, record play sessions, and write reviews.

## Features

- **Dashboard:** View collection statistics, recently added games, recent reviews, and play sessions.
- **Game library:** Add, view, edit, and delete games.
- **Search and filtering:** Search games and filter by status, genre, and platform.
- **Sorting:** Sort games by title, release date, and date added.
- **Genres and platforms:** Organize games using reusable genre and platform records.
- **Reviews:** Create, view, edit, and delete game reviews with ratings from 1 to 10.
- **Play history:** Record, view, edit, and delete play sessions, including dates, duration, and notes.
- **Playtime formatting:** Display playtime in hours and minutes.
- **Form validation:** Validate user input and display helpful error messages.
- **Responsive interface:** Dark-themed interface built with Bootstrap 5.
- **Custom error page:** A branded 404 page for unavailable routes.

## Technology Stack

- Python
- Django
- PostgreSQL
- HTML
- CSS
- Bootstrap 5

## Requirements

- Python 3.14 or a compatible Python version supported by the installed Django release
- PostgreSQL
- Git

## Installation and Setup

The following instructions use Windows PowerShell.

### 1. Clone the repository

```powershell
git clone https://github.com/skanchev03/gamevault.git
cd gamevault
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current terminal session, you can run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Make sure PostgreSQL is running. Connect using your PostgreSQL username, then create the database:

```sql
CREATE DATABASE gamevault;
```

If the database already exists, skip this step.

### 5. Configure environment variables

Copy the example environment file to create your local configuration:

```powershell
Copy-Item .env.example .env
```

Open `.env` in your editor and update the database credentials to match your local PostgreSQL setup:

```dotenv
DB_NAME=gamevault
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

Replace `your_password_here` with your PostgreSQL password. If your PostgreSQL username differs from `postgres`, update `DB_USER` as well.

Keep `.env` private. It contains local configuration and must not be committed to Git.

### 6. Apply database migrations

```powershell
python manage.py migrate
```

### 7. Run the development server

```powershell
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## Project Structure

```text
gamevault/
├── activity/          # Reviews, play sessions, forms, and template tags
├── config/            # Django settings and root URL configuration
├── core/              # Dashboard and custom error page
├── library/           # Games, genres, platforms, and forms
├── static/            # CSS and other static assets
├── templates/         # HTML templates and reusable partials
├── .env.example       # Example environment configuration
├── .gitignore
├── manage.py
└── requirements.txt
```

## Database Models

GameVault uses five primary database models:

- **Game:** Stores game information, including title, developer, release date, status, description, and cover image URL.
- **Genre:** Categorizes games by genre.
- **Platform:** Represents the platforms on which games can be played.
- **Review:** Stores a game's rating and written review.
- **PlaySession:** Records the date and duration of a gaming session, along with optional notes.

### Model Relationships

- A game can belong to multiple genres.
- A game can be associated with multiple platforms.
- A game can have multiple reviews.
- A game can have multiple play sessions.

The relationships are implemented using Django's many-to-many and foreign-key fields.

## Validation and Data Integrity

The application uses Django ModelForms to validate submitted data.

Examples include:

- Required game and review fields.
- Review ratings restricted to a range of 1–10.
- Minimum review text length.
- Positive play-session duration.
- Prevention of future-dated play sessions.
- Validation of genre and platform names.

Existing reviews cannot be reassigned to a different game when edited.

## Development and Deployment Notes

GameVault is configured for local development with PostgreSQL and Django's development server.

Before deploying to production:

- Set `DEBUG = False`.
- Configure `ALLOWED_HOSTS` for the deployment domain.
- Use secure environment variables for database credentials and other secrets.
- Configure production-ready static file serving and HTTPS.

## License

No license has been specified yet.
