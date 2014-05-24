module.exports = (match) ->
  match '', 'home#index'
  match '!/stat', 'home#stat'
  match '!/search', 'search#search'
