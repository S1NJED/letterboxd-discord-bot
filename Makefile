DB = "db"
PYTHON = python

create_db:
	@echo "Creating database"
	@sqlite3 database/$(DB).sqlite < database/create_db.sql
	@echo "Sucessfully created database"

create_db_dev:
	@echo "Creating database (dev)"
	@sqlite3 database/$(DB)_dev.sqlite < database/create_db.sql
	@echo "Sucessfully created database"


run:
	@clear
	@if [ ! -f database/$(DB).sqlite ]; then \
		make create_db; \
	fi
	@python src/bot.py --mode=prod

dev:
	@clear
	@if [ ! -f database/$(DB)_dev.sqlite ]; then \
		make create_db_dev; \
	fi
	@python src/bot.py --mode=dev

fclean:
	@rm database/*sqlite* log
	@rm -rf __pycache__
	@rm -rf src/__pycache__
	@rm -rf src/cogs/__pycache__
	@echo "Removed db and log and __pycache__"

update-deps:
	uv pip install -U -r requirements.txt
	uv pip freeze > requirements.txt