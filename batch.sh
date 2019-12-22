docker build -t mizuno .
docker stop mizuno
docker rm mizuno
docker run --name mizuno -it -p 5001:5000 mizuno
