run_getonbrd:
	docker build -t get_on_board -f ./dockerfiles/getonboard/dockerfile .
	docker run --env-file=.docker.env --name get_on_board get_on_board