module.exports = class View extends Chaplin.View

  listen:
    'addedToDOM': 'addedToDOM'

  addedToDOM: ->

  getTemplateFunction: ->
    @template

  initialize: =>
    super
    @init_loading()

  init_loading: ->
    $('.loading').removeClass('hidden').addClass('show')
  loading_done: ->
    $('.loading').removeClass('show').addClass('hidden')
