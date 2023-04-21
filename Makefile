run_getonbrd:
	docker build -t get_on_board ./dockerfiles/getonboard
	docker run --env-file=.docker.env --name get_on_board get_on_board