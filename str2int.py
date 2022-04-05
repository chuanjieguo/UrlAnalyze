import random

i = 3
print(i.__sizeof__())

i = 123456789012345678
print(i.__sizeof__())

i = 'qd990.com'
print(i.__sizeof__())

# 要从10开始
il = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_.~!*\'();:@&=+$,/?#[]'
ibase = 10
ii = list(range(ibase, ibase + len(il)))
id = dict(zip(il, ii))



def ip2int(ip):
    sl = []
    for i in ip:
        ii = id.get(i)
        if ii is None:
            return None
        else:
            sl.append("{:02d}".format(ii))
    str = "".join(sl)
    return int(str)


def int2ip(v):
    vs = "{:d}".format(v)
    l = round(len(vs)/2)
    sl = []
    for i in range(l):
        st = vs[i*2:i*2+2]
        sl.append(il[int(st)-ibase])
    return "".join(sl)

ul = [
'49208.com',
'1875444.com',
'1875444.com?10&r',
'311155.com',
'87559.com',
'zl246.com',
'49208b.com',
'admin.providesupport.com',
'0.12333gd.c',
'0.27844b.com:2784',
'0.27844b.com:27844',
'0.4our-health.com',
'0.gadmz.com',
'0.jdzs668.com',
'0.lubukseni.co',
'0.movies-house.com',
'0.sj0453.com',
'0.xiao0571.com',
'0.ygdxzz.cn',
'00.lizhelaixi.com',
'00.quttao.com',
'00.xinwenzazhi.com',
'00.ygdxzz.cn',
'0000000.imagesbyanthonyphotography.co',
'0000000145.com',
'000000bet.com',
'0000033.com',
'000004331.com',
'0000088hg.com',
'000009114.com',
'00000vs.com',
'00000w.com',
'0000193.com',
'00002337.com',
'00003658.com',
'00004.cc',
'00004048.com',
'00004906.com',
'000051a.com',
'000051c.com',
'0000599.com',
'00006.educ22.com',
'00006277.com',
'00006801.com',
'00006802.com',
'00006803.com',
'00006804.com',
'00006805.com',
'00006806.com',
'00006807.com',
'00006808.com',
'00006809.com',
'00006810.com',
'00006811.com',
'0000799.com',
'000082.com',
'0000836.com',
'0000868.com',
'000088807.com',
'000088hd.com',
'000088hg.com',
'00009365.com',
'0000996.com',
'0000998.com',
'0000999.net',
'0000999.vip',
'0000aaa.c',
'0000aaa.cc',
'0000bmw.com',
'0000hui.com',
'0000lh.c',
'0000lh.cc',
'0000p6.cc',
'0001213.com',
'0001353.com',
'00016365.co',
'0001678.com',
'0001705.com',
'0001wns.com',
'0001zzz.com',
'00023a.com',
'00023b.com',
'00023c.com',
'00023dl.com',
'000249.com',
'00025.com',
'0002737.app',
'00028a1.com',
'00028a2.com',
'00028a3.com',
'00028a4.com',
'00028a5.com',
'00028a6.com',
'00028a7.com',
'00028a8.com',
'00028a9.com',
'00028b1.com',
'00028b2.com',
'00028b3.com',
'00028s.com',
'0002wns.com',
'0002zzz.com',
'0003055.com',
'0003245.com',
'000333.co',
'0003345.com',
'00034.com',
'000340.com',
'0003599.com',
'00035bb.club',
'00035bb.live',
'00037w.co',
'00037w.com',
'00038.com',
'00039.net',
'0003955.com',
'0003wns.com',
'0003zzz.com',
'0004048.com',
'000410.co',
'000410.com',
'0004270.com',
'000434.com',
'000435.co',
'000435.com',
'000438.com',
'0004384.com',
'000443.co',
'000443.com',
'000449.co',
'000449.com',
'000457.com',
'000459.com',
'0004717.com',
'000494.com',
'0004975.com',
'0004wns.com',
'0004zzz.com',
'0005296.com',
'0005396.com',
'00054.com',
'000542.com',
'0005433.com',
'00055508.com',
'00055545.com',
'00055626.com',
'0005682.com',
'0005824.com',
'0005889.co',
'0005889.com',
'00059333.com',
'0005wns.com',
'0005zzz.com',
'00062188.com',
'000640.co',
'000640.com',
'0006555.com',
'00066.net',
'00066024.com',
'00066025.com',
'00066035.com',
'00066040.com',
'00066059.com',
'000663365.com',
'0006688.com',
'0006689.com',
'00066hb.com',
'00066jc.com',
'00066vip.com',
'00066yh.com',
'00067365.com',
'00068f.com',
'0006wns.com',
'00070.cc',
'0007148.com',
'000724.co',
'000724.com',
'00075365.com',
'000765.net',
'00076543.com',
'000772.com',
'000779.com',
'0007wns.com',
'00081fec30ebd.chatnow.mstatik.com',
'00083.net',
'000840.co',
'000840.com',
'000870.co',
'000870.com',
'000873.com',
'00088806.com',
'00088807.com',
'0008881.com',
'0008882.com',
'0008883.com',
'0008884.com',
'0008885.com',
'0008887.com',
'000888888000.com',
'0008899.com'
]
isum = 0
ssum = 0
tdic = {}
idic = {}
with open(r'20210113.txt', 'r', encoding='utf-8') as file:
#with open(r'7700000.txt', 'r', encoding='utf-8') as file:
    i = 0
    for line in file:
        i += 1
        if i == 50:
            break
        es = line.split(',')
        if len(es) != 4:
            print("not 4 " + line)
            continue
        else:
            u = es[0]
            ssum += u.__sizeof__()
            i = ip2int(u)
            tdic[i] = random.randint(1, 10000)
            idic[u] = random.randint(1, 10000)
            isum += i.__sizeof__()
            #print(i)
            s = int2ip(i)
            if u != s:
                print("{} {} {}".format(u, i, s))
            #print(s)

print(isum)
print(ssum)
print(idic.__sizeof__())
print(tdic.__sizeof__())