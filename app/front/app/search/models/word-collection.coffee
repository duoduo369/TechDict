Collection = require 'common/models/base/collection'
Item = require './word-item'

module.exports = class WordCollection extends Collection

  model: Item

  urlPath: -> "/search"
