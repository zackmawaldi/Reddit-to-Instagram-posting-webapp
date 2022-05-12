import requests
import time


def post_to_ig(caption, hashtags, img_url, public_fb_page_id, access_token):
    # First query is to get IG page ID from public FB page ID.
    raw_query_1 = "https://graph.facebook.com/v10.0/{FB_ID}?fields=instagram_business_account&access_token={AT}"\
        .format(
                FB_ID=public_fb_page_id,
                AT=access_token
                )
    query_result_1 = requests.get(raw_query_1)

    # Second query is to post (draft) a post using Reddit URL to IG
    ig_page_id = str(query_result_1.text).split('"')[5]
    raw_query_2 = 'https://graph.facebook.com/{IG_ID}/media?image_url={url}&caption={cap}&access_token={AT}'\
        .format(
                IG_ID=ig_page_id,
                url=img_url,
                cap=requests.utils.quote(caption + hashtags),
                AT=access_token
                )
    query_result_2 = requests.post(raw_query_2)

    # Third query to publish post from last query using post ID created in last query
    post_id = str(query_result_2.text).split('"')[3]
    raw_query_3 = 'https://graph.facebook.com/{IG_ID}/media_publish?creation_id={p_ID}&access_token={AT}'\
        .format(
                IG_ID=ig_page_id,
                p_ID=post_id,
                AT=access_token
                )
    query_result_3 = requests.post(raw_query_3)

    # printing results
    print(query_result_1.text)
    print(query_result_2.text)
    print(query_result_3.text)

    # states success
    if 'error' in query_result_2.text.split('"'):
        return 0
    if str(query_result_2) == '<Response [200]>':
        return 1


# How to get long lived AT
# GET "https://graph.facebook.com/{graph-api-version v00.0}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}"
#
# postman is great when you add the link above^
#
# All info found on this link:
# https://developers.facebook.com/apps/501954157599274/settings/basic/?business_id=2358898537739922
