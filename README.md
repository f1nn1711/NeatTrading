# 🧠 Trading Helper 🧠
## Introduction
This project aims to help analyse a wide range of financial indicators and then provide alerts when possible forex position entries arrise. This application gets it data from Trading212's RESTful API however there are plans to incorporate other sources of information such as Yahoo Finance.
## Set up
To ensure intercompatabilty between development environments and to allow for easy deployment to container orchestration tools such as Kubernetes, this project has been developed within a docker container. To build and run the docker container:
``
docker build -t neat-trading
docker run --name neat-trading -it -d neat-trading
docker exec -it neat-trading /bin/bash
``
## Run the application
Once a bash command line has been opened within the container, run the following command to get the latest alerts for the specified forex pairs:
``
python3.10 main.py getDecisions EURGBP,NZDUSD,USDCHF,AUDUSD,USDCAD,USDJPY,EURUSD,GBPUSD
``
## Improvements
 - I would like to implement automatic trade exection to minimise the amount of interation needed to execute trades. Additionally this would improve the accuracy of the application as there would be reduced delay in between a signal being generated and a trade being executed.
 - I would like to add multiple sources of financial prices so that the users trading platform could be used.
 - I would like to add a web interface so that users can control the algorithm's parameters and forex pairs without access to the command line.
