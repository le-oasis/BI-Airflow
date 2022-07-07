# Data Engineering for Beginners: Business Intelligence with Apache Airflow
What we are going to build next will be a small Airflow application in which we will automate various business tasks in an ETL pipeline.

## Project Requirements

* We have been booked by a retail store client which has a number of store outlets located at different locations.
* From the transactions happening in various stores, the company wants to get ‘daily profit reports’ on how its stores are performing in the market.
* As an input, we are given a raw CSV file containing the transaction data of all stores.

## Project Breakdown. 

The full in-depth, step-by step breadown of the project can be found on the [Meduim](https://medium.com/@le.oasis/data-engineering-for-beginners-business-intelligence-with-apache-airflow-a63e4dd50471) article I published. 

## Airflow Setup 

This project contains the following containers and thier environment variables:

* Postgres
    * Image: [postgres:5.7.27](https://hub.docker.com/_/postgres)
    * Database Port: 5432
    * POSTGRES_USER: airflow 
    * POSTGRES_PASSOWRD: airflow
    * References: https://hub.docker.com/_/postgres
    
* MySQL

    * Image: [postgres:13](https://hub.docker.com/_/mysql)
    * DB USER: root 
    * DB PASSWORD: root
    * References: https://hub.docker.com/_/mysql

* Airflow Webserver
    * Image: [puckel/docker-airflow:1.10.4](https://hub.docker.com/r/puckel/docker-airflow)

## Starting Services 


    $ docker-compose -f ./docker-compose-LocalExecutor.yml up -d

