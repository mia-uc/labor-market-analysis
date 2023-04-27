drop: 
	docker stop ${container}
	docker rm ${container}

build:
	docker build -t jobs_scrapers -f ./Dockerfile .

# run_getonbrd:
# 	docker run --env-file=.docker.env --name get_on_board get_on_board

# clean_getonbrd:
# 	docker stop get_on_board
# 	docker rm get_on_board

# run_laborum:
# 	docker build -t laborum -f ./src/scrapers/laborum/Dockerfile .
# 	docker run --env-file=.docker.env --name laborum laborum

# clean_laborum:
run: 
	docker run -d --env-file=.docker.env --name laborum jobs_scrapers python main.py laborum
	docker run -d --env-file=.docker.env --name getonboard jobs_scrapers python main.py getonboard
	docker run -d --env-file=.docker.env --name trabajando_cl jobs_scrapers python main.py trabajando-cl

run_laborum:
	docker run --env-file=.docker.env --name laborum jobs_scrapers python main.py laborum
	docker stop laborum
	docker rm laborum

run_getonbrd:
	docker run --env-file=.docker.env --name getonboard jobs_scrapers python main.py getonboard
	docker stop getonboard
	docker rm getonboard

run_trabajando_cl:
	docker run --env-file=.docker.env --name trabajando_cl jobs_scrapers python main.py trabajando-cl
	docker stop trabajando_cl
	docker rm trabajando_cl

update_trabajando_cl:
	docker run --env-file=.docker.env --name update_trabajando_cl jobs_scrapers python main.py update-trabajando-cl
	docker stop update_trabajando_cl
	docker rm update_trabajando_cl

migrate_mongo:
	docker run --env-file=.docker.env --name migrate_mongo jobs_scrapers python main.py mongo-migrate    
	docker stop migrate_mongo
	docker rm migrate_mongo    
