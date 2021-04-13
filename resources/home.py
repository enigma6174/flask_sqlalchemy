from flask import render_template, make_response
from flask_restful import Resource


class Home(Resource):

    def __init__(self):
        self.font_url = "https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap"
        self.header = {'Content-Type': 'text/html'}

    def get(self):
        return make_response(render_template('index.html', font_url=self.font_url), 200, self.header)
