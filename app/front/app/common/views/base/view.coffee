module.exports = class View extends Chaplin.View

  listen:
    'addedToDOM': 'addedToDOM'

  addedToDOM: ->

  getTemplateFunction: ->
    @template

