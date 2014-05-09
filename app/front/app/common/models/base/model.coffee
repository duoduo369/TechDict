config = require 'common/config'

module.exports = class Model extends Chaplin.Model
  apiRoot: config.apiRoot

  urlRoot: ->
    return "#{@apiRoot}#{@urlPath()}" if @id or not @collection
    return "#{@apiRoot}#{@collection.urlPath()}"
