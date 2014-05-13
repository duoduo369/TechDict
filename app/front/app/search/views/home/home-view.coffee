View = require 'common/views/base/view'

module.exports = class HomeView extends View

  autoRender: true
  container: 'body'
  keepElement: true
  template: require './templates/home'

  regions:
    'header': 'header'
    'container': '.container'
    'footer': 'footer'
