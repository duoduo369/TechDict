View = require 'common/views/base/view'
Model = require 'common/models/base/model'
Utils = require 'common/lib/utils'

module.exports = class SearchView extends View
  autoRender: true
  container: '.search'
  noWrap: true
  template: require './templates/search'
  initialize: ->
    super
