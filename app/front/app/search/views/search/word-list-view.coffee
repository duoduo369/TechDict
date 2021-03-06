CollectionView = require 'common/views/base/collection-view'
ItemView = require './word-item-view'
utils = require 'common/lib/utils'
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
    'click .subject-list li a': 'click_button'
    'click .trans-word': 'click_trans_word'
    'click .word': 'click_word'

  hover_in_item: (e)->
    $cur = $(e.currentTarget or e)
    bg = $cur.attr('class').match(/(bg-(\d+))/)
    if bg
      bg_old = bg[0]
      bg_num = bg[2]
      $cur.removeClass(bg_old)
        .addClass('bd-'+bg_num)
        .css('transition', '.3s ease-in-out')
      $('> h3', $cur).css('opacity', 1)
        .addClass('fg-'+bg_num)
        .css('transition', 'opacity .3s ease-in-out')
      $('> span', $cur).css('opacity', .8)
        .addClass('fg-'+bg_num)
        .css('transition', 'opacity .3s ease-in-out')

  hover_out_item: (e)->
    $cur = $(e.currentTarget or e)
    bg = $cur.attr('class').match(/(bd-(\d+))/)
    if bg
      bd = bg[0]
      bg_num = bg[2]
      $cur.removeClass(bd)
        .addClass('bg-'+bg_num)
        .css('transition', '.3s ease-in-out')
    $('> h3', $cur)
      .removeClass('fg-'+bg_num)
      .css('opacity', .8)
      .css('transition', 'opacity .3s ease-in-out')
    $('> span', $cur)
      .removeClass('fg-'+bg_num)
      .css('opacity', .6)
      .css('transition', 'opacity .3s ease-in-out')

  click_item: (e)->
    $cur = $(e.currentTarget or e)
    $overlay = $('.rb-overlay', $cur)
    $close = $('.rb-close', $cur)
    $overlay.css('opacity', 1).css('zIndex', 9999).css('pointer-events','auto')

  click_item_close: (e) ->
    $cur = $(e.currentTarget or e)
    $overlay = $cur.parent()
    $overlay.css('opacity', 0)
      .css('zIndex', -1)
      .css('pointer-events', 'none')
    @$('.list').removeClass('zoom')
    @$('.trans-word').removeClass('display-hide').removeClass('full-height')
    @$('.trans-word ul').addClass('display-hide')
    e.stopPropagation()

  click_button: (e) ->
    $cur = $(e.currentTarget or e)

  click_word: (e) =>
    if @$('.list').hasClass('zoom')
      @$('.list').removeClass('zoom')
      @$('.trans-word').removeClass('display-hide').removeClass('full-height')
      @$('.trans-word ul').addClass('display-hide')


  click_trans_word: (e) =>
    @$('.list').addClass('zoom')
    $cur = $(e.currentTarget or e)
    $cur.addClass('full-height')
    $('ul', $cur).removeClass('display-hide')
    @$('.trans-word').addClass('display-hide')
    $cur.removeClass('display-hide')

  initialize: =>
    super
    @collection.fetch
      data: @collection.options['data']
      success: (collection, response) =>
        @init_subject_list(response)
        @loading_done()

  init_subject_list: (items) =>
    if not items or not items.length
      $subject_list = @$('.subject-list').html(
        '<span class="no-result">没有找到相应结果，试试看别的关键词吧亲～</span>')

      return
    root = utils.get_root_url()
    params = utils.get_url_params()
    raw_data = _.pluck(items, 'raw_data')
    subjects = _.map(raw_data, (data) -> return _.pluck(data, 'subject'))
    subjects = _.flatten(_.map(raw_data, (data) -> return _.pluck(data, 'subject')))
    subjects = _.uniq(subjects)
    $subject_list = @$('.subject-list')
    _.each(subjects, (sub) ->
      str = '<li><a class="button-xsmall pure-button" '
      str +='href="/!/search?word='+params['word']+'&subject='+sub+'">'
      str += sub+'</a></li>'
      $subject_list.append(str))


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
        dom_string = '<div><span>'+obj['word']+'</span><ul class="text-left display-hide">'
        raw_data_length = raw_data.length
        if raw_data_length < 4
          for j in [raw_data_length...4]
            raw_data[j] = undefined
        for j in [1..4]
          raw = raw_data[j-1]
          if raw
            dom_string += '<li><a href="'+raw['url']+'" target=_blank>'
            dom_string += raw['paper_edu_pub_record']+'</a></li>'
        dom_string += '</ul></div>'

      $(dom_string)
        .addClass('trans-word')
        .addClass(class_1+'-'+i)
        .appendTo($dom_sw)
    super
