exports.config =
  plugins:
    autoReload:
      port: 9485
    coffeelint:
      pattern: /^app\/.*\.coffee$/
      options:
        no_trailing_semicolons:
          level: "ignore"
        max_line_length:
          level: "ignore"
  # See http://brunch.io/#documentation for docs.
  files:
    javascripts:
      joinTo:
        'javascripts/app.js': /^app|(?!zarfx)/
        'javascripts/vendor.js': /^(?!app)/
        #'javascripts/vendor.js': /^(?!app)|^lib/
        #'javascripts/vendor.js': /^(?!app)|node_modules\/d3\.layout\.cloud/

    stylesheets:
      joinTo: 'stylesheets/app.css'

    templates:
      joinTo: 'javascripts/app.js'
