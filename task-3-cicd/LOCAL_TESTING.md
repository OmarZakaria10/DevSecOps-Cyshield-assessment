# Local Testing Cheat-Sheet — Task Manager API

All commands are run from the `task-3-cicd/` directory.

---

## 1. Start Everything

```bash
# Build the image and start both containers (postgres + app)
docker compose up --build

# Or run in the background (detached)
docker compose up --build -d
```

Once you see:
```
taskapi_app  |  * Running on http://0.0.0.0:5000
```
the API is ready.

---

## 2. Health Check

```bash
curl http://localhost:5000/health
# Expected: {"status":"ok"}
```

---

## 3. Create Tasks

```bash
# Create task 1
curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}' | python3 -m json.tool

# Create task 2
curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Read a book"}' | python3 -m json.tool

# Create task 3
curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix the pipeline"}' | python3 -m json.tool
```

---

## 4. List All Tasks

```bash
curl -s http://localhost:5000/api/tasks | python3 -m json.tool
```

---

## 5. Get a Single Task (replace 1 with actual id)

```bash
curl -s http://localhost:5000/api/tasks/1 | python3 -m json.tool
```

---

## 6. Update a Task

```bash
# Mark task 1 as done
curl -s -X PATCH http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}' | python3 -m json.tool

# Rename task 1
curl -s -X PATCH http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries AND cook dinner"}' | python3 -m json.tool
```

---

## 7. Delete a Task

```bash
# Delete task 1 (returns 204 No Content on success)
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" \
  -X DELETE http://localhost:5000/api/tasks/1

# Confirm it's gone (should return 404)
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" \
  http://localhost:5000/api/tasks/1
```

---

## 8. Error Cases (input validation)

```bash
# Missing title → 400
curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

# Blank title → 400
curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "   "}' | python3 -m json.tool

# Non-existent ID → 404
curl -s http://localhost:5000/api/tasks/99999 | python3 -m json.tool
```

---

## 9. Connect to the Database Directly

```bash
# Open a psql session inside the running DB container
docker compose exec db psql -U postgres -d taskdb

# Useful queries once inside psql:
# \dt                         -- list tables
# SELECT * FROM tasks;        -- see all tasks
# \q                          -- quit
```

---

## 10. View Live Logs

```bash
# Follow logs from both services
docker compose logs -f

# Follow only the app
docker compose logs -f app

# Follow only postgres
docker compose logs -f db
```

---

## 11. Run the Test Suite (pytest) Locally

```bash
# Install deps in a local venv first (one-time setup)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Run tests against the live Docker postgres (same DB the app uses)
DATABASE_URL="postgresql://postgres:localpassword@localhost:5433/taskdb" pytest -v

# Or run tests with the SQLite fallback (no Docker needed at all)
pytest -v
```

---

## 12. Stop & Clean Up

```bash
# Stop containers (keeps volumes / data)
docker compose down

# Stop AND delete the database volume (full reset)
docker compose down -v
```
