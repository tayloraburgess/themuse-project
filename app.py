from flask import Flask, request, render_template, send_from_directory
from werkzeug.contrib.cache import SimpleCache
import os, requests, json, scrape, muse 

app = Flask(__name__, static_url_path='/static')
cache = SimpleCache()
api_key = os.environ['THEMUSE_API_KEY']

@app.route('/', methods=['GET', 'POST'])
def index():
    filter_data = scrape.job_params(cache, api_key)
    if request.method == 'GET': 
        jobs = muse.jobs(api_key)
        default = {
            'company': None,
            'category': None,
            'level': None,
            'location': None
        }
        context = {
            'filter_data': filter_data,
            'jobs': jobs['results'],
            'page': jobs['page'],
            'page_count': jobs['page_count'],
            'default': default
        }
        return render_template('index.html', **context) 
    else:
        company = request.form['company'] if request.form['company'] else None
        category = request.form['category'] if request.form['category'] else None
        level = request.form['level'] if request.form['level'] else None
        location = request.form['location'] if request.form['location'] else None
        jobs = muse.jobs(api_key, int(request.form['page']), company, category, level, location)
        default = {
            'company': company,
            'category': category,
            'level': level,
            'location': location
        }
        context = {
            'filter_data': filter_data,
            'jobs': jobs['results'],
            'page': jobs['page'],
            'page_count': jobs['page_count'],
            'default': default
        }
        return render_template('index.html', **context) 

@app.route('/companies', methods=['GET', 'POST'])
def companies_route():
    filter_data = scrape.company_params(cache, api_key)
    if request.method == 'GET':
        companies = muse.companies(api_key)
        default = {
            'industry': None,
            'size': None,
            'location': None
        }
        context = {
            'filter_data': filter_data,
            'companies': companies['results'],
            'page': companies['page'],
            'page_count': companies['page_count'],
            'default': default
        }
        return render_template('companies.html', **context)
    else:
        industry = request.form['industry'] if request.form['industry'] else None
        size = request.form['size'] if request.form['size'] else None
        location = request.form['location'] if request.form['location'] else None
        companies = muse.companies(api_key, int(request.form['page']), industry, size, location)
        default = {
            'industry': industry,
            'size': size,
            'location': location
        }
        context = {
            'filter_data': filter_data,
            'companies': companies['results'],
            'page': companies['page'],
            'page_count': companies['page_count'],
            'default': default
        }
        return render_template('companies.html', **context) 

@app.route('/coaches', methods=['GET', 'POST'])
def coaches_route():
    filter_data = scrape.coach_params(cache, api_key)
    if request.method == 'GET':
        coaches = muse.coaches(api_key)
        default = {
            'offering': None,
            'level': None,
            'specialization': None
        }
        context = {
            'filter_data': filter_data,
            'coaches': coaches['results'],
            'page': coaches['page'],
            'page_count': coaches['page_count'],
            'default': default
        }
        return render_template('coaches.html', **context)
    else:
        offering = request.form['offering'] if request.form['offering'] else None
        level = request.form['level'] if request.form['level'] else None
        specialization = request.form['specialization'] if request.form['specialization'] else None
        coaches = muse.coaches(api_key, int(request.form['page']), offering, level, specialization)
        default = {
            'offering': offering,
            'level': level,
            'specialization': specialization
        }
        context = {
            'filter_data': filter_data,
            'coaches': coaches['results'],
            'page': coaches['page'],
            'page_count': coaches['page_count'],
            'default': default
        }
        return render_template('coaches.html', **context) 


@app.route('/posts', methods=['GET', 'POST'])
def posts_route():
    filter_data = scrape.post_tags(cache, api_key)
    if request.method == 'GET':
        posts = muse.posts(api_key)
        default = None
        context = {
            'filter_data': filter_data,
            'posts': posts['results'],
            'page': posts['page'],
            'page_count': posts['page_count'],
            'default': default
        }
        return render_template('posts.html', **context)
    else:
        tag = request.form['tag'] if request.form['tag'] else None
        posts = muse.posts(api_key, int(request.form['page']), tag)
        default = tag
        context = {
            'filter_data': filter_data,
            'posts': posts['results'],
            'page': posts['page'],
            'page_count': posts['page_count'],
            'default': default
        }
        return render_template('posts.html', **context) 

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('static/css', path)

app.run()
