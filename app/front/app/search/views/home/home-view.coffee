View = require 'common/views/base/view'

module.exports = class HomeView extends View

  autoRender: true
  container: 'body'
  template: require './templates/home'

  regions:
    'header': 'header'
    'container': '.container'
    'footer': 'footer'
