from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from werkzeug.utils import secure_filename
import json
import os

# provide static_url_path always to avoid collision with app static folder.
# change all url_for arguments to urlshort.static or urlshort.func_name
bp = Blueprint('urlshort', __name__, static_folder='static',
               static_url_path='/public', template_folder='templates')


# app decorators --> bp decorators
@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        # load all the urls used.
        if os.path.exists('urls.json'):
            with open('urls.json') as fo:
                urls = json.load(fo)

        if request.form['code'] in urls.keys():
            # flash messages requires app.secret_key
            flash('name already used.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            # use werkzeug.utils secure_name to convert the user uploaded file name
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save(bp.root_path + '/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('./urls.json', 'w') as fo:
            session[request.form['code']] = True
            json.dump(urls, fo)

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


# variable route
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as fo:
            urls = json.load(fo)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('urlshort.static', filename='user_files/'+urls[code]['file']))

    # if code not found urls.json show 404 error page
    # logic needs refining!
    return abort(404)


# Errorhandler to use custom 404 page.
@bp.errorhandler(404)
def not_found(error):
    return render_template('page_not_found.html'), 404


# toy api
@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
