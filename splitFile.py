
with open("http_detail_converse_loc_redis.txt", 'r', encoding='utf-8') as f:
    for line in f:
        ls = line.split('\t')
        l = len(ls)
        tmp = ''
        for i in range(l):
            if i % 6 ==  0:
                print(tmp)
                tmp = ''
            tmp += "{}\t".format(ls[i])
