Model         = require './model'
config        = require "common/config"

module.exports = class Collection extends Chaplin.Collection

  apiRoot: config.apiRoot

  # Use the project base model per default, not Chaplin.Model
  model: Model

  url: ->
    "#{@apiRoot}#{@urlPath()}"

  initialize: (options={})=>
    super
    @options = options
