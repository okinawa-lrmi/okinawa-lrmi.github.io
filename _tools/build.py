# -*- coding: utf-8 -*-
"""サイトの全ページを作り直すスクリプト。
使い方:  python _tools/build.py   （サイトのフォルダで実行）
文章を直すときはこのファイルの中身を書き換えてから実行する。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://okinawa-lrmi.github.io/'
ORG = 'おきなわ長寿復興・医療イノベーション研究所'
ORG_WBR = 'おきなわ長寿復興・<wbr>医療イノベーション<wbr>研究所'  # 見出し用（折り返し位置つき）
ORG_FULL = '一般社団法人 ' + ORG
ZIP = '〒901-2214'
ADDR = '沖縄県宜野湾市我如古4-4-2 613'
TEL = '080-6485-5626'
MAIL = 'okinawa.lrmi@gmail.com'
DESC = ORG + 'では沖縄県における次世代の地域医療に関する事業、調査、政策提言を行っています。'


def enc(t):
    """迷惑メール対策としてメールアドレスを文字参照に変える"""
    return ''.join('&#%d;' % ord(c) for c in t)


MAIL_E = enc(MAIL)
MAILTO = enc('mailto:' + MAIL)
TEL_HREF = 'tel:' + TEL.replace('-', '')

# リンク欄・リンクページを出すかどうか（今は中身がないので隠している。True にすると復活する）
SHOW_LINKS = False

NAV = [
    ('index.html', 'トップページ'),
    ('facilities.html', '研究所案内'),
    ('plan.html', '受託案件'),
    ('news.html', '新着情報'),
    ('link.html', 'リンク'),
    ('contact.html', 'お問合せ'),
]

if not SHOW_LINKS:
    NAV = [n for n in NAV if n[0] != 'link.html']

# 新着情報（新しいものを上に書く）
# （日付, 表示用の日付, ページのファイル名, 見出し, 本文HTML）
NEWS = [
    ('2026-11-15', '2026.11.15', '20261115.html', 'Webサイトをリニューアルしました。',
     '<p>おきなわ長寿復興・医療イノベーション研究所のWebサイトをリニューアルしました。</p>'),
    ('2016-02-24', '2016.02.24', '20150320.html', '「医療情報利用推進セミナー」を開催します。',
     '<p>詳しくは<a href="content/files/20160224-075621.pdf">こちら</a>（PDF）</p>'),
    ('2015-03-19', '2015.03.19', '20150319.html', 'ウェブサイトを公開しました。',
     '<p>おきなわ長寿復興・医療イノベーション研究所のウェブサイトを公開しました。</p>'),
]

LINKS = [
    ('http://ganju-with-you.com/', 'がんじゅー With You　共同企業体',
     '情報通信技術を利用・活用することによって、高齢者の効率的な健康管理の実現、健康意識の改善、離島生活における不安の軽減が実現するかを検証しています。'),
    ('http://www.yuima-ru.med.u-ryukyu.ac.jp/', 'ゆい健康プロジェクト（健康行動実践モデル実証事業）',
     '学童と高齢者への食に対する情報提供と食事介入で地域の健康行動を向上させ、生活習慣病改善で沖縄県民の健康と長寿を促進することを目標としております。'),
]

FONTS = ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500'
         '&amp;family=Shippori+Mincho:wght@500;700&amp;display=swap')


def head(title, desc, path):
    full = ORG_FULL if not title else title + '｜' + ORG_FULL
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%s">
<link rel="stylesheet" href="assets/css/style.css">
</head>
""" % (full, desc, BASE, '' if path == 'index.html' else path, FONTS)


def header(current, home=False):
    items = ''.join('<li><a href="%s"%s>%s</a></li>\n' % (h, ' aria-current="page"' if h == current else '', t)
                    for h, t in NAV)
    return """<body%s>
<header class="hd">
<div class="wrap">
<a class="brand" href="index.html"><small>一般社団法人</small><strong>%s</strong></a>
<button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false">Menu</button>
<nav aria-label="メインメニュー">
<ul class="nav" id="nav">
%s</ul>
</nav>
</div>
</header>
""" % (' class="home"' if home else '', ORG_WBR, items)


def footer():
    return """<footer class="ft">
<div class="wrap">
<address><b>%s</b><span>%s %s</span><span>TEL：<a href="%s">%s</a></span><span>MAIL：<a href="%s">%s</a></span></address>
<p class="copy">Copyright &copy; %s. All rights reserved.</p>
</div>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
""" % (ORG_FULL, ZIP, ADDR, TEL_HREF, TEL, MAILTO, MAIL_E, ORG_FULL)


def page(path, title, en, desc, body, crumbs=None):
    c = '<li><a href="index.html">トップページ</a></li>'
    for h, t in (crumbs or []):
        c += '<li><a href="%s">%s</a></li>' % (h, t)
    c += '<li>%s</li>' % title
    cur = crumbs[0][0] if crumbs else path
    html = head(title, desc, path) + header(cur) + '''<main>
<div class="wrap">
<ul class="crumbs">%s</ul>
<div class="page-hd">
<p class="en">%s</p>
<h1>%s</h1>
</div>
</div>
<div class="wrap page">
<div class="prose">
%s
</div>
</div>
</main>
''' % (c, en, title, body) + footer()
    write(path, html)


