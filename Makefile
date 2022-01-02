run-db:
	docker run --name mcullenm_dev_db -p 5423:5423 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mcullenmdev -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres