run_getonbrd:
	docker build -t get_on_board -f ./src/scrapers/getonboard/Dockerfile .
	docker run --env-file=.docker.env --name get_on_board get_on_board

clean_getonbrd:
	docker stop get_on_board
	docker rm get_on_board

run_laborum:
	docker build -t laborum -f ./src/scrapers/laborum/Dockerfile .
	docker run --env-file=.docker.env --name laborum laborum

clean_laborum:
	docker stop laborum
	docker rm laborum