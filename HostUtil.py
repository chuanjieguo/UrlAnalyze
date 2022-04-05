# -*- coding: utf-8 -*-
# @Time    : 2021-07-01 15:21
# @Author  : chuanjieguo
# @Mail    : chuanjieguo@139.com
from urllib import parse
import re
import time

debug = True

def log(str, file='log.txt'):
    '''
    记录日志
    :param str:
    :param file:
    :return:
    '''
    global debug
    if debug:
        with open(file, 'a+', encoding='utf-8') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + str + '\n')


def filterIpPostfix(str):
    '''
    过滤IP，如果是IP，则返回空字符串
    :param str:
    :return:
    '''
    str = str.strip('.').replace(':', '')
    try:
        i = int(str)
        return ''
    except:
        return str


def getFullHost(line):
    '''
    获取完整的域名
    :param line:
    :return: 如果成功，返回完整的域名，否则反馈空字符串
    '''
    le = line.strip().lower()
    if not le.startswith('http:') and not le.startswith('https:'):
        le = 'http://' + le
    try:
        p = parse.urlparse(url=le,scheme='http',allow_fragments=True)
    except:
        return ''
    return p.hostname


def getHost(line, count=0, index=0):
    '''
    获取域名相关信息
    :param line:
    :param count:
    :param index:
    :return: 返回三个值：二级域名，域名名字，域名级数，比如a.com为1级，a.com.cn为2级，如果提取域名失败，则为0
    '''
    # 返回三个值：二级域名，域名名字，域名级数，比如a.com为1级，a.com.cn为2级，如果提取域名失败，则为0
    # 通用顶级域名
    set1 = {
    '.co','.com','.net','.org','.gov','.mil','.edu','.biz','.info','.pro','.name','.coop','.travel','.xxx','.idv','.aero','.museum','.mobi','.asia','.tel','.int','.post','.jobs','.cat'
    }

    #国家地区及不常用的后缀
    set2 = {
    '.ac','.ad','.ae','.af','.ag','.ai','.al','.am','.an','.ao','.aq','.ar','.as','.at','.au','.aw','.az','.ba','.bb','.bd','.be','.bf','.bg','.bh','.bi','.bj','.bm','.bn','.bo','.br','.bs','.bt','.bv','.bw','.by','.bz','.ca','.cc','.cd','.cf','.cg','.ch','.ci','.ck','.cl','.cm','.cn','.co','.cr','.cu','.cv','.cx','.cy','.cz','.de','.dj','.dk','.dm','.do','.dz','.ec','.ee','.eg','.eh','.er','.es','.et','.eu','.fi','.fj','.fk','.fm','.fo','.fr','.ga','.gd','.ge','.gf','.gg','.gh','.gi','.gl','.gm','.gn','.gp','.gq','.gr','.gs','.gt','.gu','.gw','.gy','.hk','.hm','.hn','.hr','.ht','.hu','.id','.ie','.il','.im','.in','.io','.iq','.ir','.is','.it','.je','.jm','.jo','.jp','.ke','.kg','.kh','.ki','.km','.kn','.kp','.kr','.kw','.ky','.kz','.la','.lb','.lc','.li','.lk','.lr','.ls','.ma','.mc','.md','.me','.mg','.mh','.mk','.ml','.mm','.mn','.mo','.mp','.mq','.mr','.ms','.mt','.mu','.mv','.mw','.mx','.my','.mz','.na','.nc','.ne','.nf','.ng','.ni','.nl','.no','.np','.nr','.nu','.nz','.om','.pa','.pe','.pf','.pg','.ph','.pk','.pl','.pm','.pn','.pr','.ps','.pt','.pw','.py','.qa','.re','.ro','.ru','.rw','.sa','.sb','.sc','.sd','.se','.sg','.sh','.si','.sj','.sk','.sm','.sn','.so','.sr','.st','.sv','.sy','.sz','.tc','.td','.tf','.tg','.th','.tj','.tk','.tl','.tm','.tn','.to','.tp','.tr','.tt','.tv','.tw','.tz','.ua','.ug','.uk','.um','.us','.uy','.uz','.va','.vc','.ve','.vg','.vi','.vn','.vu','.wf','.ws','.ye','.yt','.yu','.yr','.za','.zm','.zw','.accountant','.club','.coach','.college','.company','.construction','.consulting','.contractors','.cooking','.corp','.credit','.creditcard','.dance','.dealer','.democrat','.dental','.dentist','.design','.diamonds','.direct','.doctor','.drive','.eco','.education','.energy','.engineer','.engineering','.equipment','.events','.exchange','.expert','.express','.faith','.farm','.farmers','.fashion','.finance','.financial','.fish','.fit','.fitness','.flights','.florist','.flowers','.food','.football','.forsale','.furniture','.game','.games','.garden','.gmbh','.golf','.health','.healthcare','.hockey','.holdings','.holiday','.home','.hospital','.hotel','.hotels','.house','.inc','.industries','.insurance','.insure','.investments','.islam','.jewelry','.justforu','.kid','.kids','.law','.lawyer','.legal','.lighting','.limited','.live','.llc','.llp','.loft','.ltd','.ltda','.managment','.marketing','.media','.medical','.men','.money','.mortgage','.moto','.motorcycles','.music','.mutualfunds','.ngo','.partners','.party','.pharmacy','.photo','.photography','.photos','.physio','.pizza','.plumbing','.press','.prod','.productions','.radio','.rehab','.rent','.repair','.report','.republican','.restaurant','.room','.rugby','.safe','.sale','.sarl','.save','.school','.secure','.security','.services','.shoes','.show','.soccer','.spa','.sport','.sports','.spot','.srl','.storage','.studio','.tattoo','.taxi','.team','.tech','.technology','.thai','.tips','.tour','.tours','.toys','.trade','.trading','.travelers','.university','.vacations','.ventures','.versicherung','.versicherung','.vet','.wedding','.wine','.winners','.work','.works','.yachts','.zone','.archi','.architect','.casa','.contruction','.estate','.haus','.house','.immo','.immobilien','.lighting','.loft','.mls','.realty','.academy','.arab','.bible','.care','.catholic','.charity','.christmas','.church','.college','.community','.contact','.degree','.education','.faith','.foundation','.gay','.halal','.hiv','.indiands','.institute','.irish','.islam','.kiwi','.latino','.mba','.meet','.memorial','.ngo','.phd','.prof','.school','.schule','.science','.singles','.social','.swiss','.thai','.trust','.university','.uno','.auction','.best','.bid','.boutique','.center','.cheap','.compare','.coupon','.coupons','.deal','.deals','.diamonds','.discount','.fashion','.forsale','.free','.gift','.gold','.gratis','.hot','.jewelry','.kaufen','.luxe','.luxury','.market','.moda','.pay','.promo','.qpon','.review','.reviews','.rocks','.sale','.shoes','.shop','.shopping','.store','.tienda','.top','.toys','.watch','.zero','.bar','.bio','.cafe','.catering','.coffee','.cooking','.diet','.eat','.food','.kitchen','.menu','.organic','.pizza','.pub','.rest','.restaurant','.vodka','.wine','.abudhabi','.africa','.alsace','.amsterdam','.barcelona','.bayern','.berlin','.boats','.booking','.boston','.brussels','.budapest','.caravan','.casa','.catalonia','.city','.club','.cologne','.corsica','.country','.cruise','.cruises','.deal','.deals','.doha','.dubai','.durban','.earth','.flights','.fly','.fun','.gent','.guide','.hamburg','.helsinki','.holiday','.hotel','.hoteles','.hotels','.ist','.istanbul','.joburg','.koeln','.land','.london','.madrid','.map','.melbourne','.miami','.moscow','.nagoya','.nrw','.nyc','.osaka','.paris','.party','.persiangulf','.place','.quebec','.reise','.reisen','.rio','.roma','.room','.ruhr','.saarland','.stockholm','.swiss','.sydney','.taipei','.tickets','.tirol','.tokyo','.tour','.tours','.town','.travelers','.vacations','.vegas','.wales','.wien','.world','.yokohama','.zuerich','.art','.auto','.autos','.baby','.band','.baseball','.beats','.beauty','.beknown','.bike','.book','.boutique','.broadway','.car','.cars','.club','.coach','.contact','.cool','.cricket','.dad','.dance','.date','.dating','.design','.dog','.events','.family','.fan','.fans','.fashion','.film','.final','.fishing','.football','.fun','.furniture','.futbol','.gallery','.game','.games','.garden','.gay','.golf','.guru','.hair','.hiphop','.hockey','.home','.horse','.icu','.joy','.kid','.kids','.life','.lifestyle','.like','.living','.lol','.makeup','.meet','.men','.moda','.moi','.mom','.movie','.movistar','.music','.party','.pet','.pets','.photo','.photography','.photos','.pics','.pictures','.play','.poker','.rodeo','.rugby','.run','.salon','.singles','.ski','.skin','.smile','.soccer','.social','.song','.soy','.sport','.sports','.star','.style','.surf','.tatoo','.tennis','.theater','.theatre','.tunes','.vip','.wed','.wedding','.win','.yoga','.you','.analytics','.antivirus','.app','.blog','.call','.camera','.channel','.chat','.click','.cloud','.computer','.contact','.data','.dev','.digital','.direct','.docs','.domains','.dot','.download','.email','.foo','.forum','.graphics','.guide','.help','.home','.host','.hosting','.idn','.link','.lol','.mail','.mobile','.network','.online','.open','.page','.phone','.pin','.search','.site','.software','.webcam','.airforce','.army','.black','.blue','.box','.buzz','.casa','.cool','.day','.discover','.donuts','.exposed','.fast','.finish','.fire','.fyi','.global','.green','.help','.here','.how','.international','.ira','.jetzt','.jot','.like','.live','.kim','.navy','.new','.news','.next','.ninja','.now','.one','.ooo','.pink','.plus','.red','.solar','.tips','.today','.weather','.wow','.wtf','.xyz','.abogado','.adult','.anquan','.aquitaine','.attorney','.audible','.autoinsurance','.banque','.bargains','.bcn','.beer','.bet','.bingo','.blackfriday','.bom','.boo','.bot','.broker','.builders','.business','.bzh','.cab','.cal','.cam','.camp','.cancerresearch','.capetown','.carinsurance','.casino','.ceo','.cfp','.circle','.claims','.cleaning','.clothing','.codes','.condos','.connectors','.courses','.cpa','.cymru','.dds','.delivery','.desi','.directory','.diy','.dvr','.ecom','.enterprises','.esq','.eus','.fail','.feedback','.financialaid','.frontdoor','.fund','.gal','.gifts','.gives','.giving','.glass','.gop','.got','.gripe','.grocery','.group','.guitars','.hangout','.homegoods','.homes','.homesense','.hotels','.ing','.ink','.juegos','.kinder','.kosher','.kyoto','.lat','.lease','.lgbt','.liason','.loan','.loans','.locker','.lotto','.love','.maison','.markets','.matrix','.meme','.mov','.okinawa','.ong','.onl','.origins','.parts','.patch','.pid','.ping','.porn','.progressive','.properties','.property','.protection','.racing','.read','.realestate','.realtor','.recipes','.rentals','.sex','.sexy','.shopyourway','.shouji','.silk','.solutions','.stroke','.study','.sucks','.supplies','.supply','.tax','.tires','.total','.training','.translations','.travelersinsurcance','.ventures','.viajes','.villas','.vin','.vivo','.voyage','.vuelos','.wang','.watches','.apple','.ax','.bing','.canon','.cash','.cyou','.lt','.lu','.lv','.ly','.moe','.monster','.ovh','.ren','.rs','.sncf','.space','.su','.systems','.tools','.toray','.website','.wiki','.xin','.google','.audio','.sl', '.video', '.tube'
    }
    le = line.strip().lower()
    if not le.startswith('http:') and not le.startswith('https:'):
        le = 'http://' + le
    try:
        p = parse.urlparse(url=le,scheme='http',allow_fragments=True)
    except:
        return '','',0
    l = p.hostname
    try:
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                            l) is not None:
            log("A\t{}\t{}\t{}".format(index, count, l))
            return l, l,0
    except:
        return '', '',0
    if l == '' or l is None:
        log("B\t{}\t{}\t{}".format(index, count, l))
        return '', '',0
    ri1 = l.rfind('.')
    ri2 = l.rfind('.', 0, ri1)
    if ri1 < 0:
        log("C\t{}\t{}\t{}".format(index, count, l))
        return '', '',0
    if ri2 > 0:
        pfix1 = l[ri2:ri1]
        pfix2 = l[ri1:]
        if pfix1 in set1:
            if pfix2 in set2:
                ri3 = l.rfind('.', 0, ri2)
                if ri3 < 0:
                    return l, l[0:ri2],2
                else:
                    return l[ri3+1:], l[ri3+1:ri2],2
            else:
                #非法域名
                log("D\t{}\t{}\t{}\t{}".format(index, count, l, filterIpPostfix(pfix2))) #abc.com.errorposfix
                return '', '',0
        elif pfix2 in set1 or pfix2 in set2:
            return l[ri2+1:], l[ri2+1:ri1],1
        else:
            #非法域名
            log("E\t{}\t{}\t{}\t{}".format(index, count, l, filterIpPostfix(pfix2)))
            return '', '',0
    else:
        pfix1 = l[ri1:]
        if pfix1 in set1 or pfix1 in set2:  # .abc.com  abc.cn  abc.hk
            return l.strip('.'), (l[0:ri1]).strip('.'),1
        else:
            #非法域名
            log("F\t{}\t{}\t{}\t{}".format(index, count, l, filterIpPostfix(pfix1)))
            return '', '',0
    return '', '',0

