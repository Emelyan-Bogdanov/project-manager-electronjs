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
- Communication is via `fetch` through Electron IPC bridge

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

The app starts on the login page. Create an account via the signup page or use existing credentials. Check **"Se souvenir de moi"** to persist the session across restarts.

## Features

### Authentication & Session
- Login / Signup pages with validation
- Multi-step registration (profile setup: name, avatar, location, skills)
- "Remember me" toggle — persists session to disk (`user-session.json`)
- Auto-login on restart if session is remembered
- Logout from sidebar clears session and redirects to login
- Real backend login with credential verification

### Dashboard
- 4 stat counters (Users, Projects, Tasks, Files)
- Recent projects list with status indicators
- Recent activity feed — clickable items open task detail in a slide-in panel
- Team overview with online/offline status and avatar initials
- "Nouveau projet" button with modal form

### Kanban Task Board
- 3 columns: À faire / En cours / Terminé
- Task cards with tags, description (plain-text preview), deadline, views, comments, author avatars
- Real-time search filtering by title, description, or tags
- Filter by tag and user
- Sort / Filters / View toolbar buttons
- Create tasks with rich text editor (bold, italic, underline)
- Task type selector (basic / advanced)
- File uploads and image uploads with base64 encoding
- URL field for external links

### Task Detail & Inline Editor
- Slide-in task detail panel (from dashboard activity or tasks board)
- Medium-like block editor when viewing your own task:
  - **Header blocks** — contenteditable headings
  - **Text blocks** — rich text with floating toolbar (bold, italic, underline)
  - **Image blocks** — images with captions/titles, uploaded via file picker with prompt for title
  - **"+" button** between blocks to insert new headers, text, or images
  - Block delete on hover
- Read-only mode for tasks owned by other users
- Save button persists description as structured JSON

### User Management
- Grid of user cards with avatars, names, locations, and skill tags
- Avatar placeholder with initials when no image
- Real-time search by name, location, or tags
- "Ajouter" user button with modal form

### User Profile
- Cover photo with avatar overlay
- View: name, username, email, location, skill tags
- **Edit mode** (own profile only):
  - Edit name, username, email, location
  - Add/remove skill tags (comma-separated input with tag pills)
  - Upload avatar photo (click camera icon on avatar)
  - Save button calls the PATCH API

### Sidebar Navigation
- Company logo
- Menu: Dashboard, Tasks, Publications, Files, Users, Profile
- Project members section with avatars
- Logout button at bottom

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Login | `auth/login.html` | Authentication with remember me |
| Signup | `auth/sign.html` | Multi-step registration with profile setup |
| Dashboard | `dashboard.html` | Main hub with stats, recent projects, activity feed, team |
| Tasks | `tasks.html` | Kanban board with search, filters, and create modal |
| Task Detail | `task.html` | Full task detail with block editor (Medium-like) |
| All Users | `allUsers.html` | User grid with search |
| Profile | `profile.html` | User profile with view/edit mode |
| Files | `files.html` | File management |

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
| `activity-item` | Activity feed entry (avatar or icon mode, clickable) |
| `team-member-item` | Team member row with online status |
| `user-card-item` | User card for the users grid |
| `column-title` | Kanban column header with task count |
| `tag-compo` | Checkbox tag with count badge |
| `task-slide-panel` | Slide-in task detail panel with Medium-like block editor |

## Flask API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` or `/api/users` | List all users |
| GET | `/howmanyusers` | Get user count |
| POST | `/api/users` | Create a new user |
| PATCH | `/api/users/<id>` | Update user (name, username, email, avatar, tags, location) |
| GET | `/deleteuser/<id>` | Delete a user |
| POST | `/api/login` | Authenticate user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` or `/api/tasks` | List all tasks |
| POST | `/addtask` | Create a task (supports taskType, urls, images, files) |
| GET | `/task/<id>` | Get task details with author info |
| PATCH | `/task/<id>` | Update task fields (description, title, status, etc.) |

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

### User
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Display name |
| username | String | Unique login name |
| email | String | Unique email |
| password | String | Login password |
| avatar | Text | Avatar URL or base64 data |
| tags | Text | JSON array of skill tags |
| location | String | User location |

### Workspace
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Unique workspace name |
| description | Text | Workspace description |
| iconPath | String | Icon path |

### Task
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Task title |
| taskType | String | "basic" or "advanced" |
| tags | String | JSON array of tags |
| description | Text | HTML or JSON block array |
| urls | Text | JSON array of URLs |
| views | Integer | View count |
| comments | Integer | Comment count |
| deadline | String | Task deadline |
| authorId | Integer | Foreign key to User |
| images | Text | JSON array of images |
| files | Text | JSON array of files |
| priority | Integer | 1=Low, 2=Medium, 3=High |
| status | String | todo, in_progress, done |

### Comment / Message
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| text | Text | Content |
| authorId | Integer | (messages) Foreign key to User |
| workspaceId | Integer | (messages) Foreign key to Workspace |

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
| Communication | fetch via IPC bridge |
| Session Storage | JSON file in `app.getPath('userData')` |
| Packaging | electron-builder (Windows NSIS) |
