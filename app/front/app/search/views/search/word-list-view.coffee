CollectionView = require 'common/views/base/collection-view'
ItemView = require './word-item-view'
subscribe = Chaplin.mediator.subscribe

module.exports = class WordListView extends CollectionView
  autoRender: true
  template: require './templates/word-list'
  itemView: ItemView
  listSelector: 'div.list'

  initialize: ->
    super
    console.log @collection.options['data']
    @collection.fetch({data:@collection.options['data']})
