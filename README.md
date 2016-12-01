# The Muse Interview Project

A small web app, with the backend written purely in Flask—the client side is entirely templated views that Flask serves (with currently very minimal styling).

The app interacts with The Muse public API, allowing users to filter Jobs, Companies, Posts & Coaches using a number of categories. This is done via POST requests and page re-renders once the user submits their filters.

Additionally, the app scrapes The Muse API to create an exhaustive list of categories that can be filtered, and uses a very simple caching system to avoid constant (and very slow) additional requests for this information.

A test deployment of this app is [here](https://stark-forest-99653.herokuapp.com/).