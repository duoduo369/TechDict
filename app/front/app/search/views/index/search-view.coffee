View = require 'common/views/base/view'
publish = Chaplin.mediator.publish

module.exports = class SearchView extends View
  autoRender: true
  container: '.search'
  noWrap: true
  template: require './templates/search'
  events:
    'click button': 'search'
  initialize: ->
    super

  search: ->
    publish 'search', $('#search_input').val()
