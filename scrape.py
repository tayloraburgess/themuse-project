import requests

def job_params(cache, api_key):
    if not cache.get('job_params'):
        return_data = {
            'companies': set(),
            'categories': set(),
            'levels': set(),
            'locations': set()
        }
        data = {
            'api_key': api_key,
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
    
def company_params(cache, api_key):
    if not cache.get('company_params'):
        return_data = {
            'industries': set(),
            'sizes': set(),
            'locations': set()
        }
        data = {
            'api_key': api_key,
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

def post_tags(cache, api_key):
    if not cache.get('post_params'):
        return_tags = set()
        data = {
            'api_key': api_key,
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

def coach_params(cache, api_key):
    if not cache.get('coach_params'):
        return_data = {
            'offerings': set(),
            'levels': set(),
            'specializations': set()
        }
        data = {
            'api_key': api_key,
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
