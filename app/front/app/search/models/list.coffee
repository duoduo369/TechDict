Collection = require 'common/models/base/collection'
Item = require './item'

module.exports = class List extends Collection

  model: Item