def getHost2(line):
    '''
    获取域名相关信息
    :param line:
    :return: 返回三个值：二级域名，域名名字，域名级数，比如a.com为1级，a.com.cn为2级，如果提取域名失败，则为0
    '''
    # 返回三个值：二级域名，整体域名，域名级数，比如a.com为1级，a.com.cn为2级，如果提取域名失败，则为0
    # 通用顶级域名
    set1 = {
    '.co','.com','.net','.org','.gov','.mil','.edu','.biz','.info','.pro','.name','.coop','.travel','.xxx','.idv','.aero','.museum','.mobi','.asia','.tel','.int','.post','.jobs','.cat'
    }

    #国家地区及不常用的后缀
    set2 = {
    '.ac','.ad','.ae','.af','.ag','.ai','.al','.am','.an','.ao','.aq','.ar','.as','.at','.au','.aw','.az','.ba','.bb','.bd','.be','.bf','.bg','.bh','.bi','.bj','.bm','.bn','.bo','.br','.bs','.bt','.bv','.bw','.by','.bz','.ca','.cc','.cd','.cf','.cg','.ch','.ci','.ck','.cl','.cm','.cn','.co','.cr','.cu','.cv','.cx','.cy','.cz','.de','.dj','.dk','.dm','.do','.dz','.ec','.ee','.eg','.eh','.er','.es','.et','.eu','.fi','.fj','.fk','.fm','.fo','.fr','.ga','.gd','.ge','.gf','.gg','.gh','.gi','.gl','.gm','.gn','.gp','.gq','.gr','.gs','.gt','.gu','.gw','.gy','.hk','.hm','.hn','.hr','.ht','.hu','.id','.ie','.il','.im','.in','.io','.iq','.ir','.is','.it','.je','.jm','.jo','.jp','.ke','.kg','.kh','.ki','.km','.kn','.kp','.kr','.kw','.ky','.kz','.la','.lb','.lc','.li','.lk','.lr','.ls','.ma','.mc','.md','.me','.mg','.mh','.mk','.ml','.mm','.mn','.mo','.mp','.mq','.mr','.ms','.mt','.mu','.mv','.mw','.mx','.my','.mz','.na','.nc','.ne','.nf','.ng','.ni','.nl','.no','.np','.nr','.nu','.nz','.om','.pa','.pe','.pf','.pg','.ph','.pk','.pl','.pm','.pn','.pr','.ps','.pt','.pw','.py','.qa','.re','.ro','.ru','.rw','.sa','.sb','.sc','.sd','.se','.sg','.sh','.si','.sj','.sk','.sm','.sn','.so','.sr','.st','.sv','.sy','.sz','.tc','.td','.tf','.tg','.th','.tj','.tk','.tl','.tm','.tn','.to','.tp','.tr','.tt','.tv','.tw','.tz','.ua','.ug','.uk','.um','.us','.uy','.uz','.va','.vc','.ve','.vg','.vi','.vn','.vu','.wf','.ws','.ye','.yt','.yu','.yr','.za','.zm','.zw','.accountant','.club','.coach','.college','.company','.construction','.consulting','.contractors','.cooking','.corp','.credit','.creditcard','.dance','.dealer','.democrat','.dental','.dentist','.design','.diamonds','.direct','.doctor','.drive','.eco','.education','.energy','.engineer','.engineering','.equipment','.events','.exchange','.expert','.express','.faith','.farm','.farmers','.fashion','.finance','.financial','.fish','.fit','.fitness','.flights','.florist','.flowers','.food','.football','.forsale','.furniture','.game','.games','.garden','.gmbh','.golf','.health','.healthcare','.hockey','.holdings','.holiday','.home','.hospital','.hotel','.hotels','.house','.inc','.industries','.insurance','.insure','.investments','.islam','.jewelry','.justforu','.kid','.kids','.law','.lawyer','.legal','.lighting','.limited','.live','.llc','.llp','.loft','.ltd','.ltda','.managment','.marketing','.media','.medical','.men','.money','.mortgage','.moto','.motorcycles','.music','.mutualfunds','.ngo','.partners','.party','.pharmacy','.photo','.photography','.photos','.physio','.pizza','.plumbing','.press','.prod','.productions','.radio','.rehab','.rent','.repair','.report','.republican','.restaurant','.room','.rugby','.safe','.sale','.sarl','.save','.school','.secure','.security','.services','.shoes','.show','.soccer','.spa','.sport','.sports','.spot','.srl','.storage','.studio','.tattoo','.taxi','.team','.tech','.technology','.thai','.tips','.tour','.tours','.toys','.trade','.trading','.travelers','.university','.vacations','.ventures','.versicherung','.versicherung','.vet','.wedding','.wine','.winners','.work','.works','.yachts','.zone','.archi','.architect','.casa','.contruction','.estate','.haus','.house','.immo','.immobilien','.lighting','.loft','.mls','.realty','.academy','.arab','.bible','.care','.catholic','.charity','.christmas','.church','.college','.community','.contact','.degree','.education','.faith','.foundation','.gay','.halal','.hiv','.indiands','.institute','.irish','.islam','.kiwi','.latino','.mba','.meet','.memorial','.ngo','.phd','.prof','.school','.schule','.science','.singles','.social','.swiss','.thai','.trust','.university','.uno','.auction','.best','.bid','.boutique','.center','.cheap','.compare','.coupon','.coupons','.deal','.deals','.diamonds','.discount','.fashion','.forsale','.free','.gift','.gold','.gratis','.hot','.jewelry','.kaufen','.luxe','.luxury','.market','.moda','.pay','.promo','.qpon','.review','.reviews','.rocks','.sale','.shoes','.shop','.shopping','.store','.tienda','.top','.toys','.watch','.zero','.bar','.bio','.cafe','.catering','.coffee','.cooking','.diet','.eat','.food','.kitchen','.menu','.organic','.pizza','.pub','.rest','.restaurant','.vodka','.wine','.abudhabi','.africa','.alsace','.amsterdam','.barcelona','.bayern','.berlin','.boats','.booking','.boston','.brussels','.budapest','.caravan','.casa','.catalonia','.city','.club','.cologne','.corsica','.country','.cruise','.cruises','.deal','.deals','.doha','.dubai','.durban','.earth','.flights','.fly','.fun','.gent','.guide','.hamburg','.helsinki','.holiday','.hotel','.hoteles','.hotels','.ist','.istanbul','.joburg','.koeln','.land','.london','.madrid','.map','.melbourne','.miami','.moscow','.nagoya','.nrw','.nyc','.osaka','.paris','.party','.persiangulf','.place','.quebec','.reise','.reisen','.rio','.roma','.room','.ruhr','.saarland','.stockholm','.swiss','.sydney','.taipei','.tickets','.tirol','.tokyo','.tour','.tours','.town','.travelers','.vacations','.vegas','.wales','.wien','.world','.yokohama','.zuerich','.art','.auto','.autos','.baby','.band','.baseball','.beats','.beauty','.beknown','.bike','.book','.boutique','.broadway','.car','.cars','.club','.coach','.contact','.cool','.cricket','.dad','.dance','.date','.dating','.design','.dog','.events','.family','.fan','.fans','.fashion','.film','.final','.fishing','.football','.fun','.furniture','.futbol','.gallery','.game','.games','.garden','.gay','.golf','.guru','.hair','.hiphop','.hockey','.home','.horse','.icu','.joy','.kid','.kids','.life','.lifestyle','.like','.living','.lol','.makeup','.meet','.men','.moda','.moi','.mom','.movie','.movistar','.music','.party','.pet','.pets','.photo','.photography','.photos','.pics','.pictures','.play','.poker','.rodeo','.rugby','.run','.salon','.singles','.ski','.skin','.smile','.soccer','.social','.song','.soy','.sport','.sports','.star','.style','.surf','.tatoo','.tennis','.theater','.theatre','.tunes','.vip','.wed','.wedding','.win','.yoga','.you','.analytics','.antivirus','.app','.blog','.call','.camera','.channel','.chat','.click','.cloud','.computer','.contact','.data','.dev','.digital','.direct','.docs','.domains','.dot','.download','.email','.foo','.forum','.graphics','.guide','.help','.home','.host','.hosting','.idn','.link','.lol','.mail','.mobile','.network','.online','.open','.page','.phone','.pin','.search','.site','.software','.webcam','.airforce','.army','.black','.blue','.box','.buzz','.casa','.cool','.day','.discover','.donuts','.exposed','.fast','.finish','.fire','.fyi','.global','.green','.help','.here','.how','.international','.ira','.jetzt','.jot','.like','.live','.kim','.navy','.new','.news','.next','.ninja','.now','.one','.ooo','.pink','.plus','.red','.solar','.tips','.today','.weather','.wow','.wtf','.xyz','.abogado','.adult','.anquan','.aquitaine','.attorney','.audible','.autoinsurance','.banque','.bargains','.bcn','.beer','.bet','.bingo','.blackfriday','.bom','.boo','.bot','.broker','.builders','.business','.bzh','.cab','.cal','.cam','.camp','.cancerresearch','.capetown','.carinsurance','.casino','.ceo','.cfp','.circle','.claims','.cleaning','.clothing','.codes','.condos','.connectors','.courses','.cpa','.cymru','.dds','.delivery','.desi','.directory','.diy','.dvr','.ecom','.enterprises','.esq','.eus','.fail','.feedback','.financialaid','.frontdoor','.fund','.gal','.gifts','.gives','.giving','.glass','.gop','.got','.gripe','.grocery','.group','.guitars','.hangout','.homegoods','.homes','.homesense','.hotels','.ing','.ink','.juegos','.kinder','.kosher','.kyoto','.lat','.lease','.lgbt','.liason','.loan','.loans','.locker','.lotto','.love','.maison','.markets','.matrix','.meme','.mov','.okinawa','.ong','.onl','.origins','.parts','.patch','.pid','.ping','.porn','.progressive','.properties','.property','.protection','.racing','.read','.realestate','.realtor','.recipes','.rentals','.sex','.sexy','.shopyourway','.shouji','.silk','.solutions','.stroke','.study','.sucks','.supplies','.supply','.tax','.tires','.total','.training','.translations','.travelersinsurcance','.ventures','.viajes','.villas','.vin','.vivo','.voyage','.vuelos','.wang','.watches','.apple','.ax','.bing','.canon','.cash','.cyou','.lt','.lu','.lv','.ly','.moe','.monster','.ovh','.ren','.rs','.sncf','.space','.su','.systems','.tools','.toray','.website','.wiki','.xin','.google','.audio','.sl', '.video', '.tube'
    }
    le = line.strip().lower()
    if not le.startswith('http:') and not le.startswith('https:'):
        le = 'http://' + le
    try:
        p = parse.urlparse(url=le,scheme='http',allow_fragments=True)
    except:
        return '','',0
    l = p.hostname
    try:
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                            l) is not None:
            return l, l,0
    except:
        return '', '',0
    if l == '' or l is None:
        return '', '',0
    ri1 = l.rfind('.')
    ri2 = l.rfind('.', 0, ri1)
    if ri1 < 0:
        return '', '',0
    if ri2 > 0:
        pfix1 = l[ri2:ri1]
        pfix2 = l[ri1:]
        if pfix1 in set1:
            if pfix2 in set2:
                ri3 = l.rfind('.', 0, ri2)
                if ri3 < 0:
                    return l, l,2
                else:
                    return l[ri3+1:], l,2
            else:
                #非法域名
                return '', '',0
        elif pfix2 in set1 or pfix2 in set2:
            return l[ri2+1:], l,1
        else:
            return '', '',0
    else:
        pfix1 = l[ri1:]
        if pfix1 in set1 or pfix1 in set2:  # .abc.com  abc.cn  abc.hk
            return l.strip('.'), l.strip('.'),1
        else:
            return '', '',0
    return '', '',0