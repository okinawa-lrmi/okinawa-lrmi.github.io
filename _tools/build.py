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

NAV = [
    ('index.html', 'トップページ'),
    ('facilities.html', '研究所案内'),
    ('plan.html', '受託案件'),
    ('news.html', '新着情報'),
    ('link.html', 'リンク'),
    ('contact.html', 'お問合せ'),
]

# 新着情報（新しいものを上に書く）
NEWS = [
    ('2016-02-24', '2016.02.24', '20150320.html', '「医療情報利用推進セミナー」を開催します。', 'お知らせ'),
    ('2015-03-19', '2015.03.19', '20150319.html', 'ウェブサイトを公開しました。', 'お知らせ'),
]

LINKS = [
    ('http://ganju-with-you.com/', 'がんじゅー With You　共同企業体',
     '情報通信技術を利用・活用することによって、高齢者の効率的な健康管理の実現、健康意識の改善、離島生活における不安の軽減が実現するかを検証しています。'),
    ('http://www.yuima-ru.med.u-ryukyu.ac.jp/', 'ゆい健康プロジェクト（健康行動実践モデル実証事業）',
     '学童と高齢者への食に対する情報提供と食事介入で地域の健康行動を向上させ、生活習慣病改善で沖縄県民の健康と長寿を促進することを目標としております。'),
]

