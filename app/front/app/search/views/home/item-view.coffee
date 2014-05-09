View = require 'common/views/base/view'

module.exports = class ItemView extends View

  tagName: 'li'
  className: 'pure-u-1'
  template: require './templates/item'

  events:
    'click .swap': 'swap'
    'click .delete': 'remove'

  initialize: ->
    @model.bind('change', @render)
    @model.bind('remove', @unrender)
    super


  unrender: =>
    @$el.remove()

  swap: ->
    @model.set
      part1: @model.get 'part2'
      part2: @model.get 'part1'

  remove: ->
    @model.destroy()
