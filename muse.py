import json, requests

def jobs(api_key, page=1, company=None, category=None, level=None, location=None):
    data = {
        'api_key': api_key,
        'page': page,
        'company': company,
        'category': category,
        'level': level,
        'location': location 
    } 
    res = requests.get('https://api-v2.themuse.com/jobs', data)
    return res.json()

def companies(api_key, page=1, industry=None, size=None, location=None):
    data = {
        'api_key': api_key,
        'page': page,
        'industry': industry,
        'size': size,
        'location': location 
    } 
    res = requests.get('https://api-v2.themuse.com/companies', data)
    return res.json()

def coaches(api_key, page=1, offering=None, level=None, specialization=None):
    data = {
        'api_key': api_key, 
        'page': page,
        'offering': offering,
        'level': level,
        'specialization': specialization 
    } 
    res = requests.get('https://api-v2.themuse.com/coaches', data)
    return res.json()

def posts(api_key, page=1, tag=None):
    data = {
        'api_key': api_key,
        'page': page,
        'tag': tag 
    } 
    res = requests.get('https://api-v2.themuse.com/posts', data)
    return res.json()

