View = require 'common/views/base/view'
subscribe = Chaplin.mediator.subscribe

module.exports = class IndexView extends View
  autoRender: true
  className: 'full-width'
  template: require './templates/index'

  regions:
    'search': '.search'
    'word-cloud': '.word-cloud'

  initialize: ->
    super
    subscribe 'search', @search

  search: (args) ->
    console.log args
