# The Muse Interview Project

A small web app, with the backend written purely in Flask—the client side is entirely templated views that Flask serves (with currently very minimal styling).

The app interacts with The Muse public API, allowing users to filter Jobs, Companies, Posts & Coaches using a number of categories. This is done via POST requests and page re-renders once the user submits their filters.

Additionally, the app scrapes The Muse API to create an exhaustive list of categories that can be filtered, and uses a very simple caching system to avoid constant (and very slow) additional requests for this information.

## Running locally

1. Clone this repository.

2. Create a Python virtual environment within the repository (i.e. `virtualenv venv`), and activate it, and run `pip3 install -r requirements.txt`

3. In your environment, export a key for The Muse public API as ‘THEMUSE_API_KEY’

4. Start the development server with ‘python3 app.py’

