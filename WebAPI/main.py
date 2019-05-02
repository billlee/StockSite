from flask import Blueprint, jsonify, abort, make_response, request, render_template, redirect, url_for
import sqlite3
import requests

bp = Blueprint('main',__name__)

@bp.route('/StockApp/')
def home():
    return render_template('main.html')

@bp.route('/StockApp/historical/', methods=['GET','POST'])
def fetch():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
    else:
        ticker = request.args.get('ticker', '')
    return render_template('main.html')

@bp.route('/StockApp/predict/', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        type = request.form.get('type')
        return render_template('predict.html')
    else:
        ticker = request.args.get('ticker', '')
        type = request.args.get('predictionType', '')
        return render_template('predict.html')
    
# @bp.errorhandler(400)
# def bad_request(error):
    # return make_response(jsonify({'error': 'Bad request'}), 400)
    
@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
if __name__ == '__main__':
    app.run(debug=True)
    
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db