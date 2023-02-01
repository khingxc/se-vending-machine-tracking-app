# Vending Machine Tracking Application

## Functionalities

* Viewing all created machines' infos
* Viewing specific machine's info
* Creating new machine
* Editing existed machine's info
* Deleting existed machine
* Viewing all items in specific machine
* Adding new product to existed machine
* Deleting product from specific machine
* Editing product from specific machine

## Set Up

* Running docker-compose: ```docker compose up -d```
* Running python file: ```python3 app.py```
  * Remark: please check that you are currently on the right directory

## Close The Project

* Running ```docker compose down``` / Exit via Docker Desktop
* Executing the running ```app.py```

## Testing

* Postman

## Available APIs

Remark: <vending_machine_id> refers to the id in the form of integer ex: http://127.0.0.1:5000/machine/0/info

### APIs related to Vending Machine

* http://127.0.0.1:5000/machine : To view all machines
* http://127.0.0.1:5000/machine/create : To create machine
  * Input Requirement(s): Location (string)
* http://127.0.0.1:5000/machine/<vending_machine_id>/info : To get chosen machine's information
* http://127.0.0.1:5000/machine/<vending_machine_id>/edit : To edit chosen machine's information
  * Input Requirement(s): Location (string)
* http://127.0.0.1:5000/machine/<vending_machine_id>/delete : To delete machine

### APIs related to Items inside Vending Machine

* http://127.0.0.1:5000/machine/<vending_machine_id>/item : To view all items in chosen machine
* http://127.0.0.1:5000/machine/<vending_machine_id>/add-item : To add item and amount to chosen machine
  * Input Requirement(s): Product (string), Amount (integer)
* http://127.0.0.1:5000/machine/machine/<vending_machine_id>/edit-item : To edit item in chosen machine
  * Input Requirement(s): Product (string), Amount (integer)
* http://127.0.0.1:5000/machine/<vending_machine_id>/delete-item : To delete chosen item in chosen machine
  * Input Requirement(s): Product (string)

## Author

* Khwanchanok Chaichanayothinwatchara 6280164
