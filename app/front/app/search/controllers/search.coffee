Controller = require 'common/controllers/base/controller'
HeaderView = require 'search/views/common/header-view'
HomeView = require 'search/views/home/home-view'
IndexView = require 'search/views/index/index-view'
SearchView = require 'search/views/index/search-view'
Model = require 'common/models/base/model'
WordCloudCollection = require 'search/models/word-cloud-collection'
WordSearchCollection = require 'search/models/word-search-collection'
WordCollectionView = require 'search/views/search/word-list-view'
Utils = require 'common/lib/utils'

module.exports = class SearchController extends Controller

  beforeAction: ->
    @reuse 'home', HomeView
    @reuse 'header', HeaderView, region: 'header'
    @reuse 'container', IndexView, region: 'container'
    #@reuse 'search', SearchView, region: 'search'

  search: (params, route, options)=>
    word = Utils.get_url_params()['word']
    @search_view = new SearchView
      region: 'search'
      model: new Model
        search_word: word

    @word_collection_view = new WordCollectionView
      region: 'search-display'
      collection: new WordSearchCollection
        data: options['query']
