# Django-Command-Line-Chatbot-Application

## Introduction

The purpose of this repository is to showcase a Django CLI Application Using OPEN AI To Make A Simple Chatbot Interacting With Customers, Logging Their Chat, Help Him To Solve His Problem and Giving Him A Summary About his Problem and The Solutions.

## Installation

First you need to install this requirements
```sh
python -m pip install -r requirements.txt
```
Second You Need To Create Your .env with the path django_chatbot/chatbot/management/commands/.env
And Add your OPENAI_API_KEY Which you can get via https://platform.openai.com/api-keys


## To Run Django CLI
First Clone This Repo
```sh
cd django_chatbot
python manage.py  chatbot
```

## Overview of the files
chatbot/models.py Contain The Database tables that will be created in mysql db and these Tables Are

!(models_erd.png)


