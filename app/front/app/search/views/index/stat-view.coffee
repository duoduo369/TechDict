View = require 'common/views/base/view'
Utils = require 'common/lib/utils'

module.exports = class StatView extends View
  autoRender: true
  className: 'stat full-width'
  template: require './templates/stat'

  initialize: =>
    super
    @collection.fetch
      success: =>
        @loading_done()
        @init_chart()

  init_chart: =>
    ctx = @$('#stat_line_chart')[0].getContext('2d')
    total_nums = @collection.pluck('total_num')
    scrapy_nums = @collection.pluck('scrapy_num')
    stat_nums = @collection.pluck('stat_num')
    total_num = Utils.sum(total_nums)
    scrapy_num = Utils.sum(scrapy_nums)
    stat_num = Utils.sum(stat_nums)
    sel_dict =
      '#stat_total': total_num
      '#scrapy_num': scrapy_num
      '#stat_num': stat_num
    for sel_id, num of sel_dict
      @$(sel_id+' .data').html(num)
    options =
      scaleFontSize: 20
    data =
      labels: @collection.pluck('year')
      datasets: [
        {
          fillColor: 'rgba(220,220,220,0.5)',
          strokeColor: 'rgba(220,220,220,1)',
          pointColor: 'rgba(220,220,220,1)',
          pointStrokeColor: '#fff',
          data: total_nums
        },
        {
          fillColor : "rgba(151,187,205,0.5)",
          strokeColor : "rgba(151,187,205,1)",
          pointColor : "rgba(151,187,205,1)",
          pointStrokeColor : "#fff",
          data: scrapy_nums
        },
        {
          fillColor : "rgba(151,187,205,0.5)",
          strokeColor : "rgba(151,187,205,1)",
          pointColor : "rgba(151,187,205,1)",
          pointStrokeColor : "#fff",
          data: stat_nums
        },
      ]
    line_char = new Chart(ctx).Line(data, options)
