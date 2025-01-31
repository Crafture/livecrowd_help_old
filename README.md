# Livecrowd FAQ
Created by Tony Kyriakidis and Nouh Lahouel 
___

_For Markup Cheatsheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet_

# Table of Contents 

[Starting Virtual Environment](#markdown-header-Starting-the-Virtual-Environment)

[Starting Django](#markdown-header-Starting-Django)

[To-Do's](#markdown-header-to-do)

[Future Features](#markdown-header-future-features)


---

## Starting the Virtual Environment ##

First you need to go to your projects root folder and then activate the environment with the source command.

```shell
cd ~/<PATH TO YOUR LOCAL LIVECROWD-FAQ FOLDER>

source livecrowdFAQenv/bin/activate
```

---

## Starting Django ##

NOTE: Make sure you have started your virtualenvironment!
```python
cd ~/<PATH TO YOUR LOCAL LIVECROWD-FAQ FOLDER>/app/

python manage.py runserver
```


## Frontend templating ##

* HTML templates : Go to `app/templates/` to edit
* CSS & JS development : For the first time -> Open commandline and navigate to `app/static/faq` and run: `npm install`
* Every time you want to develop the frontend navigate to: `app/static/faq` and run `gulp watch`. Make changes in the development folder, by saving the files it will be compiled and merged to JS or CSS folder.


---

## To-do ##

* Create config files for local, production and other settings.
* intergrate postgresql and create database

---
## Future Features ##

* Excel intergration
* Create a Messaging API ( [Franz](https://github.com/meetfranz/plugins/tree/master/docs) & [Rambox](http://rambox.pro/) )