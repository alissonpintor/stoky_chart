# Imports do Flask
from flask import render_template

# imports da aplicação
from app.application import app


# Views para tratar os erros
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('errors/page_404.html.j2', error=error), 404


# View para erros internos da aplicação
@app.errorhandler(500)
def internalServerError(error):
    return render_template('errors/page_500.html.j2', error=error), 500