def write(path, html):
    with io.open(os.path.join(ROOT, path), 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('作成:', path)


def news_items(items):
    return ''.join('<li><time datetime="%s">%s</time><a href="%s">%s</a></li>\n' % n[:4] for n in items)


# ---------- トップページ ----------
def build_index():
    html = head('', DESC, 'index.html') + header('index.html', home=True) + """<main>
<section class="hero">
<div class="wrap">
<picture>
<source srcset="assets/img/keyvisual.webp" type="image/webp">
<img class="hero-art" src="assets/img/keyvisual.jpg" alt="ガジュマルの大樹とハイビスカス、遠くに島の見える海を描いた線画" width="1510" height="850">
</picture>
<div class="hero-text">
<p class="hero-sub">Okinawa LRMI</p>
<h1 class="hero-main"><span>沖縄県における</span><span>次世代の地域医療に関する</span><span>事業、調査、政策提言を</span><span>行っています。</span></h1>
<div class="hero-cta">
<a class="more" href="facilities.html">研究所案内</a>
<figure class="qr"><img src="assets/img/qr.svg" alt="このサイトのQRコード" width="80" height="80"><figcaption>スマートフォンで<br>ご覧いただけます</figcaption></figure>
</div>
</div>
</div>
</section>

<section class="newsbar">
<div class="wrap">
<div class="newsbar-hd">
<h2><span class="en">News</span><span class="ja">新着情報</span></h2>
<a class="more" href="news.html">すべて表示</a>
</div>
<ul class="news">
%s</ul>
<a class="more" href="news.html">すべて表示</a>
</div>
</section>
</main>
""" % news_items(NEWS[:3]) + footer()
    write('index.html', html)


# ---------- 研究所案内 ----------
def people(rows):
    return '<ul class="people">\n' + ''.join('<li><span>%s</span>%s</li>\n' % r for r in rows) + '</ul>'


def build_facilities():
    officers = people([('業務執行理事', '大屋祐輔'), ('監事', '田名毅'), ('監事', '又吉哲太郎'),
                       ('理事', '玉城信光'), ('理事', '宮里達也')])
    members = people([('設立時社員', '崎間敦'), ('設立時社員', '東上里康司'), ('設立時社員', '又吉哲太郎'),
                      ('設立時社員', '横田勝彦'), ('社員', '岩淵成志'), ('社員', '梅村武寛'), ('社員', '奥村耕一郎'),
                      ('社員', '白井こころ'), ('社員', '等々力英美')])
    staff = people([('総務', '末吉未央'), ('システム・コーディネーター', '樽川智亜希')]).replace('class="people"', 'class="people people-wide"')
    body = '''<h2>代表挨拶</h2>
<p>一般社団法人おきなわ長寿復興・医療イノベーション研究所の理事を代表して、一言ご挨拶と本研究所開設の趣旨についてお話しいたします。</p>
<p>本研究所は、医療分野でのイノベーションとなる新技術の開発支援を通して、沖縄県の地域産業振興に貢献するという目的のもとに設立されました。</p>
<p>これまで、全国1位を誇ってきた男性の平均寿命が1990年に5位となり95年に4位、2000年に26位へ後退したいわゆる26ショックに続き、今年2月には女性の平均寿命も全国1位の座から陥落するという事態を迎え、県民の健康水準の低下が大きな社会的関心を集めているところです。県民の保健衛生の低下は、県民自身の生活はもちろんのこと、医療機関における業務負担の増大や、これまで健康長寿県のポジティブイメージの恩恵を被ってきた観光産業や食品産業への影響も懸念されます。</p>
<p>また、沖縄県の健康問題は日本本土を先取りしていると言われており、現在沖縄県が直面している医療課題は将来本土が直面するものと考えられます。そこで、沖縄県の医療をモデルに、将来の日本の医療を変えるような、新しい技術、サービスを開発していく。そして、（いつの日か、）再び長寿日本一を奪還する。そうした取り組みを県内の医療者、企業、大学、自治体、さらには中央官庁も一体となって支援していこうと考えております。</p>
<p>私は、医療分野においては専門ではありませんが、経験を生かして、これまで行政や産業界での経験を生かして、取り組む所存です。</p>
<p>ご助言、ご協力を頂けますようよろしくお願い申し上げます。</p>

<h2>事業内容</h2>
<ul class="list">
<li>地域医療情報に関する調査事業</li>
<li>離島医療における調査事業</li>
<li>医療機器開発に関する調査支援事業</li>
<li>地域医療における研究報告会・講習会の開催</li>
<li>医・工連携による地域産官学連携推進事業</li>
<li>関係省庁との情報交換と連携推進事業</li>
<li>ホームページやソーシャル・ネットワーキング・サービスによる情報配信</li>
<li>その他この法人の目的を達成するために必要な事業</li>
</ul>

<h2>研究所概要</h2>
<dl class="outline">
<div><dt>会社名</dt><dd>%s</dd></div>
<div><dt>代表理事</dt><dd>牧野浩隆</dd></div>
<div><dt>所在地</dt><dd>%s<br>%s</dd></div>
<div><dt>設立</dt><dd>2014年7月1日</dd></div>
<div><dt>資本金</dt><dd>0円</dd></div>
<div><dt>役員</dt><dd>
%s
</dd></div>
<div><dt>社員</dt><dd>
%s
</dd></div>
<div><dt>事務局</dt><dd>
%s
</dd></div>
</dl>''' % (ORG_FULL, ZIP, ADDR, officers, members, staff)
    page('facilities.html', '研究所案内', 'About',
         ORG + 'の事業内容など、研究所のご案内をしています。', body)


# ---------- 受託案件 ----------
def build_plan():
    # 新しい案件を上に書く
    rows = [
        ('琉球歴史文化コンテンツ創出支援事業 / 御冠船ダイニング～日本遺産「守礼の心」でもてなす、琉球官邸料理を現代に再解釈する体験型コンテンツ創出事業～（令和8年～継続中）', []),
        ('遠隔医療連携構築支援事業 / 沖縄急性期疾患診療ネットワーク　次世代連携拡張事業（令和6年～継続中）', []),
        ('実験及び研究開発',
         ['Cutting Ballon評価試験（平成30年度）', 'ステント通過性評価試験（平成29年度）', 'ステント押し込み試験（平成29年度）']),
        ('医療データを用いた冠動脈の解析プログラム開発研究（平成29年度）',
         ['（理化学研究所共同研究）＊特許出願中']),
        ('血管モデルを利用するための製造技術の開発とその応用についての研究（平成29年度）',
         ['（理化学研究所共同研究）＊特許出願中']),
        ('心臓血管モデルの貸出及び心臓血管モデルを利用したワークショップの開催',
         ['（平成29年度）年5回開催', '（平成28年度）年3回開催']),
        ('再生医療サミット（平成28年度）', []),
        ('沖縄医療産業競争力強化事業（平成27年度～平成29年度）', []),
        ('再生医療・細胞治療の臨床応用に向けた共同研究体制事業（平成27年度）', []),
        ('健康情報コンサルティング（平成26年度）（沖縄県市町村職員組合検診データ解析）', []),
        ('医療情報プロジェクトコンサルティング（平成26年度）', []),
        ('ICT利活用した離島高齢者見守り実証事業　がんじゅーWithYouプロジェクト（平成26～平成28年度）', []),
        ('地域新成長創出促進事業/沖縄医工連携等創出ネットワーク形成事業（平成25年度）', []),
    ]
    li = ''
    for t, sub in rows:
        s = ('\n<ul>\n' + ''.join('<li>%s</li>\n' % x for x in sub) + '</ul>\n') if sub else ''
        li += '<li>%s%s</li>\n' % (t, s)
    page('plan.html', '受託案件', 'Projects',
         ORG + 'がこれまでに受託した事業・研究開発の一覧です。', '<ul class="list">\n%s</ul>' % li)


# ---------- 新着情報 ----------
def build_news():
    page('news.html', '新着情報', 'News',
         ORG + 'の新着情報を一覧でご覧いただけます。', '<ul class="news">\n%s</ul>' % news_items(NEWS))
    back = '\n<p class="back"><a class="more" href="news.html">新着情報一覧</a></p>'
    for iso, shown, path, title, body in NEWS:
        page(path, title, 'News', title, '<p class="post-date">%s</p>\n%s' % (shown, body) + back,
             [('news.html', '新着情報')])


# ---------- リンク ----------
def build_link():
    li = ''.join('<li><a href="%s">%s</a><p>%s</p><small>%s</small></li>\n' % (u, t, d, u) for u, t, d in LINKS)
    page('link.html', 'リンク', 'Links', ORG + 'のおすすめサイトをご紹介します。',
         '<ul class="linklist">\n%s</ul>' % li)


# ---------- お問合せ ----------
def build_contact():
    body = '''<p>ご質問、お問合せは、お電話またはメールにてお気軽にお問い合わせ下さい。</p>
<dl class="contact">
<div><dt>住所</dt><dd class="addr">%s<br>%s</dd></div>
<div><dt>お電話</dt><dd><a href="%s">%s</a></dd></div>
<div><dt>メール</dt><dd><a href="%s">%s</a></dd></div>
</dl>''' % (ZIP, ADDR, TEL_HREF, TEL, MAILTO, MAIL_E)
    page('contact.html', 'お問合せ', 'Contact',
         'お電話かメールで、' + ORG + 'へのお問合せいただけます。', body)


if __name__ == '__main__':
    build_index()
    build_facilities()
    build_plan()
    build_news()
    if SHOW_LINKS:
        build_link()
    build_contact()
