from flask import render_template
from . import bp as main

@main.route('/')
def home():
    matrix_posts = {'instructors' : {
                        'sean' : ['Flask week is here'],
                        'dylan' : ['I love flask']},
                    'students' : {
                        student : [f'this is post {num}']for num, student in enumerate(['ben','christian','sima','david'])}}
    return render_template('index.jinja', instructors = matrix_posts['instructors'], students = matrix_posts['students'], title='Fakebook Home')