from flask import Flask, render_template, redirect, request
import random
import post_to_ig as p
import reddit_scraper as r
import time
import sqlite3 as sql

app = Flask(__name__)

# opens, reads, then splits captions, used captions. Hashtags are just opened.
captions_list = open('captions.txt', mode='r').read().split(',')
used_captions_list = open('used_captions.txt', mode='r').read().split(',')
tags = open('hashtags.txt', mode='r').read()


# opens, reads, then splits FB authentication tokens and page ID. AT and FB_page_id return lists.
FB_page_id = open('real_authen.txt', mode='r').read().split(',')[0]
AT = open('real_authen.txt', mode='r').read().split(',')[1]


# selects a caption to be used in post
def random_caption(old_caption):
    while True:
        x = random.choice(captions_list)
        if x not in used_captions_list and x !=  old_caption:
            break
    return x



"""
selects images from subreddits given. returns url and author.
used to display images in web app, and allow user to select desired image to be published.
"""
def image_selector(count):
    global author
    log_in = r.red
    log_subs = log_in.subreddit('chemistrymemes+mathmemes+physicsmemes+okbuddyphd')
    memes = log_subs.top('day', limit=50)
    loop_counter = 0
    for submission in memes:
        if not submission.stickied:
            x = submission.url
            author = submission.author
            file_type = x.split('.')[-1]
            if file_type == 'jpg' or 'jpeg' or 'png':
                if loop_counter == count:
                    break
        loop_counter += 1
    return x, str(author)


def add_to_db(url, author, caption):
    conn = sql.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO que VALUES ('{}', '{}', '{}', '{}')".format(int(time.time()), url, author, caption))
    c.execute("SELECT * FROM que")
    # y = c.fetchall()
    # print(y)
    conn.commit()
    conn.close()


def get_db_list():
    conn = sql.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM que")
    db_list = c.fetchall()
    conn.commit()
    conn.close()
    return db_list

def del_db_entry(count):
    count = int(count)
    conn = sql.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM que ORDER BY time ASC")
    db_list = c.fetchall()
    time_id = db_list[count][0]
    c.execute("DELETE FROM que WHERE time={}".format(time_id))
    conn.commit()
    conn.close()


# variables displayed to user in web app, and also used in functions below and in html.
top = r.red.subreddit('chemistrymemes+mathmemes+physicsmemes+okbuddyphd').top('day', limit=50)
url_list = [post.url for post in top]

post_outcome = ''  # used to display outcome of attempted post to user.
image_counter = 0  # used in loops below, and to display # of post in web app.
caption_used = random_caption('')
image_url = image_selector(0)[0]

@app.route('/')
def hello_world():
    return 'Hi, this is zack. Please leave a voice message...'

@app.route('/main')
def main_page():
    global top, url_list
    top = r.red.subreddit('chemistrymemes+mathmemes+physicsmemes+okbuddyphd').top('day', limit=50)
    url_list = [post.url for post in top]
    return render_template('index.html', url_list=url_list, pic=image_url, cap='caption: ' + caption_used, count=str(image_counter + 1), post_outcome=post_outcome, db_list=get_db_list())

# allows user to input caption to var caption_used
@app.route('/main', methods=['POST'])
def my_form_post():
    global caption_used, image_counter
    caption_used = request.form['text']
    return redirect("/main")

"""
used to allow user to type in a number to select image.
This feature now is kinda useless, since I added ability to click on image to
select it for posting.
"""
@app.route('/custom_image_counter', methods=['POST', 'GET'])
def custom_image_counter():
    global image_counter, image_url
    image_counter = int(request.form['custom_image_counter']) - 1
    image_url = image_selector(image_counter)[0]
    return redirect("/main")

# allows user to click on image to select it.
@app.route('/custom_image_link/<count>')
def custom_image_link(count):
    global image_counter, image_url
    image_counter = int(count)
    image_url = image_selector(image_counter)[0]
    return redirect("/main")

# click left and right to select image. nulled use since clicking on images is easier
@app.route("/next_image", methods=['POST'])
def next_image():
    global image_counter, image_url
    image_counter += 1
    image_url = image_selector(image_counter)[0]
    return redirect("/main")

@app.route("/previous_image", methods=['POST'])
def previous_image():
    global image_counter, image_url
    image_counter -= 1
    image_url = image_selector(image_counter)[0]
    return redirect("/main")

# display random camption
@app.route("/caption", methods=['POST'])
def caption_button():
    global caption_used
    caption_used = random_caption(caption_used)
    return redirect("/main")

# post to IG button
@app.route("/post", methods=['POST'])
def post_button():
    global caption_used, image_url, post_outcome
    outcome = p.post_to_ig(caption_used, tags + str(author), image_url, FB_page_id, AT)
    if outcome == 1:
        post_outcome = 'POST success!! check IG'
    else:
        post_outcome = 'POST failed.'
    print('POST success!! check IG')
    return redirect("/main")

@app.route("/add_to_schedule", methods=['POST'])
def add_to_schedule():
    global image_counter, que, caption_used, db_list
    post_info = list(image_selector(image_counter))
    #post_info should be [url, auther, caption]
    post_info.append(caption_used)
    add_to_db(post_info[0], post_info[1], post_info[2])
    db_list = get_db_list()
    print(db_list)
    return redirect("/main")

@app.route('/remove_schedule/<count>')
def remove_schedule(count):
    del_db_entry(count)
    return redirect("/main")


