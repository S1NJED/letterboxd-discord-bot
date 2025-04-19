DB = "db.sqlite"

db:
	@echo "Creating database"
	@sqlite3 $(DB) < create_db.sql
	@echo "Sucessfully created database"