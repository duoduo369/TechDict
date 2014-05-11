View = require 'common/views/base/view'
WordCollection = require 'search/models/word-collection'

module.exports = class CloudView extends View
  autoRender: true
  className: 'abc'
  container: '.word-cloud'
  template: require './templates/word-cloud'
  events:
    'click button': 'search'

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

    d3.layout.cloud().size([600, 300])
      .words(words
      .map (d) -> return {text: d['word'], size: 18 + 6 * d['word_count']})
      .padding(5)
      .rotate((d, i)-> return (i % 2 ) * 90)
      .font("Impact")
      .fontSize((d)-> return d.size)
      .on("end", @draw)
      .start()

  draw: (words)->
    fill = d3.scale.category20()
    d3.select('.word-cloud').append("svg")
      .attr("width", 600)
      .attr("height", 300)
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
