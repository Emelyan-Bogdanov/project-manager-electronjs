# Project Manager

A desktop project management application built with **Electron.js** (frontend) and **Flask** (backend API with SQLite).

## Architecture

```
┌─────────────────────┐       HTTP        ┌──────────────────────┐
│   Electron.js App   │ ◄──────────────► │   Flask API Server   │
│  (Desktop UI)       │   localhost:5000  │   (REST + SQLite)   │
└─────────────────────┘                   └──────────────────────┘
```

- **Electron** renders HTML/Vue 2 pages in a native window
- **Flask** provides a REST API backed by SQLite (SQLAlchemy ORM)
- Communication is via `node-fetch` through Electron IPC bridge

## Quick Start

### Backend (Flask)

```bash
cd backend
pip install flask flask-sqlalchemy flask-cors
python run_flask_server.py
```

Server starts at `http://localhost:5000`.

### Frontend (Electron)

```bash
cd electronjs
npm install
npm start
```

### Login

The app starts on the login page. Use any credentials to sign in (the login endpoint on Flask is a stub — ready for real auth integration). Check **"Se souvenir de moi"** to persist the session across restarts.

## Features

### Authentication & Session
- Login / Signup pages with validation
- "Remember me" toggle — persists session to disk (`user-session.json`)
- Auto-login on restart if session is remembered
- Logout from sidebar clears session and redirects to login

### Dashboard
- 4 stat counters (Users, Projects, Tasks, Messages)
- Recent projects list with status indicators
- Recent activity feed
- Team overview with online/offline status
- "Nouveau projet" button

### Kanban Task Board
- 3 columns: À faire / En cours / Terminé
- Task cards with tags, description, deadline, avatars, comments, views
- Real-time search filtering by title, description, or tags
- Trier / Filtres / Vue toolbar buttons

### User Management
- Grid of user cards with avatars, names, locations, and skill tags
- Real-time search by name, location, or tags
- "Ajouter" user button

### User Profile
- Cover photo with avatar overlay
- Name, role, location display
- Bio section
- Skill tags (orange pills)
- Recent activity timeline

### Sidebar Navigation
- Company logo
- Menu: Dashboard, Tasks, Publications, Files, Users
- Project members section
- Logout button at bottom

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Login | `auth/login.html` | Authentication with remember me |
| Signup | `auth/sign.html` | Registration with validation |
| Dashboard | `dashboard.html` | Main hub with stats and overview |
| Tasks | `tasks.html` | Kanban board with search |
| All Users | `allUsers.html` | User grid with search |
| Profile | `profile.html` | User profile page |

## Vue Components

All components are Vue 2 global components located in `electronjs/src/assets/compos/`.

| Component | Description |
|-----------|-------------|
| `left-big-menu` | Full sidebar menu with navigation and logout |
| `side-menu-button` | Sidebar navigation link with icon, badge, and URL |
| `company-logo` | Logo display with orange circle and company name |
| `sidebar-section-header` | Sidebar section divider with optional + button |
| `sidebar-member-item` | Team member entry with avatar and time |
| `stat-card` | Dashboard metric card with icon and count |
| `project-card` | Kanban task card with full metadata |
| `project-list-item` | Compact project row for dashboard list |
| `activity-item` | Activity feed entry (avatar or icon mode) |
| `team-member-item` | Team member row with online status |
| `user-card-item` | User card for the users grid |
| `column-title` | Kanban column header with task count |
| `tag-compo` | Checkbox tag with count badge |

## Flask API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` or `/api/users` | List all users |
| GET | `/howmanyusers` | Get user count |
| GET | `/deleteuser/<id>` | Delete a user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` or `/api/tasks` | List all tasks |
| POST | `/addtask` | Create a task |
| GET | `/task/<id>` | Get task details |

### Workspaces
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces` or `/api/workspaces` | List all workspaces |
| POST | `/addworkspace` | Create a workspace |
| GET | `/workspace/<id>` | Get workspace details |
| POST | `/updateworkspace/<id>` | Update a workspace |
| GET | `/deleteworkspace/<id>` | Delete a workspace |

### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/messages/<workspace_id>/` | List messages for a workspace |

## Database Models

All models use SQLAlchemy ORM on **SQLite** (`test.db`).

- **User** — id, username, email, password
- **Workspace** — id, name, description, iconPath
- **Task** — id, title, tags, views, comments, deadline, authorId, images, priority, status
- **Comment** — id, text
- **Message** — id, text, authorId, workspaceId

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Desktop Shell | Electron 42 |
| UI Framework | Vue 2 (CDN) |
| Styling | Bootstrap 5 + Custom CSS |
| Icons | Bootstrap Icons |
| Font | Cairo |
| Backend | Flask (Python) |
| Database | SQLite + SQLAlchemy |
| Communication | node-fetch via IPC bridge |
| Session Storage | JSON file in `app.getPath('userData')` |
| Packaging | electron-builder (Windows NSIS) |
