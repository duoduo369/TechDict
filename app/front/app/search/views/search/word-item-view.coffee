View = require 'common/views/base/view'
subscribe = Chaplin.mediator.subscribe

module.exports = class WordItemView extends View
  autoRender: true
  template: require './templates/word-item'
