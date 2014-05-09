Controller = require 'common/controllers/base/controller'
ListView = require 'search/views/home/list-view'
HeaderView = require 'search/views/common/header-view'
HomeView = require 'search/views/home/home-view'

module.exports = class HomeController extends Controller

  beforeAction: ->
    @reuse 'home', HomeView
    @reuse 'header', HeaderView, region: 'header'

  index: ->
    new ListView
      region: 'container'
