<p float="middle">
  <img width="400" alt="portfolio_view" src="https://raw.githubusercontent.com/zackmawaldi/Reddit-to-Instagram-posting-webapp/main/screenshots/2.png">
  <img width="400" alt="portfolio_view" src="https://raw.githubusercontent.com/zackmawaldi/Reddit-to-Instagram-posting-webapp/main/screenshots/1.png">
<!--  <img width="200" alt="portfolio_view" src="https://raw.githubusercontent.com/zackmawaldi/Reddit-to-Instagram-posting-webapp/main/screenshots/3.png"> -->
</p>

# Reddit to Instagram posting webapp
Web app I wrote that allows users to use Reddit's API to automate posts on Instagram, using Facebooks's API. Flask is underlying infrastructure. I needed to write this app since I had an Instagram page, and I wanted to upload to it automatically, and in a way that's supported by Instagram officially.

### Things I wanted to get out of this project:
Main purpose of this project is to help me automate/streamline posting process on my business IG page. So when I wrote the code, the end goal was to just work, and I didn't care if the code was hard to read. In retrospect, that's bad practice.
I also wanted to learn and pick up how use Reddit and Facebooks APIs, Flask, basic html, SQL, and generally work with a larger project.

I think I'm done with this project. The tool is very useful to me, and I use it daily to manage my IG page. I may add a feature that allows scaling to multiple IG pages, we'll see.

### Usage
First, modify all `.txt` files so that they apply to you. Script splits data with `,`, so make sure that your info don't have any `,`.
Setting up Facebook's API is a pain. Check out this [YouTube tutorial](https://www.youtube.com/watch?v=Q5kw7vGLqgs) on how to set it up. [Here's the link](https://developers.facebook.com/docs/instagram-api/) to official Facebook documentation.

## How to use this app
The key piece of code is `flask_app.py` file. It's the hub of flask web app. From there, requests are made and received. Here's the workflow: user requests to go to the webapp though `flask_app.py` → `flask_app.py` requests images from `reddit_scraper.py` and they get displayed → user selects image and either sets it to schedule or post

if post:
`post_to_ig` is used to post using Facebook API

if schedule:
`flask_app.py` uses SQL to place post into in `database.db`

### Dependencies:
- flask
- praw
- time
- sqlite3
- requests

### Rights

If you'd like to implement as similar script, feel free to fork! If you're going to use this project, or any aspect of it commercially, let me know first.
