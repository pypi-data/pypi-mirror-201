import redis, re, random, requests, asyncio, warnings, sys, urllib3, smtplib, pymongo, hashlib
from w3lib import html
from aiohttp import ClientSession
from email.mime.text import MIMEText


class ale():
    def __int__(self, yu, url_ku, ip_all, redis_password, redis_port, redis_db, mongodb_port, mongodb_password,
                daili_no, daili_name, daili_password, dali_host, daili_port):
        self.yu = yu
        self.url_ku = url_ku
        # 链接数据库
        self.ip_all = ip_all
        self.redis_password = redis_password
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.mongodb_port = mongodb_port
        self.mongodb_password = mongodb_password
        # 开启代理设置1否则0
        self.daili_no = daili_no
        self.daili_name = daili_name
        self.daili_password = daili_password
        self.dali_host = dali_host
        self.daili_port = daili_port


    # 报错邮箱(不含附件)
    def email(self,title, content):
        # 构造邮件内容
        msg = MIMEText(content)
        # 设置邮件主题
        msg["Subject"] = title
        # 发送者
        msg['From'] = 'fanwen_feedback@foxmail.com'
        # 邮箱服务账号
        from_addr = "1194546292@qq.com"
        # 邮箱服务器密码
        password = "nowxkjsugzyifjcd"
        # 收件人地址
        to_addr = "1194546292@qq.com"
        # smtp服务器地址
        smtp_server = 'smtp.qq.com'
        # smtp协议的默认端口是25，QQ邮箱smtp服务器端口是465，第三个参数是超时设置
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
        server.ehlo()
        # 登录邮箱
        server.login(from_addr, password)
        # 发送邮件，第一个参数是发送方地址，第二个参数是接收方列表，列表中可以有多个接收方地址，msg.as_string()将MIMEText对象转化成文本
        server.sendmail(from_addr, [to_addr], msg.as_string())
        # 关闭邮箱
        server.quit()


    # 列表分割
    def func(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


    # 生成随机ua
    def get_ua(self):
        first_num = random.randint(55, 62)
        third_num = random.randint(0, 3200)
        fourth_num = random.randint(0, 140)
        os_type = [
            '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
            '(Macintosh; Intel Mac OS X 10_12_6)'
        ]
        chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

        ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                       '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                      )
        return ua


    # 定义页面打开函数,使用了随机ua和代理ip
    def get(self,url, yu):
        global err
        headers = {"User-Agent": self.get_ua(), "Referer": 'https://www.%s' % yu}
        if self.daili_no == 1:
            # pip install -U requests[socks]  socks5代理
            # pip install --index https://mirrors.ustc.edu.cn/pypi/web/simple/ virtualenv
            proxyMeta = "socks5://%(user)s:%(pass)s@%(host)s:%(port)s" % {"host": self.dali_host, "port": self.daili_port,
                                                                          "user": self.daili_name, "pass": self.daili_password}
            myproxies = {"http": proxyMeta, "https": proxyMeta}
            try:
                urllib3.disable_warnings()
                data = self.session.get(url, headers=headers, proxies=myproxies, timeout=5)
                if data.status_code == 200:
                    data.encoding = "gbk"
                    return data.text
                elif data.status_code == 403:
                    self.get(url, yu)
                elif data.status_code == 404:
                    return '无数据'
                else:
                    err += 1
                    if err >= 5:
                        err = 0
                        print("\n", "-" * 74, '此ip已被封禁！', "-" * 74, "\n")
                        exit()
                    return '无数据'
            except:
                self.get(url, yu)
        else:
            data = requests.get(url, headers=headers)
            if data.status_code == 200:
                data.encoding = "gbk"
                return data.text
            elif data.status_code == 403:
                self.get(url, yu)
            elif data.status_code == 404:
                return '无数据'
            else:
                err += 1
                if err >= 5:
                    err = 0
                    print("\n", "-" * 74, '此ip已被封禁！', "-" * 74, "\n")
                    exit()
                return '无数据'


    # 获取审核结果
    def shenhe_jieguo(self,response):
        try:
            bai_shen_js = 0
            bai_shen_list = []
            for bai_shen in response['result']['predict']:
                score = float("%.2f" % bai_shen['score'])
                new_highsens_hit = bai_shen['new_highsens_hit']
                lowsens_hit = bai_shen['lowsens_hit']
                bai_shen_list += new_highsens_hit
                bai_shen_list += lowsens_hit
                if bai_shen['label'] == '1':
                    if score >= 0.8:
                        score = 20
                    bai_shen_js += score
                elif bai_shen['label'] == '2':
                    if score >= 0.7:
                        score = 20
                    bai_shen_js += score
                elif bai_shen['label'] == '3':
                    if score >= 0.8:
                        score = 20
                    bai_shen_js += score
                elif bai_shen['label'] == '4':
                    if score >= 0.8:
                        score = 20
                    bai_shen_js += score
                elif bai_shen['label'] == '5':
                    if score >= 0.8:
                        score = 20
                    bai_shen_js += score
                elif bai_shen['label'] == '6':
                    if score >= 0.94:
                        score = 20
                    bai_shen_js += score
                elif bai_shen['label'] == '7':
                    if score >= 0.7:
                        score = 20
                    bai_shen_js += score
            if bai_shen_js < 15 and bai_shen_list == []:
                return '合规'
            else:
                return '不合规'
        except Exception as e:
            return e


    # 百度文本审核及存储
    async def baidu_shenhe(self,pd_txt, txt, title_html, url2):
        try:
            url = 'http://localhost:8800/text_censor_controller'
            headers = {'content-type': 'application/json'}
            data = {"appid": 89304,
                    "fields": {"content": pd_txt},
                    "config": {"labels": ["1", "2", "3", "4", "5", "6"]},
                    "logid": "23644756797"}
            async with ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    response = await response.json(content_type='text/html')
                    # 判断审核结果
                    if self.shenhe_jieguo(response) == '合规':
                        for ci in self.quchu_content_ci:
                            txt = txt.replace(ci, '')
                        key_pd_md5 = hashlib.md5(title_html.encode(encoding='utf-8')).hexdigest()
                        txt_cn = {'quchong_md5': hashlib.md5(txt.encode(encoding='utf-8')).hexdigest(),
                                  'chaxun_md5': key_pd_md5, 'title': title_html, 'content': txt}

                        # 判断是否有栏目然后存储数据
                        if "(" in title_html and ")" in title_html:
                            try:
                                self.mongo_db['fanwen']['daishenhe'].insert_one(txt_cn)
                                self.redis_sql.sadd('fanwen_daishenhe_title_all', str([title_html, key_pd_md5]))
                            except:
                                pass
                        else:
                            try:
                                self.mongo_db['fanwen']['daishenhe_wufenlei'].insert_one(txt_cn)
                                self.redis_sql.sadd('fanwen_daishenhe_wufenlei_title_all', str([title_html, key_pd_md5]))
                            except:
                                pass
                        # 存储爬取过的url
                        self.redis_sql.sadd('%s_yu_quchong' % self.url_ku, url2)

        except Exception as e:
            pass


    # 中文转数字
    def shuzi_zhuan(self,num):
        new_str = ""
        num_dict = {"零": u"0", "一": u"1", "二": u"2", "三": u"3", "四": u"4", "五": u"5", "六": u"6", "七": u"7",
                    "八": u"8", "九": u"9"}
        listnum = list(num)
        shu = []
        for i in listnum:
            if i in num_dict:
                shu.append(num_dict[i])
            else:
                shu.append(i)
        new_str = "".join(shu)
        return new_str


    # 标签正常
    def html_chang(self,fg_content, title):
        html_linshi_pd = 0
        for s, r in zip(fg_content, range(1, len(fg_content) + 1)):
            if str(r) not in s and self.shuzi_zhuan(title) not in s:
                html_linshi_pd = 1
        return html_linshi_pd


    # 分类正常
    def fenlei_yes(self,txt):
        if '作文' in txt or '读后感' in txt or '有感' in txt or '心得' in txt or '体会' in txt or '观后感' in txt or '征文' in txt or '随笔' in txt or '议论文' in txt:
            return '(作文)'
        elif '总结' in txt or '计划' in txt:
            return '(总结计划)'
        elif '策划' in txt or '方案' in txt or '广告语' in txt or '任务书' in txt or '宣传语' in txt:
            return '(策划)'
        elif '合同' in txt or '协议' in txt or '委托' in txt or '证明' in txt or '申请书' in txt or '条款' in txt or '承诺书' in txt or '保证书' in txt or '协商函' in txt:
            return '(合同)'
        elif '教案' in txt or '课件' in txt or '阅读答案' in txt or '阅读理解' in txt or '说课稿' in txt or '教学' in txt:
            return '(教案)'
        elif '简历' in txt or '自我介绍' in txt or '自我鉴定' in txt:
            return '(简历)'
        elif '导游词' in txt:
            return '(旅游)'
        elif '讲话' in txt or '演讲' in txt or '发言稿' in txt or '致辞' in txt or '主持词' in txt or '感言' in txt or '新闻稿' in txt or '广播稿' in txt or '串词' in txt and '思想汇报' not in txt and '宣言' not in txt:
            return '(讲话)'
        elif '党总支' in txt or '思想汇报' in txt or '团总支' in txt or '党团' in txt or '入团' in txt or '入党' in txt or '党员' in txt:
            return '(行政党团)'
        elif '故事' in txt:
            return '(故事)'
        elif '信' in txt or '自荐书' in txt:
            return '(信件)'
        elif '通知' in txt or '公告' in txt or '启事' in txt or '讣告' in txt or '通知' in txt or '告知单' in txt or '警告' in txt or '通告' in txt:
            return '(通知)'
        elif '文书' in txt or '检讨书' in txt or '倡议书' in txt or '汇报' in txt or '报告' in txt or '读书笔记' in txt or '邀请函' in txt or '邀请涵' in txt or '制度' in txt or '闭幕词' in txt or '周记' in txt or '决心书' in txt or '情况说明' in txt or '简报' in txt or '鉴定' in txt or '主要内容' in txt or '意见' in txt or '职责' in txt or '设计' in txt:
            return '(文书)'
        elif '礼仪' in txt or '事迹' in txt or '材料' in txt:
            return '(其他)'
        else:
            return '空'


    # 大分类处理
    def fenlei(self,txt, txts):
        if txts == 1:
            return ''
        else:
            fen = self.fenlei_yes(txt)
            if fen == '空':
                if html_mianbaoxie != '':
                    fen = self.fenlei_yes(html_mianbaoxie)
                    if fen == '空':
                        return ''
                    else:
                        return fen
                else:
                    return ''
            else:
                return fen


    # 面包屑通用处理
    def mianbaoxie(self,mianbaoxie):
        # 过滤转义符
        qing_gz = r'&(.+?);'
        qing = re.findall(qing_gz, mianbaoxie, re.S)
        for i in qing:
            i = '&' + i + ';'
            mianbaoxie = mianbaoxie.replace(i, '')
        results = re.compile('<[^>]+>')
        mianbaoxie = results.sub("", mianbaoxie)
        mianbaoxie = mianbaoxie.replace(' ', '')
        return mianbaoxie


    # 瑞文系面包屑提取
    def mianbaoxie_ruiwenxi(self,htm):
        try:
            # 瑞文网、短美文
            mianbaoxie_gz = r'<div class="sidebar">(.+?)</div>'
            mianbaoxie = re.findall(mianbaoxie_gz, htm, re.S)[0]
            return mianbaoxie
        except:
            try:
                # 范文先生
                mianbaoxie_gz = r'<div class="list_path">(.+?)</div>'
                mianbaoxie = re.findall(mianbaoxie_gz, htm, re.S)[0]
                return mianbaoxie
            except:
                try:
                    # 朵朵
                    mianbaoxie_gz = r'<div class="mianbaoxie">(.+?)</div>'
                    mianbaoxie = re.findall(mianbaoxie_gz, htm, re.S)[0]
                    return mianbaoxie
                except:
                    try:
                        # 育文
                        mianbaoxie_gz = r'<div class="jiaoshimao_site">(.+?)</div>'
                        mianbaoxie = re.findall(mianbaoxie_gz, htm, re.S)[0]
                        return mianbaoxie
                    except:
                        try:
                            # 快淘
                            mianbaoxie_gz = r'<div class="place">(.+?)</div>'
                            mianbaoxie = re.findall(mianbaoxie_gz, htm, re.S)[0]
                            return mianbaoxie
                        except:
                            try:
                                # 文小秘
                                mianbaoxie_gz = r'<div class="position">(.+?)</div>'
                                mianbaoxie = re.findall(mianbaoxie_gz, htm, re.S)[0]
                                return mianbaoxie
                            except:
                                return ''


    # 通用内容初步处理
    def content_tong(self,html_content):
        html_content = html_content.replace('<pstyle=', '<p style=')
        # 去除文本内指定标签
        html_content = html.remove_tags(html_content, which_ones=(
            'a', 'img', 'em', 'br', 'span', 'section', 'hr', 'internet', 'strong', 'wbr', 'u', 'table', 'o', 'tbody',
            'style'))
        # 其他p、h2标签
        qing_gz = r'<p (.+?)>'
        qing = re.findall(qing_gz, html_content, re.S)
        for i in qing:
            i = '<p ' + str(i) + '>'
            html_content = html_content.replace(i, '<p>')
        qing_gz = r'</p (.+?)>'
        qing = re.findall(qing_gz, html_content, re.S)
        for i in qing:
            i = '</p ' + str(i) + '>'
            html_content = html_content.replace(i, '</p>')
        qing_gz = r'<h2 (.+?)>'
        qing = re.findall(qing_gz, html_content, re.S)
        for i in qing:
            i = '<h2 ' + str(i) + '>'
            html_content = html_content.replace(i, '<h2>')
        # 过滤转义符
        qing_gz = r'&(.+?);'
        qing = re.findall(qing_gz, html_content, re.S)
        for i in qing:
            i = '&' + i + ';'
            html_content = html_content.replace(i, '')
        # 其他过滤
        html_content = html_content.replace('<strong>', '<p>').replace('</strong>', '</p>').replace(
            '</p></p>', '</p>').replace('<p><p>', '<p>')
        # 去除邮箱
        results = re.compile(r'(\w[-\w.+]*#([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14})', re.S)
        html_content = results.sub("", html_content)
        results = re.compile(r'(\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14})', re.S)
        html_content = results.sub("", html_content)
        # 去除网址
        results = re.compile(r'([a-zA-z]+://[^\s]*)', re.S)
        html_content = results.sub("", html_content)
        # 去除手机号
        results = re.compile(r'(0?(13|14|15|17|18|19)[0-9]{9})', re.S)
        html_content = results.sub("", html_content)
        # 去除座机号
        results = re.compile(r'([0-9-()（）]{7,18})', re.S)
        html_content = results.sub("", html_content)
        # 去除QQ号
        results = re.compile(r'([1-9]([0-9]{5,11}))', re.S)
        html_content = results.sub("", html_content)
        # 去除域名
        results = re.compile(
            r'(\w+\.\w+\.\w+\.(com|net|me|co|cn|xyz|cc|asia|love|icu|store|fun|work|ltd|top|site|club|online))', re.S)
        html_content = results.sub("", html_content)
        results = re.compile(
            r'(\w+\.\w+\.(com|net|me|co|cn|xyz|cc|asia|love|icu|store|fun|work|ltd|top|site|club|online))', re.S)
        html_content = results.sub("", html_content)
        results = re.compile(
            r'(\w+\.(com|net|me|co|cn|xyz|cc|asia|love|icu|store|fun|work|ltd|top|site|club|online))', re.S)
        html_content = results.sub("", html_content)
        # 去除空标签对
        html_content = re.sub(r'<([a-z]+\d?)\b[^>]*>( |[\s　])*</\1>', '', html_content)
        # 去除空符号
        html_content = html_content.replace('（）', '').replace('【】', '').replace('「」', '').replace(
            '《》', '').replace('<>', '').replace('{}', '').replace('[]', '').replace('()', '').replace(
            '<h2></h2>', '').replace('<p></p>', '').replace('<<', '《').replace('>>', '》')
        return html_content


    # 通用子内容处理
    def content_zi(self,i):
        # 数据再次处理：
        i = i.replace('</spanstyle>', '').replace('<spanstyle>', '').replace(
            '</p>：</p>', '</p>').replace('</p>:</p>', '</p>').replace('</p>。</p>', '</p>').replace(
            '</p>;</p>', '</p>').replace('</p>"</p>', '</p>').replace("</p>'</p>", '</p>').replace(
            '</p>.</p>', '</p>').replace('</p>；</p>', '</p>').replace('</p>【</p>', '</p>').replace(
            '</p>】</p>', '</p>').replace('</p>「</p>', '</p>').replace('</p>」</p>', '</p>').replace(
            '</p>{</p>', '</p>').replace('</p>}</p>', '</p>').replace('</p>[</p>', '</p>').replace(
            '</p>]</p>', '</p>').replace('</p>,</p>', '</p>').replace('</p>《</p>', '</p>').replace(
            '</p>》</p>', '</p>').replace('</p>/</p>', '</p>').replace('</p>、</p>', '</p>').replace(
            '</p>｜</p>', '</p>').replace('</p>\</p>', '</p>').replace('</p>。</p>', '</p>').replace(
            '</p>!</p>', '</p>').replace('</p>！</p>', '</p>').replace('</p>@</p>', '</p>').replace(
            '</p>#</p>', '</p>').replace('</p>¥</p>', '</p>').replace('</p>%</p>', '</p>').replace(
            '</p>&</p>', '</p>').replace('</p>*</p>', '</p>').replace('</p>（</p>', '</p>').replace(
            '</p>）</p>', '</p>').replace('</p>$</p>', '</p>').replace('</p>^</p>', '</p>').replace(
            '</p>(</p>', '</p>').replace('</p>)</p>', '</p>').replace('<p>     ', '<p>').replace(
            '<p>    ', '<p>').replace('<p>   ', '<p>').replace('<p>  ', '<p>').replace(
            '<p>　　　　　', '<p>').replace('<p>　　　　', '<p>').replace('<p>　　　', '<p>').replace(
            '<p>　　', '<p>').replace('<p>　', '<p>').replace('</p>', '</p><p>').replace(
            '<p><p>', '<p>').replace('<p></p>', '')
        i = i + '<p>结尾</p>'
        i = i.replace('<p><p>结尾</p>', '').replace('<p>结尾</p>', '').replace('</p>', '</p>$分割$')
        # 判断p标签是否完整
        ju_pd = i.split('$分割$')
        p_chupan = 0
        for lin in ju_pd:
            lin = lin.replace(' ', '')
            if lin != '' or None:
                if '<p>' not in lin or '</p>' not in lin:
                    p_chupan = 1
                    continue
        if p_chupan == 0:
            i = ''.join(ju_pd)
            # 判断是否含有除了p之外的其他标签
            pd_i = i.replace('<p>', '').replace('</p>', '')
            # 生成26英文字母
            char_all = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
            pd_i_biaoqian = 0
            # 判断是否包含其他标签
            for zi in char_all:
                if '<' + zi in pd_i:
                    pd_i_biaoqian = 1
                    print(i.replace('</p>', '</p>\n'))
            # 排除含有其他html的数据
            if pd_i_biaoqian == 0:
                contentse.append(i)
                contents.append(i.replace('<p>', '').replace('</p>', ''))

        else:
            i = ''.join(ju_pd)
            print(i.replace('</p>', '</p>\n'))


# 通用标题标签判断
def title_biaoqian_pd(self,title_html, fg_content, html_content, url):
    global cw, contents, contentse, rengong
    # 判断标题是否包含指定违禁词
    title_html_panduan = 0
    for i in self.quchu_title_content_ci:
        if i in title_html:
            title_html_panduan = 1
            continue
    if title_html_panduan == 0:
        # 判断是否有内容可分割
        if len(fg_content) > 0:
            # 去除四位数字
            results = re.compile(r'(\d{4})', re.S)
            fg_content_str = results.sub("", str(fg_content))
            results = re.compile(r'(\d+)字', re.S)
            fg_content_str = results.sub("", fg_content_str)
            # 提取数字
            number = re.findall("\d+", fg_content_str)
            if len(number) > 0:
                numbers = [int(i) for i in number]
                if len(numbers) > 0:
                    if max(numbers) == len(fg_content):
                        # 标签正常
                        html_linshi_pd = self.html_chang(fg_content, title_html)
                        if html_linshi_pd == 0:
                            cw = ''
                        else:
                            # 标签出错 记录错误url
                            self.redis_sql.sadd('%s_chucuo' % self.url_ku, url)
                            cw = 'A'
                    else:
                        cuo = len(fg_content) - max(numbers)
                        if cuo > 8:
                            # 标签出错 记录错误url
                            self.redis_sql.sadd('%s_chucuo' % self.url_ku, url)
                            cw = 'A'
                        elif cuo < 0:
                            # 标签出错 记录错误url
                            cw = 'A'
                            self.redis_sql.sadd('%s_chucuo' % self.url_ku, url)
                        else:
                            # 标签正常 记录错误url
                            html_linshi_pd = self.html_chang(fg_content, title_html)
                            if html_linshi_pd == 0:
                                cw = cuo
                            else:
                                # 标签出错 记录错误url
                                cw = 'A'
                                self.redis_sql.sadd('%s_chucuo' % self.url_ku, url)
                else:
                    # 标签出错 记录错误url
                    cw = 'A'
                    self.redis_sql.sadd('%s_chucuo' % self.url_ku, url)
                if cw != '' and cw.replace('a', 'A') != 'A':
                    if int(cw) > 0:
                        html_content = html_content.split('<h2>fenge</h2>')
                        # 删除错误元素
                        html_content = html_content[int(cw) + 1:]
                else:
                    html_content = html_content.split('<h2>fenge</h2>')
                    html_content = html_content[1:]
                fenlei_pd = 0
                rengong = 0
                if cw.replace('a', 'A') != 'A':
                    fenlei_pan = self.fenlei(linshi_title, 0)
                    if fenlei_pan.replace('a', 'A') != 'A':
                        pd_title = ''
                    else:
                        pd_title = 'A'
                else:
                    # 弃用url
                    self.redis_sql.sadd('%s_qita' % self.url_ku, url)
                    pd_title = 'A'
                if pd_title.replace('a', 'A') != 'A':
                    if pd_title != '':
                        fenlei_pan = self.fenlei(pd_title, 0)
                        fenlei_pan = pd_title + fenlei_pan
                        if fenlei_pd == 1:
                            fenlei_pan = self.fenlei(pd_title, 1)
                            fenlei_pan = pd_title + fenlei_pan
                    else:
                        fenlei_pan = self.fenlei(title_html, 0)
                        fenlei_pan = title_html + fenlei_pan
                        if fenlei_pd == 1:
                            fenlei_pan = self.fenlei(title_html, 1)
                            fenlei_pan = title_html + fenlei_pan
                    # 临时存放判断通过内容
                    contents = []
                    contentse = []
                    # 遍历每篇文章进行审核存储
                    for i in html_content:
                        # 子通用内容数据处理
                        self.content_zi(i)
                    # 分割异步携程百度审核
                    if contents != [] and contentse != []:
                        tasks = [asyncio.ensure_future(
                            self.baidu_shenhe(pd_txt, txt, "「%s」" % linshi_title + fenlei_pan, url)) for pd_txt, txt in
                            zip(contents, contentse)]
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(asyncio.wait(tasks))
                else:
                    # 弃用url
                    self.redis_sql.sadd('%s_qita' % self.url_ku, url)
    else:
        # 弃用url
        self.redis_sql.sadd('%s_qita' % self.url_ku, url)


    # 瑞文title提取
    def title_ruiwenxi(self,htm):
        try:
            title_gz = r'<h1 class="title">(.+?)</h1>'
            html_title = re.findall(title_gz, str(htm), re.S)[0]
            return html_title
        except:
            title_gz = r'<title>(.+?)</title>'
            html_title = re.findall(title_gz, str(htm), re.S)[0]
            return html_title


    # 通用标题处理
    def title(self,tml_title):
        global linshi_title
        linshi_title =  self.html_title
        html_title =  self.html_title.replace('(', '（').replace(')', '）').replace('{', '（').replace(
            '}', '）').replace(' ', '').replace('[', '【').replace(']', '】').replace('<', '【').replace(
            '>', '】').replace('\t', '').replace('\n', '').replace('\r', '').replace('1-2分钟', '$$分钟').replace('4s',
                                                                                                                 '四s')
        # 初步处理标题
        results = re.compile(r'（.*）', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'【.*】', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'「.*」', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'_.*', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'-.*', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d{4}|\d{2})年度', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d{4}|\d{2})年', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d{4}|\d{2})', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'((1[0-2])|(0?[1-9]))月', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'((1[0-2])|(0?[1-9]))', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(([12][0-9])|(3[01])|(0?[1-9]))日', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(([12][0-9])|(3[01])|(0?[1-9]))', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d+)字左右', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d+)字', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d+)句', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d+)条', re.S)
        html_title = results.sub("", html_title)
        results = re.compile(r'(\d+)篇', re.S)
        html_title = results.sub("", html_title)
        html_title = html_title.replace('贫困申请书', '贫困生申请书')
        if html_title == '大全作文' or html_title == '作文':
            html_title = '此标题不可替换'
        # 需要去除的关键词
        for dele in  self.quchu_title_ci:
            html_title = html_title.replace(dele, '')
        # 简单处理作文类标题
        html_title_key = ['话题', '高考', '中考', '年级', '高一作文', '高二作文', '高三作文', '初一作文', '初二作文',
                          '初三作文', '英语作文', '寒假',
                          '关爱小学生', '暑假', '小学生童话', '小学生活', '记事作文', '暑期', '网络', '之友', '记叙文',
                          '聪明的', '毕业季', '写事', '我是小学生', '难忘',
                          '笑了', '记作文']
        html_title_key_id = 0
        for i in html_title_key:
            if i in html_title:
                html_title_key_id = 1
        if '作文' in html_title and '小学生作文' != html_title and html_title_key_id == 0 and '小学生的作文' != html_title and '中小学生作文' != html_title and '中小学生的作文' != html_title:
            html_title_gai = html_title.replace('小学生', '').replace('优秀的作文', '').replace('优秀作文', '').replace(
                '作文', '').replace('小学生', '')
            if len(html_title_gai) < 4:
                if '优秀' in html_title and '话题' != html_title_gai:
                    html_title = '关于' + html_title_gai + '的优秀作文'
                elif '优秀' in html_title and html_title_gai == '话题':
                    html_title = '话题优秀作文'
                elif html_title_gai == '话题':
                    html_title = '话题作文'
                elif '小学生' in html_title:
                    html_title = '关于' + html_title_gai + '的小学生作文'
                else:
                    html_title = '关于' + html_title_gai + '的作文'
        elif html_title == '此标题不可替换':
            html_title = '作文大全'
        html_title = '##$$' + html_title
        html_title = html_title.replace('的的', '的').replace('##$$的', '').replace('##$$', '').replace('四s',
                                                                                                        '4s').replace(
            '关于描写的', '描写的').replace('$$分钟', '2分钟').replace('$$', '').replace('，', '')
        return html_title


    # 瑞文系内容处理
    def content_ruiwenxi(self,htm, url):
        global html_mianbaoxie
        try:
            if 'wenxiaomi_url' !=  self.url_ku:
                # 内容初步提取
                content_gz = r'<div class="content">(.+?)<script>'
                html_content = re.findall(content_gz, htm, re.S)[0]
                # 面包屑提取及处理
                html_mianbaoxie =  self.mianbaoxie( self.mianbaoxie_ruiwenxi(htm))
                # 去除内容页外链
                results = re.compile(r'<div class="excellent_articles_box">.*</div>', re.S)
                html_content = results.sub("", html_content)
            else:
                # 文小密内容初步提取
                content_gz = r'<div class="con_article con_main" id="contentText">(.+?)<div class="gg_center" align="center">'
                html_content = re.findall(content_gz, htm, re.S)[0]
                # 面包屑提取及处理
                html_mianbaoxie =  self.mianbaoxie( self.mianbaoxie_ruiwenxi(htm))
            # 通用内容初步处理
            html_content =  self.content_tong(html_content)
            # 提取二级标题
            fg_gz = r'<h2>(.+?)</h2>'
            fg_content = re.findall(fg_gz, html_content, re.S)
            # 去除二级标题大些数字
            fg_content = [ self.shuzi_zhuan(s) for s in fg_content]
            # 制作内容分割符
            for i in fg_content:
                i = '<h2>' + i + '</h2>'
                html_content = html_content.replace(i, '<h2>fenge</h2>')
            # 提取瑞文系title
            title_ruixi = title_ruiwenxi(htm)
            # 通用标题处理
            title_html = title(title_ruixi)
            # 通用标题标签判断处理
            title_biaoqian_pd(title_html, fg_content, html_content, url)
        except:
            pass


    # 瑞文系数据库url遍历
    def ruiwen_xilie(self):
        # 去除已经爬取过的url
        zong_url = list( self.redis_sql.sdiff( self.url_ku,  self.url_ku.replace('_url', '_url_qita'),  self.url_ku.replace('_url', '_yu_quchong'),
                                               self.url_ku.replace('_url', '_url_chucuo')))
        # 遍历差集url
        for url in zong_url:
            # 判断是否为外站url
            if 'www.%s' %  self.yu in url:
                # 剔除指定栏目url
                ti_url = 0
                for ti in  self.quchu_lujing_ci:
                    if ti in url:
                        ti_url = 1
                        # 弃用url
                        self.redis_sql.sadd('%s_qita' %  self.url_ku, url)
                        continue
                if ti_url == 0:
                    # 内容提取并压缩html
                    htm =  self.get(url,  self.yu)
                    if htm != '无数据':
                        htm = re.sub(r">\s+<", "><", str(htm)).replace('　', '').replace('\n', '').replace('\r', '')
                        # 内容处理
                        content_ruiwenxi(htm, url)
            else:
                # 删除redis键的元素
                self.redis_sql.srem(self.url_ku, url)

    def run(self):
        # 处理url计数初始计数/报错计数
        err = 0
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # 屏蔽警告
        warnings.simplefilter('ignore', DeprecationWarning)
        if self.daili_no == 1:
            session = requests.session()
            session.keep_alive = False
        pool = redis.ConnectionPool(host=self.ip_all, port=self.redis_port, password=self.redis_password, db=self.redis_db,
                                    decode_responses=True)
        redis_sql = redis.Redis(connection_pool=pool)
        mongo_db = pymongo.MongoClient(self.ip_all, self.mongodb_port, username='root', password=self.mongodb_password)

        for biao in ['quchu_title_ci', 'quchu_title_content_ci', 'quchu_lujing_ci', 'quchu_content_ci', 'tag_ciku']:
            # 去除标题内指定词
            if biao == 'quchu_title_ci':
                quchu_title_ci = list(redis_sql.smembers(biao))
            # 去除标题含指定词的内容
            elif biao == 'quchu_title_content_ci':
                quchu_title_content_ci = list(redis_sql.smembers(biao))
            # 去除指定路径的文章
            elif biao == 'quchu_lujing_ci':
                quchu_lujing_ci = list(redis_sql.smembers(biao))
            # 去除指定路径的文章
            elif biao == 'quchu_content_ci':
                quchu_content_ci = list(redis_sql.smembers(biao))
        try:
            # 异步运行瑞文系列网站数据
            ruiwen_xilie()
        except Exception as e:
            self.email('%s入库审核脚本报错' % self.yu, '报错为：%s' % e)

        self.email('有程序运行结束', '%s入库程序结束' % self.yu)


if __name__ == '__main__':
    a=ale(yu='1') #给入参数
    a.run()