Controller = require 'common/controllers/base/controller'
HeaderView = require 'search/views/common/header-view'
HomeView = require 'search/views/home/home-view'
IndexView = require 'search/views/index/index-view'
SearchView = require 'search/views/index/search-view'

module.exports = class HomeController extends Controller

  beforeAction: ->
    @reuse 'home', HomeView
    @reuse 'header', HeaderView, region: 'header'

  index: ->
    new IndexView
      region: 'container'
    new SearchView
      region: 'search'
