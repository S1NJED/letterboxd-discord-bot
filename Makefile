DB = "db.sqlite"
PYTHON = python

db:
	@echo "Creating database"
	@sqlite3 $(DB) < create_db.sql
	@echo "Sucessfully created database"

test:
	clear
	@$(PYTHON) test.py