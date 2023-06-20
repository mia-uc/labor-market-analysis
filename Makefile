drop: 
	docker stop ${container}
	docker rm ${container}

build:
	docker build -t jobs_scrapers -f ./Dockerfile .

run_getonbrd:
	docker run --env-file=.docker.env --name getonboard jobs_scrapers python -m scrapers getonbrd ${flags}

run_laborum:
	docker run --env-file=.docker.env --name laborum jobs_scrapers python -m scrapers laborum ${flags}

run_working:
	docker run --env-file=.docker.env --name workingcl jobs_scrapers python -m scrapers workingcl ${flags}

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

update_and_run:
	git pull origin main
	docker stop ${container}
	docker rm ${container}	
	docker build -t jobs_scrapers -f ./Dockerfile .
	docker run --env-file=.docker.env --name ${container} jobs_scrapers python -m scrapers ${container} ${flags}	
