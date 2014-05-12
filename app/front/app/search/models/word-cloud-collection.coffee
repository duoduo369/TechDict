Collection = require 'common/models/base/collection'
Item = require './word-cloud-item'

module.exports = class WordCloudCollection extends Collection

  model: Item

  urlPath: -> "/wordcloud"
