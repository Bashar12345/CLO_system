from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404():
    return render_template('error/404.html'), 404


@errors.app_errorhandler(403)
def error_403():
    return render_template('error/403.html'), 403


@errors.app_errorhandler(500)
def error_500():
    return render_template('error/500.html'), 500
