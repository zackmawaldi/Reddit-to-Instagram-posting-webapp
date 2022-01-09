"""this script logs into reddit through"""
import praw

login_info = open('reddit_login_info.txt', mode='r').read().split(',')

client_id = login_info[0]
client_secret = login_info[1]
password = login_info[2]
user_agent = login_info[3]
username = login_info[4]

red = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     username=username)