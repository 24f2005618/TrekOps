# TrekOps - Trekking Management Application

TrekOps is a modern, comprehensive multi-role trekking booking and management platform designed to streamline trekking operations. It features three custom user roles: Admin, Staff, and Trekker. The application features booking workflows, interactive route tracking, asynchronous tasks for reminder emails, monthly reporting, and CSV history exports.

---

## 🚀 Tech Stack

### Frontend
- **Framework:** [Vue 3](https://vuejs.org/) (Composition API)
- **Routing & State:** [Vue Router](https://router.vuejs.org/) & [Vuex](https://vuex.vuejs.org/)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **UI & Styling:** [Bootstrap 5](https://getbootstrap.com/) & Bootstrap Icons

### Backend
- **Framework:** [Flask](https://flask.palletsprojects.com/) (Python 3)
- **Database:** SQLite (via [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/))
- **Authentication & Security:** [Flask-Security-Too](https://flask-security-too.readthedocs.io/)
- **Caching:** Redis Cache (via [Flask-Caching](https://flask-caching.readthedocs.io/))
- **Email Notifications:** [Flask-Mail](https://pythonhosted.org/Flask-Mail/)

### Task Queue & Scheduler
- **Asynchronous Processing:** [Celery](https://docs.celeryq.dev/)
- **Message Broker & Result Backend:** [Redis](https://redis.io/)

---

## 🛠️ Key Features

### 👤 Role-based Dashboards
1. **Admin Dashboard:**
   - Manage staff members, trekkers, and trekking routes.
   - Create, edit, and schedule treks.
   - Monitor and review bookings.
2. **Staff Dashboard:**
   - View assigned treks and schedule details.
   - Access and download participant lists for assigned treks.
   - Edit staff profile and security settings.
3. **Trekker Dashboard:**
   - Browse and search available treks.
   - Book treks and manage current bookings.
   - View trek history and request CSV report exports of their booking history.
   - Manage trekker profile.

### ⏱️ Asynchronous & Scheduled Tasks
- **Upcoming Trek Reminders:** Automatically runs daily at 21:00 (Asia/Kolkata timezone) to email tomorrow's trek details to registered participants and assigned staff.
- **Monthly Operational Report:** Automatically runs on the 1st of every month at 08:00 to generate and email a PDF/HTML report of previous month's treks, total participants, active staff, and popular routes to the administrator.
- **On-Demand Exports:** Generates and exports trekker booking history to CSV format asynchronously.

---

## 📂 Project Structure

```text
TrekOps/
├── backend/                  # Flask application source
│   ├── dep/                  # Core modules (Models, Views, Celery Tasks)
│   │   ├── models.py         # SQLAlchemy schemas for Trek, Route, Bookings, etc.
│   │   ├── tasks.py          # Celery background tasks
│   │   └── views.py          # Blueprint API endpoints
│   ├── templates/            # HTML/email templates (e.g., monthly report)
│   ├── app.py                # App entrypoint and Flask-Security initialization
│   ├── config.py             # Configuration (db URI, mail, redis, celery beat schedule)
│   ├── extensions.py         # Shared instances (Mail, Cache)
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # Vue 3 SPA source
│   ├── src/
│   │   ├── components/       # Shared UI components
│   │   ├── router/           # Vue Router navigation guards and path maps
│   │   ├── store/            # Vuex state management (auth, user details)
│   │   ├── views/            # Screen views (Home, Auth, Admin, Staff, Trekker)
│   │   ├── App.vue           # Root component
│   │   └── main.js           # JS initialization
│   ├── index.html            # SPA template
│   ├── package.json          # Node dependencies and build scripts
│   └── vite.config.js        # Vite configurations
│
└── .gitignore                # Global git ignore configuration
```

---

## ⚙️ Installation & Setup

### Prerequisites
Make sure you have the following installed on your system:
- **Python 3.8+**
- **Node.js 16+** & **npm**
- **Redis Server**

---

### 1. Run Redis Server
Start the Redis server, which is required for Celery queuing and Flask caching:
```bash
redis-server
```

---

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask development server:
   ```bash
   python app.py
   ```
   *The backend server will run at `http://127.0.0.1:5000`.*
   *Note: On first run, the SQLite database `model.db` will be initialized automatically in the `instance/` folder and pre-populated with default roles (`admin`, `staff`, `trekker`) and an administrator account.*

#### Start Celery Worker & Beat
To handle asynchronous events, open two separate terminal sessions with the virtual environment activated:
- **Start Celery Worker:**
  ```bash
  celery -A app.celery worker --loglevel=info
  ```
- **Start Celery Beat Scheduler:**
  ```bash
  celery -A app.celery beat --loglevel=info
  ```

---

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend dev server will typically run at `http://localhost:5173`.*

---

