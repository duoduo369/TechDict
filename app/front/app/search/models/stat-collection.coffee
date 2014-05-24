Collection = require 'common/models/base/collection'
Item = require './stat-item'

module.exports = class StatCollection extends Collection

  model: Item

  urlPath: -> "/stat"
