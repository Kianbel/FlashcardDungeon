# Flashcard Dungeon

A flashcard study app with a dungeon-crawling RPG theme, built with Django for the IM2 course. Decks are dungeons, cards are monsters, and every card you remember earns XP, raises your rank and unlocks adventurer titles.

## Features

- **Accounts:** register, log in and out (POST-only logout), change username or password, delete account. Logging in honors the page you were trying to reach.
- **Bounty Board (dashboard):** every dungeon appears as a "Wanted" poster showing its card count, threat level (one level per 8 cards), bounty (cards x 15 XP) and a "Cleared" stamp once a run is completed.
- **Dungeons and cards:** create, edit and delete dungeons (decks) and their cards. Front = the monster (question), back = its weakness (answer).
- **Dungeon runs:** flip each card, then mark it **Strike** (remembered) or **Retreat** (forgot). Keyboard shortcuts: `Space` to reveal, `K` to strike, `F` to retreat.
- **Results and ranks:** each run ends with a results screen and a rank (S, A, B or C) based on recall percentage.
- **XP and levels:** 15 XP per remembered card, awarded when the run ends. The XP needed for the next level is `int(100 * level^1.5)`.
- **Titles:** titles unlock automatically at their required level and can be equipped from the Ledger (profile page).
- **Chronicle:** history of completed runs, with the dungeon each was fought in (uses a SQL JOIN via `select_related`).
- **Cursed Foes:** every card you have fled at least once (uses a SQL subquery).
- **Two visual themes:** a tavern theme (wood and parchment) and a dungeon theme (moss and stone) in a single stylesheet.

## Tech stack

- Python 3, Django 6.1.1
- PostgreSQL hosted on Supabase (via `psycopg` 3 and `dj-database-url`)
- `python-dotenv` for configuration
- Plain HTML templates, one CSS file, a little vanilla JavaScript (no frontend framework)

## Project structure

```
config/            Django settings and root URLs
apps/
  login/           Login and logout
  register/        Registration
  home/            Bounty Board dashboard, theme template tags
  profiles/        Profile (level, XP), titles, equip title
  user_settings/   Username, password, delete account
  dungeon/         Decks, cards, runs, results, chronicle, cursed foes
templates/         Base templates, per-app templates, partials
static/css/        base.css (both themes), records.css
```

## Getting started (local setup)

### Prerequisites

- Python 3 and Git
- A PostgreSQL database that accepts SSL connections (this project uses a Supabase project)

### Steps

1. Clone the repository:

   ```
   git clone https://github.com/Kianbel/FlashcardDungeon.git
   cd FlashcardDungeon
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv .venv
   source .venv/Scripts/activate      # Git Bash on Windows
   # .venv\Scripts\activate           # PowerShell / Command Prompt
   # source .venv/bin/activate        # macOS / Linux
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create your environment file by copying the example, then fill it in:

   ```
   cp .env.example .env
   ```

   | Variable       | Description                                                        |
   |----------------|--------------------------------------------------------------------|
   | `DATABASE_URL` | PostgreSQL connection string (Supabase session pooler URL)         |
   | `SECRET_KEY`   | Django secret key. Use a long random value                         |
   | `DEBUG`        | `True` for local development                                       |

   `.env` is gitignored. Never commit it.

5. Apply the migrations:

   ```
   python manage.py migrate
   ```

6. (Optional) Create an admin account:

   ```
   python manage.py createsuperuser
   ```

7. Start the development server and open http://127.0.0.1:8000/:

   ```
   python manage.py runserver
   ```

### Titles

Titles live in the `profiles_title` table, not in code. On a fresh database, add them in the Django admin at `/admin/` (a name, description and required level each). A title is granted automatically when a user's level reaches its required level and they open the Ledger or level up.

## How a run works

1. Open a dungeon and press **Descend into the Dungeon**.
2. Each card is shown front first. Reveal the weakness, then Strike or Retreat.
3. When no cards remain, the run ends: XP is awarded (15 per Strike), the profile levels up if the threshold is reached, and the results screen shows your rank.

## Main URLs

| Path                          | Page                              |
|-------------------------------|-----------------------------------|
| `/`                           | Bounty Board (dashboard)          |
| `/login/`, `/register/`       | Sign in, sign up                  |
| `/dungeon/forge/`             | Create a dungeon                  |
| `/dungeon/<id>/`              | Dungeon detail and bestiary       |
| `/dungeon/history/`           | Chronicle (completed runs)        |
| `/dungeon/cursed/`            | Cursed Foes                       |
| `/profiles/`                  | Ledger (profile and titles)       |
| `/user_settings/`             | Quarters (account settings)       |
| `/admin/`                     | Django admin                      |

## Known limitations

- Local development only. Production deployment is not configured (`ALLOWED_HOSTS` is empty, no static file serving setup).
- The database connection requires SSL (`ssl_require=True`), so a plain local PostgreSQL without SSL needs a settings change.
- The `dark_mode` and `email_notifications` fields exist in the `UserSettings` model but are not used by any screen.
- Titles cannot yet be bought with XP; they unlock by level only.

## Ideas for later

- XP shop for buying titles
- A "review only the cards I fled" run mode
- Spaced repetition scheduling
- Automated tests and deployment configuration

## Author

Kianbel, IM2 Final Project