View = require 'common/views/base/view'
CollectionView = require 'common/views/base/collection-view'
List = require 'search/models/list'
Item = require 'search/models/item'
ItemView = require './item-view'

module.exports = class ListView extends CollectionView

  autoRender: true
  className: 'pure-u-1 text-center'
  itemView: ItemView
  listSelector: 'ul'
  template: require './templates/list'

  events:
    'click button': 'addItem'

  initialize: ->
    @collection = new List
    @counter = 0
    super

  addItem: ->
    @counter++
    item = new Item
    item.set
      part2: "#{item.get 'part2'} #{@counter}"
    @collection.add item
