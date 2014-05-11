View = require 'common/views/base/view'
WordCollection = require 'search/models/word-collection'

module.exports = class CloudView extends View
  autoRender: true
  noWrap: true
  template: require './templates/word-cloud'
  events:
    'click button': 'search'
  svg_w: 960
  svg_h: 300

  initialize: =>
    super
    #@collection = new WordCollection
    @collection.fetch
      success: =>
        @init_cloud()

  search: ->
    publish 'search', $('#search_input').val()

  init_cloud: =>

    words = @collection.map (word)->
      'word': word.get('word')
      'word_count': word.get('raw_data_count')

    d3.layout.cloud().size([@svg_w * 1.8, @svg_h * 1.8])
      .words(words
      .map (d) -> return {text: d['word'], size: 18 + 6 * d['word_count']})
      .padding(5)
      .rotate((d, i)-> return (i % 2 ) * 90)
      .font("Impact")
      .fontSize((d)-> return d.size)
      .on("end", @draw)
      .start()

  draw: (words)=>
    fill = d3.scale.category20()
    d3.select('.search-display').append("svg")
      .attr("width", @svg_w)
      .attr("height", @svg_h)
      .attr("class", 'word-cloud')
      .append("g")
      .attr("transform", "translate(150,150)")
      .selectAll("text")
      .data(words)
      .enter().append("text")
        .style("font-size", (d)-> return d.size + "px")
        .style("font-family", "Impact")
        .style("fill", (d, i)-> return fill(i))
        .attr("text-anchor", "middle")
        .attr("transform", (d)->
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"
        )
        .text((d)-> return d.text)
