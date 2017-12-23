from flask_assets import Bundle


css = Bundle(
    'css/bootstrap.min.css',
    'css/bootstrap-table.min.css',
    'http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700',
    'css/demo.min.css',
    'css/dashboard.css',
    'css/styles.css'
)

js = Bundle(
    'js/jquery.min.js',
    'js/resizer.js',
    'js/jquery-ui.min.js',
    'js/jquery.slimscroll.min.js',
    'js/switchery.min.js',
    'js/bootstrap.min.js',
    'js/bootstrap-table.min.js',
    'js/bootstrap-table-pt-BR.js',
    'js/bootstrap-table-reorder-columns.js',
    'js/jquery.dragtable.js',
    'js/ultra.js',
    'js/demo.js',
    'js/init.js',
    filters='jsmin',
    output='gen/packed.js'
)