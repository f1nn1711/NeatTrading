docker build -t neat-trading .
docker rm -f neat-trading
docker run --name neat-trading -it -d neat-trading
docker exec -it neat-trading /bin/bash