Collection = require 'common/models/base/collection'
Item = require './word-search-item'

module.exports = class WordSearchCollection extends Collection

  model: Item

  urlPath: -> "/search"
