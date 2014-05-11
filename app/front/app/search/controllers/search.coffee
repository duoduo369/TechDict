Controller = require 'common/controllers/base/controller'
HeaderView = require 'search/views/common/header-view'
HomeView = require 'search/views/home/home-view'
IndexView = require 'search/views/index/index-view'
SearchView = require 'search/views/index/search-view'
WordCollection = require 'search/models/word-collection'
WordCollectionView = require 'search/views/search/word-list-view'

module.exports = class SearchController extends Controller

  beforeAction: ->
    @reuse 'home', HomeView
    @reuse 'header', HeaderView, region: 'header'
    @reuse 'container', IndexView, region: 'container'
    @reuse 'search', SearchView, region: 'search'

  search: (params, route, options)->
    console.log options['query']['word']
    console.log 'search'
    new WordCollectionView
      region: 'search-display'
      collection: new WordCollection
