with open('lvyou.log', 'r') as f:
    ls = f.readlines()
    last_url = ls[-1][42:-1]
    print(last_url)
