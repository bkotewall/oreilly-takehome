#docker login
docker build --no-cache -t oreilly-takehome_flaskapp  .
#docker tag oreilly-takehome_flaskapp:latest  bkotewall/oreilly-takehome_flaskapp:latest
#docker push bkotewall/oreilly-takehome_flaskapp:latest
docker-compose up
