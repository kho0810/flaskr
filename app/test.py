from flask import Flask, jsonify, request, render_template, redirect, url_for
from app import app


@app.route('/')
def test():
    return render_template('ajax_test.html')


@app.route('/ajax/test', methods=['GET', 'POST'])
def ajax_test():
    resp = {}
    if request.method == 'POST':
        req = request.form

        resp['result'] = int(req['first']) + int(req['second'])
        resp['success'] = True
        return jsonify(resp)
    else:
        return redirect(url_for('test'))
