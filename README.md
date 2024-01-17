# 🧠 NEAT Trading 🧠
## Introduction
## Set up
To build the docker image
``
docker run --name neat-trading -it -d neat-trading
docker exec -it neat-trading /bin/bash
``

To view the logs
``
tail -f cron_log.log
``
## Generate Training Data
``
python3.10 main.py generateData GBPUSD,EURGBP,EURUSD,USDJPY,USDCHF,AUDUSD,USDCAD,NZDUSD
``
## Train
``
python3.10 main.py train
``
## Improvements
