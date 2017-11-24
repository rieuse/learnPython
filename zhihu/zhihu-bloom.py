import multiprocessing
import pymongo
import requests
import threadpool
import time
from lxml import etree
import random
import redis
from pybloom import BloomFilter

import sys

sys.setrecursionlimit(100000000)
clients = pymongo.MongoClient('localhost')
db = clients["zhihu"]
col1 = db["person"]
col2 = db["answers"]
col3 = db["question"]
col4 = db["article"]
col5 = db["user_id"]

filter = BloomFilter(capacity=5 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据


def add_bloom_from_mongo():
    print('add user_id to bloomfilter form mongodb')
    for i in col5.find():
        filter.add(i['user_id'])
    print('over')


proxies = {
    'http': "http://HI754098W055I8BD:C3537F5006B483C5@http-dyn.abuyun.com:9020",
    'https': "http://HI754098W055I8BD:C3537F5006B483C5@http-dyn.abuyun.com:9020"
}
UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {
    'authorization': 'Bearer Mi4xRGV3U0FBQUFBQUFBRU1MOWFFRTVEQmNBQUFCaEFsVk5EU3U2V1FBcFEzRkhFQldYYlFCc00zVzJFek4wSG5XTW5R|1502780941|2997c5bc19279d25296fe7c5242bfef494915487',
    'User-Agent': random.choice(UA_LIST)
}


def to_redis(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    # print("{} into redis".format(data))
    r.sadd("zhihu_user_id", '{}'.format(data))


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("zhihu_user_id")
    return po


def to_redis_error(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("zhihu_user_id_error", '{}'.format(data))


def get_person(user_id):
    # r = redis.StrictRedis(host='127.0.0.1',port=6379, decode_responses=True)
    # time.sleep(1)
    if not user_id in filter:
        start_url = 'https://www.zhihu.com/api/v4/members/{}?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics'.format(
            user_id)
        data = requests.get(start_url, headers=headers, proxies=proxies).json()
        person = data
        if person:
            print(person['name'])
        col1.insert(person)
        user_id = person['url_token']
        answer_url = 'https://www.zhihu.com/api/v4/members/{}/answers?include=data[*].comment_count,content,voteup_count,created_time,updated_time;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0'.format(
            user_id)
        get_answers(answer_url, user_id)
        question_url = 'https://www.zhihu.com/api/v4/members/{}/questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&limit=20&offset=0'.format(
            user_id)
        get_question(question_url, user_id)
        article_url = 'https://www.zhihu.com/api/v4/members/{}/articles?include=data[*].comment_count,content,voteup_count,created,updated;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0'.format(
            user_id)
        get_article(article_url, user_id)
        dic = {'user_id': user_id}
        col5.insert(dic)
        filter.add(user_id)
        next_person_url = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'.format(
            user_id)
        next_person(next_person_url, user_id)
    else:
        print('---user_id exist---')


def get_answers(url, user_id):
    time.sleep(0.1)
    try:
        # url = 'https://www.zhihu.com/api/v4/members/{}/answers?include=data[*].comment_count,content,voteup_count,created_time,updated_time;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0'.format(user_id)
        answers_data = requests.get(url, headers=headers, proxies=proxies).json()
    except Exception as e:
        print(e)
        answers_data = requests.get(url, headers=headers).json()
    total_number = int(answers_data['paging']['totals'])
    answers = []
    for i in answers_data['data']:
        answers.append(i)
    if not answers == []:
        print(answers)
        col2.insert(answers)
        if total_number > 21:
            next_page = answers_data['paging']['next']
            get_answers(next_page, user_id)


def get_question(url, user_id):
    # time.sleep(0.6)
    try:
        question_data = requests.get(url, headers=headers, proxies=proxies).json()
    except Exception as e:
        print(e)
        question_data = requests.get(url, headers=headers).json()
    total_number = int(question_data['paging']['totals'])
    question = []
    for i in question_data['data']:
        question.append(i)
    if not question == []:
        print(question)
        col3.insert(question)
        if total_number > 21:
            next_page = question_data['paging']['next']
            get_question(next_page, user_id)


def get_article(url, user_id):
    try:
        article_data = requests.get(url, headers=headers, proxies=proxies).json()
    except Exception as e:
        article_data = requests.get(url, headers=headers, proxies=proxies).json()
        print(e)
    total_number = int(article_data['paging']['totals'])
    article = []
    for i in article_data['data']:
        article.append(i)
    if not article == []:
        print(article)
        col4.insert(article)
        if total_number > 21:
            next_page = article_data['paging']['next']
            get_article(next_page, user_id)
    filter.add(user_id)


def gen(data):
    for i in data:
        yield i['url_token']


def next_person(next_person_url, user_id):
    # url = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'.format(user_id)
    try:
        follow_data = requests.get(next_person_url, headers=headers, proxies=proxies).json()
    except:
        follow_data = requests.get(next_person_url, headers=headers, proxies=proxies).json()

    # for i in follow_data:
    #     print(i['url_token'])
    def gen(data):
        for i in data:
            yield i['url_token']

    for i in gen(follow_data['data']):
        get_person(i)
    total_number = int(follow_data['paging']['totals'])
    if total_number > 21:
        next_page = follow_data['paging']['next']
        next_person(next_page, user_id)
        # to_redis(i['url_token'])


def main(url, user_id):
    # url = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'.format(user_id)
    follow_data = requests.get(url, headers=headers, proxies=proxies).json()
    ids = []
    for i in follow_data['data']:
        u_id = i['url_token']
        if not u_id in filter:
            ids.append(u_id)
            print(u_id)
        else:
            print('user_id exist')
    thread_main(ids)
    total_number = int(follow_data['paging']['totals'])
    if total_number > 21:
        next_page = follow_data['paging']['next']
        main(next_page, user_id)


def thread_main(item):
    pool = threadpool.ThreadPool(20)
    tasks = threadpool.makeRequests(get_person, item)
    [pool.putRequest(req) for req in tasks]
    pool.wait()


def multipro_main(item):
    pool = multiprocessing.Pool(1)
    pool.map(get_person, item)
    pool.close()
    pool.join()


def get_one_id(id):
    url = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'.format(
        id)
    try:
        follow_data = requests.get(url, headers=headers, proxies=proxies).json()['data']
    except:
        follow_data = requests.get(url, headers=headers).json()['data']
    for i in follow_data:
        user_id = i['url_token']
        if not user_id in filter:
            print(user_id)
            with open('new_user_id.txt', 'a') as f:
                f.write(user_id + '\n')
                # return user_id


if __name__ == '__main__':
    add_bloom_from_mongo()
    start_id = 'jacky-yang-30'
    main_url = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'.format(
        start_id)
    main(main_url, start_id)
    # user_id = 'hi-id'
    # get_person(user_id)
    # strat_user_ids = ['windleavez','wang-doris-86', 'jasmine-huang-61','wen-sen-te-15-29','joy-cai-14', 'missxiaoxiaowu', 'jianwei', 'Nailon', 'rebor', 'wxyyxc', 'winterland','mili', 'onenew']
    # thread_main(strat_user_ids)
