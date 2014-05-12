CollectionView = require 'common/views/base/collection-view'
ItemView = require './word-item-view'
subscribe = Chaplin.mediator.subscribe

module.exports = class WordListView extends CollectionView
  autoRender: true
  template: require './templates/word-list'
  itemView: ItemView
  listSelector: '.list'

  initialize: ->
    super
    @collection.fetch({data:@collection.options['data']})
