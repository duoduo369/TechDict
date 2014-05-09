Application   = require 'common/application'
config   = require 'common/config'
routes = require './routes'


$ ->
  new Application
    routes: routes
    controllerSuffix: config.controllerSuffix
    controllerPath: 'search/controllers/'
