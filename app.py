from flask import Flask, request, render_template, send_from_directory
from werkzeug.contrib.cache import SimpleCache
import requests
import json
from os import environ

app = Flask(__name__, static_url_path='/static')
cache = SimpleCache()

def scrape_job_params():
    if not cache.get('job_params'):
        return_data = {
            'companies': set(),
            'categories': set(),
            'levels': set(),
            'locations': set()
        }
        data = {
            'api_key': environ['THEMUSE_API_KEY'],
            'page': 1
        }
        res = requests.get('https://api-v2.themuse.com/jobs', data)
        while 'results' in res.json():
            for job in res.json()['results']:
                for location in job['locations']:
                    return_data['locations'].add(location['name'])
                for category in job['categories']:
                    return_data['categories'].add(category['name'])
                for level in job['levels']:
                    return_data['levels'].add(level['name'])
                return_data['companies'].add(job['company']['name'])
            data['page'] += 1
            res = requests.get('https://api-v2.themuse.com/jobs', data)
        cache.set('job_params', return_data) 
        return return_data
    else:
        return cache.get('job_params')
    
def scrape_company_params():
    if not cache.get('company_params'):
        return_data = {
            'industries': set(),
            'sizes': set(),
            'locations': set()
        }
        data = {
            'api_key': environ['THEMUSE_API_KEY'],
            'page': 1
        }
        res = requests.get('https://api-v2.themuse.com/companies', data)
        while 'results' in res.json():
            for job in res.json()['results']:
                for location in job['locations']:
                    return_data['locations'].add(location['name'])
                for industry in job['industries']:
                    return_data['industries'].add(industry['name'])
                return_data['sizes'].add(job['size']['name'])
            data['page'] += 1
            res = requests.get('https://api-v2.themuse.com/companies', data)
        cache.set('company_params', return_data)
        return return_data
    else: 
        return cache.get('company_params')

def scrape_post_tags():
    if not cache.get('post_params'):
        return_tags = set()
        data = {
            'api_key': environ['THEMUSE_API_KEY'],
            'page': 1
        }
        res = requests.get('https://api-v2.themuse.com/posts', data)
        while 'results' in res.json():
            for job in res.json()['results']:
                for tag in job['tags']:
                    return_tags.add(tag['name'])
            data['page'] += 1
            res = requests.get('https://api-v2.themuse.com/posts', data)
        cache.set('post_params', return_tags)
        return return_tags
    else:
        return cache.get('post_params')

def scrape_coach_params():
    if not cache.get('coach_params'):
        return_data = {
            'offerings': set(),
            'levels': set(),
            'specializations': set()
        }
        data = {
            'api_key': environ['THEMUSE_API_KEY'],
            'page': 1
        }
        res = requests.get('https://api-v2.themuse.com/coaches', data)
        while 'results' in res.json():
            for job in res.json()['results']:
                for specialization in job['specializations']:
                    return_data['specializations'].add(specialization['name'])
                for product in job['products']:
                    return_data['offerings'].add(product['offering']['name'])
                return_data['levels'].add(job['level']['name'])
            data['page'] += 1
            res = requests.get('https://api-v2.themuse.com/coaches', data)
        cache.set('coach_params', return_data)
        return return_data
    else:
        return cache.get('coach_params')

def get_jobs(page=1, company=None, category=None, level=None, location=None):
    data = {
        'api_key': environ['THEMUSE_API_KEY'],
        'page': page,
        'company': company,
        'category': category,
        'level': level,
        'location': location 
    } 
    res = requests.get('https://api-v2.themuse.com/jobs', data)
    return res.json()['results']

def get_companies(page=1, industry=None, size=None, location=None):
    data = {
        'api_key': environ['THEMUSE_API_KEY'],
        'page': page,
        'industry': industry,
        'size': size,
        'location': location 
    } 
    res = requests.get('https://api-v2.themuse.com/companies', data)
    return res.json()['results']

def get_coaches(page=1, offering=None, level=None, specialization=None):
    data = {
        'api_key': environ['THEMUSE_API_KEY'],
        'page': page,
        'offering': offering,
        'level': level,
        'specialization': specialization 
    } 
    res = requests.get('https://api-v2.themuse.com/coaches', data)
    return res.json()['results']

def get_posts(page=1, tag=None):
    data = {
        'api_key': environ['THEMUSE_API_KEY'],
        'page': page,
        'tag': tag 
    } 
    res = requests.get('https://api-v2.themuse.com/posts', data)
    return res.json()['results']

@app.route('/', methods=['GET', 'POST'])
def index():
    filter_data = scrape_job_params()
    if request.method == 'GET': 
        jobs = get_jobs()
        default = {
            'company': None,
            'category': None,
            'level': None,
            'location': None
        }
        return render_template('index.html', filter_data=filter_data, jobs=jobs, default=default) 
    else:
        company = request.form['company'] if request.form['company'] else None
        category = request.form['category'] if request.form['category'] else None
        level = request.form['level'] if request.form['level'] else None
        location = request.form['location'] if request.form['location'] else None
        default = {
            'company': company,
            'category': category,
            'level': level,
            'location': location
        }
        jobs = get_jobs(1, company, category, level, location)
        return render_template('index.html', filter_data=filter_data, jobs=jobs, default=default) 

@app.route('/companies', methods=['GET', 'POST'])
def companies():
    filter_data = scrape_company_params()
    if request.method == 'GET':
        companies = get_companies()
        default = {
            'industry': None,
            'size': None,
            'location': None
        }
        return render_template('companies.html', filter_data=filter_data, companies=companies, default=default)
    else:
        industry = request.form['industry'] if request.form['industry'] else None
        size = request.form['size'] if request.form['size'] else None
        location = request.form['location'] if request.form['location'] else None
        default = {
            'industry': industry,
            'size': size,
            'location': location
        }
        companies = get_companies(1, industry, size, location)
        return render_template('companies.html', filter_data=filter_data, companies=companies, default=default) 

@app.route('/coaches', methods=['GET', 'POST'])
def coaches():
    filter_data = scrape_coach_params()
    if request.method == 'GET':
        coaches = get_coaches()
        default = {
            'offering': None,
            'level': None,
            'specialization': None
        }
        return render_template('coaches.html', filter_data=filter_data, coaches=coaches, default=default)
    else:
        offering = request.form['offering'] if request.form['offering'] else None
        level = request.form['level'] if request.form['level'] else None
        specialization = request.form['specialization'] if request.form['specialization'] else None
        default = {
            'offering': offering,
            'level': level,
            'specialization': specialization
        }
        coaches = get_coaches(1, offering, level, specialization)
        return render_template('coaches.html', filter_data=filter_data, coaches=coaches, default=default) 


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    filter_data = scrape_post_tags()
    if request.method == 'GET':
        posts = get_posts()
        default = None
        return render_template('posts.html', filter_data=filter_data, posts=posts, default=default)
    else:
        tag = request.form['tag'] if request.form['tag'] else None
        default = tag
        posts = get_posts(1, tag)
        return render_template('posts.html', filter_data=filter_data, posts=posts, default=default) 

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('static/css', path)

app.run()
