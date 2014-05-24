View = require 'common/views/base/view'

module.exports = class IndexView extends View
  autoRender: true
  className: 'full-width'
  template: require './templates/index'

  regions:
    'search': '.search'
    'search-display': '.search-display'

  initialize: ->
    super
