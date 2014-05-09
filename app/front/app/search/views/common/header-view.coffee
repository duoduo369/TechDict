View = require 'common/views/base/view'

module.exports = class HeaderView extends View
  autoRender: true
  container: 'body'
  template: require './templates/header'
  initialize: ->
    super
    console.log 'header'
