drop: 
	docker stop jobs_scrapers
	docker rm jobs_scrapers

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


update_trabajando_cl:
	docker run --env-file=.docker.env --name get_on_board jobs_scrapers python main.py update_trabajando_cl