ICON = {
    'building': '<path d="M12 54V20h24v34M36 54V30h16v24M6 54h52"/><path d="M19 28h4M27 28h4M19 36h4M27 36h4M19 44h4M27 44h4M42 38h4M42 46h4"/><path d="M24 20v-8M20 12h8"/>',
    'doc': '<path d="M16 8h24l10 10v38H16z"/><path d="M40 8v10h10M23 28h20M23 36h20M23 44h12"/>',
    'link': '<path d="M27 37a10 10 0 0 0 14 0l9-9a10 10 0 0 0-14-14l-4 4"/><path d="M37 27a10 10 0 0 0-14 0l-9 9a10 10 0 0 0 14 14l4-4"/>',
    'mail': '<path d="M8 16h48v32H8z"/><path d="M8 18l24 18 24-18"/>',
    'tel': '<path d="M20 8h24a4 4 0 0 1 4 4v40a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4V12a4 4 0 0 1 4-4z"/><path d="M28 48h8M16 16h32M16 42h32"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 64 64" fill="none" stroke="#7b2d12" stroke-width="2.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICON[name])


def head(title, desc, path):
    full = ORG_FULL if not title else title + '｜' + ORG_FULL
    return '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600;700&amp;display=swap">
<link rel="stylesheet" href="assets/css/style.css">
</head>
''' % (full, desc, BASE, '' if path == 'index.html' else path)


def brand(tag='a'):
    return ('<a class="brand" href="index.html"><img src="assets/img/favicon.svg" alt="" width="46" height="46">'
            '<span><small>一般社団法人</small><strong>%s</strong></span></a>' % ORG_WBR)


def header(current):
    items = ''.join('<li><a href="%s"%s>%s</a></li>\n' % (h, ' aria-current="page"' if h == current else '', t)
                    for h, t in NAV)
    return '''<body>
<header class="hd">
<div class="wrap hd-main">
%s
<div class="hd-aside">
<a class="btn btn-line btn-small" href="contact.html">お問合せ</a>
<button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false"><i></i>Menu</button>
</div>
</div>
<nav class="hd-nav" aria-label="メインメニュー">
<div class="wrap">
<ul class="nav" id="nav">
%s</ul>
</div>
</nav>
</header>
''' % (brand(), items)


def footer():
    items = ''.join('<li><a href="%s">%s</a></li>\n' % (h, t) for h, t in NAV)
    return '''<footer class="ft">
<div class="wrap ft-main">
<div>
%s
<address>%s %s<br>
TEL：<a href="%s">%s</a> ／ <a href="%s">%s</a></address>
</div>
<ul class="ft-nav">
%s</ul>
</div>
<div class="colophon"><p>Copyright &copy; %s. All rights reserved.</p></div>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
''' % (brand(), ZIP, ADDR, TEL_HREF, TEL, MAILTO, MAIL_E, items, ORG_FULL)


def page(path, title, en, desc, body, crumbs=None):
    c = '<li><a href="index.html">トップページ</a></li>'
    for h, t in (crumbs or []):
        c += '<li><a href="%s">%s</a></li>' % (h, t)
    c += '<li>%s</li>' % title
    cur = crumbs[0][0] if crumbs else path
    html = head(title, desc, path) + header(cur) + '''<main>
<div class="page-hd">
<div class="wrap">
<p class="en">%s</p>
<h1>%s</h1>
</div>
</div>
<div class="wrap">
<ul class="crumbs">%s</ul>
</div>
<div class="wrap page">
<div class="prose">
%s
</div>
</div>
</main>
''' % (en, title, c, body) + footer()
    write(path, html)


def write(path, html):
    with io.open(os.path.join(ROOT, path), 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('作成:', path)


def news_items(items):
    return ''.join('<li><time datetime="%s">%s</time><a href="%s">%s</a><span class="tag">%s</span></li>\n' % n
                   for n in items)


# ---------- トップページ ----------
def build_index():
    links = ''.join('<li><a class="card" href="%s"><b>%s</b></a></li>\n' % (u, t) for u, t, d in LINKS)
    feats = [
        ('facilities.html', 'building', '研究所案内', '代表挨拶、事業内容、研究所の概要をご案内します。'),
        ('plan.html', 'doc', '受託案件', 'これまでに受託した事業・研究開発の一覧です。'),
        ('link.html', 'link', 'リンク', '関連するプロジェクトのサイトをご紹介します。'),
        ('contact.html', 'mail', 'お問合せ', 'お電話またはメールにてお気軽にお問い合わせ下さい。'),
    ]
    fhtml = ''.join('<li><a class="feature" href="%s">%s<h3>%s</h3><p>%s</p></a></li>\n' % (h, icon(i), t, d)
                    for h, i, t, d in feats)
    html = head('', DESC, 'index.html') + header('index.html') + '''<main>
<section class="hero">
<img class="hero-art" src="assets/img/hero.svg" alt="" width="1600" height="720">
<div class="hero-body">
<div class="wrap">
<p class="hero-sub">Okinawa LRMI</p>
<p class="hero-main"><span>沖縄県における</span><span>次世代の地域医療に関する</span><span>事業、調査、政策提言を行っています。</span></p>
<a class="btn" href="facilities.html">研究所案内</a>
</div>
</div>
</section>

<div class="wrap sec home-cols">
<section>
<header class="sec-hd">
<h2><span class="en">News</span><span class="ja">新着情報</span></h2>
<a class="btn btn-line btn-small" href="news.html">すべて表示</a>
</header>
<ul class="news">
%s</ul>
</section>
<aside>
<div class="aside-hd">
<h2>Links</h2>
<a class="btn btn-line btn-small" href="link.html">すべて表示</a>
</div>
<ul class="cards">
%s</ul>
</aside>
</div>

<section class="about sec">
<div class="wrap about-cols">
<div>
<h2><small>一般社団法人</small>%s</h2>
<p>本研究所は、医療分野でのイノベーションとなる新技術の開発支援を通して、沖縄県の地域産業振興に貢献するという目的のもとに設立されました。</p>
<a class="btn" href="facilities.html">研究所案内</a>
</div>
<img src="assets/img/about.svg" alt="" width="480" height="360" loading="lazy">
</div>
</section>

<section class="wrap sec">
<h2 class="sr-only">ご案内</h2>
<ul class="features">
%s</ul>
</section>
</main>
''' % (news_items(NEWS), links, ORG_WBR, fhtml) + footer()
    write('index.html', html)


# ---------- 研究所案内 ----------
def people(rows):
    return '<ul class="people">\n' + ''.join('<li><span>%s</span>%s</li>\n' % r for r in rows) + '</ul>'


def build_facilities():
    officers = people([('業務執行理事', '大屋祐輔'), ('監事', '田名毅'), ('監事', '又吉哲太郎'),
                       ('理事', '玉城信光'), ('理事', '宮里達也')])
    members = people([('設立時社員', '崎間敦'), ('設立時社員', '東上里康司'), ('設立時社員', '又吉哲太郎'),
                      ('設立時社員', '横田勝彦'), ('社員', '岩淵成志'), ('社員', '奥村耕一郎'),
                      ('社員', '白井こころ'), ('社員', '等々力英美')])
    body = '''<h2>代表挨拶</h2>
<p>一般社団法人おきなわ長寿復興・医療イノベーション研究所の理事を代表して、一言ご挨拶と本研究所開設の趣旨についてお話しいたします。</p>
<p>本研究所は、医療分野でのイノベーションとなる新技術の開発支援を通して、沖縄県の地域産業振興に貢献するという目的のもとに設立されました。</p>
<p>これまで、全国1位を誇ってきた男性の平均寿命が1990年に5位となり95年に4位、2000年に26位へ後退したいわゆる26ショックに続き、今年2月には女性の平均寿命も全国1位の座から陥落するという事態を迎え、県民の健康水準の低下が大きな社会的関心を集めているところです。県民の保健衛生の低下は、県民自身の生活はもちろんのこと、医療機関における業務負担の増大や、これまで健康長寿県のポジティブイメージの恩恵を被ってきた観光産業や食品産業への影響も懸念されます。</p>
<p>また、沖縄県の健康問題は日本本土を先取りしていると言われており、現在沖縄県が直面している医療課題は将来本土が直面するものと考えられます。そこで、沖縄県の医療をモデルに、将来の日本の医療を変えるような、新しい技術、サービスを開発していく。そして、（いつの日か、）再び長寿日本一を奪還する。そうした取り組みを県内の医療者、企業、大学、自治体、さらには中央官庁も一体となって支援していこうと考えております。</p>
<p>私は、医療分野においては専門ではありませんが、経験を生かして、これまで行政や産業界での経験を生かして、取り組む所存です。</p>
<p>ご助言、ご協力を頂けますようよろしくお願い申し上げます。</p>

<h2>事業内容</h2>
<ul>
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
<div><dt>代表者</dt><dd>牧野浩隆</dd></div>
<div><dt>所在地</dt><dd>%s<br>%s</dd></div>
<div><dt>設立</dt><dd>2014年7月1日</dd></div>
<div><dt>資本金</dt><dd>0円</dd></div>
<div><dt>役員</dt><dd>
%s
</dd></div>
<div><dt>社員</dt><dd>
%s
</dd></div>
</dl>''' % (ORG_FULL, ZIP, ADDR, officers, members)
    page('facilities.html', '研究所案内', 'About',
         ORG + 'の事業内容など、研究所のご案内をしています。', body)


# ---------- 受託案件 ----------
def build_plan():
    rows = [
        ('地域新成長創出促進事業/沖縄医工連携等創出ネットワーク形成事業（H25年度）', []),
        ('ICT利活用した離島高齢者見守り実証事業　がんじゅーWithYouプロジェクト（H26～H28年度）', []),
        ('医療情報プロジェクトコンサルティング（H26年度）', []),
        ('健康情報コンサルティング（H26年度）（沖縄県市町村職員組合検診データ解析）', []),
        ('再生医療・細胞治療の臨床応用に向けた共同研究体制事業（H27年度）', []),
        ('沖縄医療産業競争力強化事業（H27年度～H29年度）', []),
        ('再生医療サミット（H28年度）', []),
        ('心臓血管モデルの貸出及び心臓血管モデルを利用したワークショップの開催',
         ['（H28年度）年3回開催', '（H29年度）年5回開催']),
        ('血管モデルを利用するための製造技術の開発とその応用についての研究（H29年度）',
         ['（理化学研究所共同研究）＊特許出願中']),
        ('医療データを用いた冠動脈の解析プログラム開発研究（H29年度）',
         ['（理化学研究所共同研究）＊特許出願中']),
        ('実験及び研究開発',
         ['ステント押し込み試験（H29年度）', 'ステント通過性評価試験（H29年度）', 'Cutting Ballon評価試験（H30年度）']),
    ]
    li = ''
    for t, sub in rows:
        s = ('\n<ul>\n' + ''.join('<li>%s</li>\n' % x for x in sub) + '</ul>\n') if sub else ''
        li += '<li>%s%s</li>\n' % (t, s)
    page('plan.html', '受託案件', 'Projects',
         ORG + 'がこれまでに受託した事業・研究開発の一覧です。', '<ul>\n%s</ul>' % li)


# ---------- 新着情報 ----------
def build_news():
    page('news.html', '新着情報', 'News',
         ORG + 'の新着情報を一覧でご覧いただけます。', '<ul class="news">\n%s</ul>' % news_items(NEWS))
    back = '\n<p class="back"><a class="btn btn-line" href="news.html">新着情報一覧</a></p>'
    page('20150319.html', 'ウェブサイトを公開しました。', 'News', 'ウェブサイトを公開しました。',
         '<p class="post-date">2015.03.19</p>\n<p>おきなわ長寿復興・医療イノベーション研究所のウェブサイトを公開しました。</p>' + back,
         [('news.html', '新着情報')])
    page('20150320.html', '「医療情報利用推進セミナー」を開催します。', 'News', '「医療情報利用推進セミナー」を開催します。',
         '<p class="post-date">2016.02.24</p>\n<p>詳しくは<a href="content/files/20160224-075621.pdf">こちら</a>（PDF）</p>' + back,
         [('news.html', '新着情報')])


# ---------- リンク ----------
def build_link():
    li = ''.join('<li><a class="card" href="%s"><b>%s</b><span>%s</span><em>%s</em></a></li>\n' % (u, t, d, u)
                 for u, t, d in LINKS)
    page('link.html', 'リンク', 'Links', ORG + 'のおすすめサイトをご紹介します。',
         '<ul class="linklist">\n%s</ul>' % li)


# ---------- お問合せ ----------
def build_contact():
    body = '''<p>ご質問、お問合せは、お電話またはメールにてお気軽にお問い合わせ下さい。</p>
<div class="contact-box">
<div>%s<h2>お電話</h2><a href="%s">%s</a></div>
<div>%s<h2>メール</h2><a href="%s">%s</a></div>
</div>''' % (icon('tel'), TEL_HREF, TEL, icon('mail'), MAILTO, MAIL_E)
    page('contact.html', 'お問合せ', 'Contact',
         'お電話かメールで、' + ORG + 'へのお問合せいただけます。', body)


if __name__ == '__main__':
    build_index()
    build_facilities()
    build_plan()
    build_news()
    build_link()
    build_contact()
