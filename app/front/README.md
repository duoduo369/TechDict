brunch chaplin boilerplate
===

Summary
---

* brunch
* coffee
* chaplin
* bower

Depend on
---
* [npm](https://www.npmjs.org/)
* [brunch](http://brunch.io/)
* [bower](http://bower.io/)

Install
---

###npm
    sudo apt-get install npm
    for windows user, go nodejs web find windows installer, download and
    installer, npm will auto install

###cnpm
    accelerate npm
        for chinese user, npm is too slow, install cnpm to accelerate
        then when you need `npm install XXX` simple use `cnpm install XXX`

    npm install -g cnpm
    or
    sudo npm install -g cnpm

###brunch
    npm instal -g brunch
    or
    sudo npm instal -g brunch

###bower
    npm install -g bower
    or
    sudo npm install -g bower


Usage
---
1. git clone
2. cd project_path
3. npm install
4. brunch w --server

App Struct
---
    app
    ├── common
    │   ├── application.coffee
    │   ├── assets
    │   │   └── images
    │   ├── config.coffee
    │   ├── controllers
    │   │   └── base
    │   │       └── controller.coffee
    │   ├── mediator.coffee
    │   ├── mock.coffee
    │   ├── models
    │   │   └── base
    │   │       ├── collection.coffee
    │   │       └── model.coffee
    │   └── views
    │       ├── base
    │       │   ├── collection-view.coffee
    │       │   └── view.coffee
    │       └── styles
    │           └── application.styl
    ├── lib
    │   ├── utils.coffee
    │   └── view-helper.coffee
    └── tutorial
        ├── assets
        │   └── index.html
        ├── controllers
        │   └── home.coffee
        ├── initialize.coffee
        ├── models
        │   ├── item.coffee
        │   └── list.coffee
        ├── routes.coffee
        └── views
            ├── common
            │   ├── header-view.coffee
            │   ├── styles
            │   │   └── header.styl
            │   └── templates
            │       └── header.hbs
            └── home
                ├── home-view.coffee
                ├── item-view.coffee
                ├── list-view.coffee
                ├── styles
                │   ├── home.styl
                │   └── item.styl
                └── templates
                    ├── home.hbs
                    ├── item.hbs
                    └── list.hbs

###module struct

very folder under apps is a module, very model has below struct

    tutorial
    ├── assets
    │   └── index.html  # for html
    ├── controllers     # chaplin controllers
    │   └── home.coffee
    ├── initialize.coffee # html has require initialize, init Application
    ├── models          # chaplin models
    │   ├── item.coffee
    │   └── list.coffee
    ├── routes.coffee   # chaplin route
    └── views           # chaplin views, templates and styles and views folder
        ├── common
        │   ├── header-view.coffee
        │   ├── styles
        │   │   └── header.styl
        │   └── templates
        │       └── header.hbs
        └── home
            ├── home-view.coffee
            ├── item-view.coffee
            ├── list-view.coffee
            ├── styles
            │   ├── home.styl
            │   └── item.styl
            └── templates
                ├── home.hbs
                ├── item.hbs
                └── list.hbs
###common module
the bases will under in common, this module has reusable things
