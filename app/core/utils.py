import os
from flask import Flask, request, redirect, url_for, config
from werkzeug.utils import secure_filename


def allowedFiles(fileName):
    return '.' in fileName and fileName.rsplit('.', 1)[1].lower() in config['ALLOWED_EXTENSIONS']