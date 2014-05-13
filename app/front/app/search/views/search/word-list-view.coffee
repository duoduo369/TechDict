CollectionView = require 'common/views/base/collection-view'
ItemView = require './word-item-view'
subscribe = Chaplin.mediator.subscribe

module.exports = class WordListView extends CollectionView
  autoRender: true
  template: require './templates/word-list'
  itemView: ItemView
  listSelector: '.list'

  events:
    'mouseover .search-word-item': 'hover_in_item'
    'mouseout .search-word-item': 'hover_out_item'
    'click .search-word-item': 'click_item'
    'click .search-word-item .rb-close': 'click_item_close'

  hover_in_item: (e)->
    $cur = $(e.currentTarget or e)
    $('> h3', $cur).css('opacity', 1)
      .css('transition', 'opacity 0.3s ease-in-out')
    $('> span', $cur).css('opacity', .8)
      .css('transition', 'opacity 0.3s ease-in-out')

  hover_out_item: (e)->
    $cur = $(e.currentTarget or e)
    $('> h3', $cur).css('opacity', .8)
      .css('transition', 'opacity 0.3s ease-in-out')
    $('> span', $cur).css('opacity', .6)
      .css('transition', 'opacity 0.3s ease-in-out')

  click_item: (e)->
    $cur = $(e.currentTarget or e)
    $overlay = $('.rb-overlay', $cur)
    $close = $('.rb-close', $cur)
    $overlay.css('opacity', 1).css('zIndex', 9999).css('pointer-events','auto')

  click_item_close: (e)->
    $cur = $(e.currentTarget or e)
    $overlay = $cur.parent()
    $overlay.css('opacity', 0)
      .css('zIndex', -1)
      .css('pointer-events', 'none')
    e.stopPropagation()

  initialize: ->
    super
    @collection.fetch
      data: @collection.options['data']
      success: @loading_done

  renderItem: (item) ->
    super

  insertView: (item, view, position, enableAnimation = true) =>
    # 将word item中背景样式补全
    _position = position
    unless typeof position is 'number'
      _position = @collection.indexOf item
    $el = view.$el
    _position = _position % 10 + 1
    if not _position
      _position = 10
    class_1 = 'bg-' + _position
    fg_class_1 = 'fg-' + _position
    $el.addClass(class_1)
    # 将word item弹出层样式和文字补全
    trans = item.get('trans')
    trans = if trans then trans else []
    trans_length = trans.length
    if trans_length < 7
      for i in [trans_length...7]
        trans[i] = undefined

    $('.search-word', $el).addClass(class_1)
    $dom_sw = $('.search-word-trans', $el)
    for i in [1..7]
      obj = trans[i-1]
      dom_string = '<div></div>'
      if obj
        raw_data = obj['raw_data']
        dom_string = '<div><span>'+obj['word']+'</span><ul>'
        raw_data_length = raw_data.length
        if raw_data_length < 4
          for j in [raw_data_length...4]
            raw_data[j] = undefined
        for j in [1..4]
          raw = raw_data[j-1]
          if raw
            dom_string += '<li><a href="'+raw['url']+'" target=_blank>'
            dom_string += raw['title_cn']+'</a></li>'
        dom_string += '</ul></div>'

      $(dom_string)
        .addClass('trans-word')
        .addClass(class_1+'-'+i)
        .appendTo($dom_sw)
    super
