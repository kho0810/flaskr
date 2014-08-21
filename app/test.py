from flask import Flask, jsonify, request, render_template, redirect, url_for
from app import app
import pusher


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


@app.route('/chat', methods=['GET'])
def chat():
    p = pusher.Pusher(
      app_id='86070',
      key='62270f36d7ecf7bf7ef0',
      secret='46b772c92bcc9d25fae9'
      )
    p['test_channel'].trigger('my_event', {
        'name': request.args.get('name_data'),
        'msg': request.args.get('msg_data')
        })
    return ""


@app.route('/mini_chat')
def mini_chat():
    return render_template("mini_chat.html")
