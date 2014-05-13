module.exports =

  get_root_url: ->
    # 网站根目录
    window.location.origin

  get_url_params: ->
    query = window.location.search.substring(1)
    raw_vars = query.split("&")

    params = {}

    for v in raw_vars
      [key, val] = v.split("=")
      params[key] = decodeURIComponent(val)

    params
