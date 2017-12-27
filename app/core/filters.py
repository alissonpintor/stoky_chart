import datetime


def dateParser(date, format='%d/%m/%Y'):
    if (type(date) == datetime.date):
        return date.strftime(format=format)


def regitryFilters(app):
    app.jinja_env.filters ['dateParser'] = (dateParser)