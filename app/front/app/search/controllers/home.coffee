Controller = require 'common/controllers/base/controller'
HeaderView = require 'search/views/common/header-view'
HomeView = require 'search/views/home/home-view'
IndexView = require 'search/views/index/index-view'
SearchView = require 'search/views/index/search-view'
CloudView = require 'search/views/index/cloud-view'
WordCloudCollection = require 'search/models/word-cloud-collection'

module.exports = class HomeController extends Controller

  beforeAction: ->
    @reuse 'home', HomeView
    @reuse 'header', HeaderView, region: 'header'

  index: ->
    new IndexView
      region: 'container'
    new SearchView
      region: 'search'
    new CloudView
      region: 'search-display'
      collection: new WordCloudCollection
