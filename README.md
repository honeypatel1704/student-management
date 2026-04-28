# Student Management System (FastAPI)

Production-style, modular FastAPI backend for student management with authentication, role-based authorization, validation, pagination, logging, agent hooks, and PostgreSQL persistence.

## What Is Included

- FastAPI + PostgreSQL architecture
- JWT authentication (`/api/v1/auth/login`)
- Role-based access control (`admin`, `user`, `agent`)
- Full student CRUD API
- Pagination + filtering
- Strong request validation via Pydantic
- Central logging and global exception handling
- Agent query + event hook endpoints

## Project Structure

```text
main.py
requirements.txt
README.md
app/
	api/
		v1/
			endpoints/
				auth.py
				students.py
				health.py
				agents.py
			router.py
	core/
		config.py
		security.py
		logging_config.py
	test.py
	.env
	alembic.ini
	alembic/
		env.py
		README
		script.py.mako
		versions/
	db/
		config/
			app_config.py
		database/
			schema/
				db.py
```powershell
			todo.py
3. Configure environment variables (optional but recommended)
			helper.py
			app.py
		api/
		core/
		db/
		dependencies/
		schemas/
		services/

```powershell
$env:POSTGRES_DSN = "postgresql+psycopg2://postgres:postgres@localhost:5432/student_db"
$env:JWT_SECRET_KEY = "replace-with-strong-secret"
$env:BOOTSTRAP_ADMIN_EMAIL = "admin@student.local"
$env:BOOTSTRAP_ADMIN_PASSWORD = "Admin@123"
```

4. Run server

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. Open docs

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Default Bootstrap Admin

On first run, a default admin user is auto-created from config.

- Email: `admin@student.local`
- Password: `Admin@123`

Change these values in environment variables before production usage.

## API Overview

- `GET /api/v1/health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/users` (admin only)
- `POST /api/v1/students`
- `GET /api/v1/students`
- `GET /api/v1/students/{enrollment_number}`
- `PUT /api/v1/students/{enrollment_number}`
- `DELETE /api/v1/students/{enrollment_number}` (admin only)
- `POST /api/v1/agent/query` (admin/agent)
- `POST /api/v1/agent/hooks/event` (admin/agent)

## Notes

- Old Flask files/templates were removed as part of migration.
- Enrollment number remains unique and immutable once created.
- Date fields use ISO format (`YYYY-MM-DD`).