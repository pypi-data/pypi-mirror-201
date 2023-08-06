# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 23:44:04 2021

@author: Petercusin
"""

import os

def get_data_text(path):
    '''
    Parameters
    ----------
    path : TYPE string
        DESCRIPTION. 
		Using path to get data from a single txt file. eg. D://raw_text.txt
        Theoretically, it supports all the text encoding formats, like utf-8, unicode, ansi, gbk etc.

    Returns
    -------
    text : TYPE string
        DESCRIPTION. 
		It returns all the text content from the target file.

    '''
    import chardet
    path=path.replace("\n","")
    f=open(path,'rb')  
    data=f.read()  
    f.close()
    file_encoding=chardet.detect(data).get('encoding')  
    f1=open(path,'r', encoding=file_encoding, errors='ignore')  
    text=f1.read().replace("’","'")
    f1.close()
    return text
            
def get_data_lines(path):
    '''
    Parameters
    ----------
    path : TYPE string
        DESCRIPTION.
		Using path to get data from a single txt file. eg. D://raw_text.txt     
		Theoretically, it supports all the text encoding formats, like utf-8, unicode, ansi, gbk etc.

    Returns
    -------
    lines : TYPE list
        DESCRIPTION. 
		It returns a list containing all the paragraphs of the target file.

    '''
    import chardet
    path=path.replace("\n","")
    f=open(path,'rb')  
    data=f.read()  
    f.close()
    file_encoding=chardet.detect(data).get('encoding')  
    f1=open(path,'r', encoding=file_encoding, errors='ignore')  
    lines=f1.readlines()
    lines=[l.replace("’","'") for l in lines if len(l.strip()) !=0]
    f1.close()
    return lines

def write_to_txt(file_path,text,mode=None,encoding=None):
    '''
    Parameters
    ----------
    file_path : TYPE string
        DESCRIPTION.
    text : TYPE
        DESCRIPTION. string
    mode : TYPE, optional # w;a+
        DESCRIPTION. The default is None.
    encoding : TYPE, optional # utf-8
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    '''
    if mode is None:
        mode="w"
    else:
        mode=mode
    if encoding is None:
        encoding="utf-8"
    else:
        encoding=encoding    
    f=open(file_path,mode=mode,encoding=encoding)
    f.write(text.strip()+"\n")
    f.close()

def get_data_excel(excel_path,column_id,sheet_name=None):
    '''
    Parameters
    ----------
    excel_path : TYPE
        DESCRIPTION. D://data_python.xlsx
        
    column_id : TYPE Int 0,1,2,3
        DESCRIPTION. 0 means the first column, 1 means the second.
        
    sheet_name : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    TYPE list
        DESCRIPTION. return a list of data.
    '''
    
    import pandas as pd
    if sheet_name is None:
        sheet_name=0
    else:
       sheet_name=sheet_name  
    df=pd.read_excel(excel_path,keep_default_na=False, sheet_name=sheet_name,header=None) 
    inter=df.iloc[0:,column_id] #提取第二列所有行  
    return list(inter)

def write_to_excel(excel_path,dic_of_list,sheet_name=None,index=None):
    '''
    Parameters
    ----------
    excel_path : TYPE
        DESCRIPTION. D://results.xlsx
        
    dic_of_list : TYPE
        DESCRIPTION. {"col":["a","b","c","d"],"freq":[1,2,3,4]}
        
    sheet_name : TYPE, optional
        DESCRIPTION. The default is None.
        
    index : TYPE, optional
        DESCRIPTION. The default is None.
        
    Returns
    -------
    None.

    '''
    import pandas as pd
    if sheet_name is None:
        sheet_name="sheet1"
    else:
       sheet_name=sheet_name
    if index is None:
        index=False
    else:
        index=True        
        
    df=pd.DataFrame(dic_of_list)
    df.style.to_excel(excel_path, sheet_name=sheet_name,startcol=0, index=index)
    
 
def get_data_json(json_path):
    '''
    Parameters
    ----------
    json_path : TYPE D://data.json
        DESCRIPTION.

    Returns
    -------
    load_dict : TYPE dict
        DESCRIPTION. return a dict of data.

    '''
    import json
    try:
        f=open(json_path,"r",encoding="utf-8")
        load_dict=json.load(f)    
        return load_dict            
    except:
        f=open(json_path,"r",encoding="utf-8-sig")
        load_dict=json.load(f)    
        return load_dict

def write_to_json(json_path,my_dic):
    '''

    Parameters
    ----------
    json_path : TYPE string
        DESCRIPTION. D://data.json
        
    my_dic : TYPE dict or list
        DESCRIPTION. 
        type1: {"pans":1}
        type2: {"word":["a","b","c"]}
        type3: [{"pans":1},{"glenna":2}]
        type4: [{"word":["a","b","c"]},{"freq":[1,2,3,4,5,6]}]

    Returns
    -------
    None.

    '''
    import json
    f2 = open(json_path, "w", encoding="utf-8", errors="ignore")
    f2.write(json.dumps(my_dic,ensure_ascii=False)) #ensure_ascii=False 让中文不再乱码
    f2.close() 
    
def FilePath(root):
    '''读取所有文件，列出每个文件的路径'''
    Filelist=[]
    for home, dirs, files in os.walk(root):
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Filelist

def FileName(file_path):
    inter=os.path.basename(file_path)
    return inter


BigPunctuation="""!"#$&\'()*+,-/:;<=>?@[\\]^_`{|}.%~＂＃＄％＆＇?。（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。``''"""   #除去英文标点.%
StopTags="""◆: 、/ 。/ ---/ -/ --/ -- :/ ;/ ?/ ??/ ?┖ @/ [/ ]/ ^/ ‘/ ’/ "/ "/ 〈/ 〉/ 《/ 》/ 【/ 】/ >/ ∶/ ■/ ●/ ·/ …/ !/ #/ %,/ %/ \'/ (/ )/ */ +/ ,/ -/ // np v n w m a x t q j ni ns d i f u p g nz c r id s k h o e / #?/ --/""" #用来停用词性标注
Special="""∶ ■ ● ① ② ③ × ℃ Ⅲ ④ ⑤ ◆ ⑥ ± ⑦ ⑧ → ⑨ ▲ ⑩ ─ ÷ μ γ β Ⅱ Ⅰ ‰ □ 〇 ○ Ⅴ Ⅳ ★ ﹐ ° ※ ︰ α ― ≠ █ о θ ω ⒈ ⒉ ⒊ н ≤ ì ǎ ≥ р т с к й а и Ⅵ é è ﹢ ﹝ ﹞  ā ⒋ ù π ◇ Ω Ф ы Я п К в у м ǒ ü á ǔ ⒌ ⒍ 䦆 Ⅹ Ⅶ ← """
StopWords="""——— 》）， ）÷（１－ ”， ）、 ＝（ : → ℃  & * 一一 ~~~~ ’ .  『 .一 ./ --  』 ＝″ 【 ［＊］ ｝＞ ［⑤］］ ［①Ｄ］ ｃ］ ｎｇ昉 ＊ // ［ ］ ［②ｅ］ ［②ｇ］ ＝｛ } ，也  ‘ Ａ ［①⑥］ ［②Ｂ］  ［①ａ］ ［④ａ］ ［①③］ ［③ｈ］ ③］ １．  －－  ［②ｂ］ ’‘  ×××  ［①⑧］ ０：２  ＝［ ［⑤ｂ］ ［②ｃ］  ［④ｂ］ ［②③］ ［③ａ］ ［④ｃ］ ［①⑤］ ［①⑦］ ［①ｇ］ ∈［  ［①⑨］ ［①④］ ［①ｃ］ ［②ｆ］ ［②⑧］ ［②①］ ［①Ｃ］ ［③ｃ］ ［③ｇ］ ［②⑤］ ［②②］ 一. ［①ｈ］ .数 ［］ ［①Ｂ］ 数/ ［①ｉ］ ［③ｅ］ ［①①］ ［④ｄ］ ［④ｅ］ ［③ｂ］ ［⑤ａ］ ［①Ａ］ ［②⑧］ ［②⑦］ ［①ｄ］ ［②ｊ］ 〕〔 ］［ :// ′∈ ［②④ ［⑤ｅ］ １２％ ｂ］ ... ................... …………………………………………………③ ＺＸＦＩＴＬ ［③Ｆ］ 」 ［①ｏ］ ］∧′＝［  ∪φ∈ ′｜ ｛－ ②ｃ ｝ ［③①］ Ｒ．Ｌ． ［①Ｅ］ Ψ －［＊］－ ↑ .日  ［②ｄ］ ［② ［②⑦］ ［②②］ ［③ｅ］ ［①ｉ］ ［①Ｂ］ ［①ｈ］ ［①ｄ］ ［①ｇ］ ［①②］ ［②ａ］ ｆ］ ［⑩］ ａ］ ［①ｅ］ ［②ｈ］ ［②⑥］ ［③ｄ］ ［②⑩］ ｅ］ 〉 】 元／吨 ［②⑩］ ２．３％ ５：０   ［①］ :: ［②］ ［③］ ［④］ ［⑤］ ［⑥］ ［⑦］ ［⑧］ ［⑨］  …… —— ? 、 。 “ ” 《 》 ！ ， ： ； ？ ． , ． ' ?  · ——— ── ?  — < > （ ） 〔 〕 [ ] ( ) - + ～ × ／ / ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ Ⅲ В " ; # @ γ μ φ φ． ×  Δ ■ ▲ sub exp  sup sub Lex  ＃ ％ ＆ ＇ ＋ ＋ξ ＋＋ － －β ＜ ＜± ＜Δ ＜λ ＜φ ＜＜ = ＝ ＝☆ ＝－ ＞ ＞λ ＿ ～± ～＋ ［⑤ｆ］ ［⑤ｄ］ ［②ｉ］ ≈  ［②Ｇ］ ［①ｆ］ ＬＩ ㈧  ［－ ...... 〉 ［③⑩］ 第二 一番 一直 一个 一些 许多 种 有的是 也就是说 末##末 啊 阿 哎 哎呀 哎哟 唉 俺 俺们 按 按照 吧 吧哒 把 罢了 被 本 本着 比 比方 比如 鄙人 彼 彼此 边 别 别的 别说 并 并且 不比 不成 不单 不但 不独 不管 不光 不过 不仅 不拘 不论 不怕 不然 不如 不特 不惟 不问 不只 朝 朝着 趁 趁着 乘 冲 除 除此之外 除非 除了 此 此间 此外 从 从而 打 待 但 但是 当 当着 到 得 的 的话 等 等等 地 第 叮咚 对 对于 多 多少 而 而况 而且 而是 而外 而言 而已 尔后 反过来 反过来说 反之 非但 非徒 否则 嘎 嘎登 该 赶 个 各 各个 各位 各种 各自 给 根据 跟 故 故此 固然 关于 管 归 果然 果真 过 哈 哈哈 呵 和 何 何处 何况 何时 嘿 哼 哼唷 呼哧 乎 哗 还是 还有 换句话说 换言之 或 或是 或者 极了 及 及其 及至 即 即便 即或 即令 即若 即使 几 几时 己 既 既然 既是 继而 加之 假如 假若 假使 鉴于 将 较 较之 叫 接着 结果 借 紧接着 进而 尽 尽管 经 经过 就 就是 就是说 据 具体地说 具体说来 开始 开外 靠 咳 可 可见 可是 可以 况且 啦 来 来着 离 例如 哩 连 连同 两者 了 临 另 另外 另一方面 论 嘛 吗 慢说 漫说 冒 么 每 每当 们 莫若 某 某个 某些 拿 哪 哪边 哪儿 哪个 哪里 哪年 哪怕 哪天 哪些 哪样 那 那边 那儿 那个 那会儿 那里 那么 那么些 那么样 那时 那些 那样 乃 乃至 呢 能 你 你们 您 宁 宁可 宁肯 宁愿 哦 呕 啪达 旁人 呸 凭 凭借 其 其次 其二 其他 其它 其一 其余 其中 起 起见 起见 岂但 恰恰相反 前后 前者 且 然而 然后 然则 让 人家 任 任何 任凭 如 如此 如果 如何 如其 如若 如上所述 若 若非 若是 啥 上下 尚且 设若 设使 甚而 甚么 甚至 省得 时候 什么 什么样 使得 是 是的 首先 谁 谁知 顺 顺着 似的 虽 虽然 虽说 虽则 随 随着 所 所以 他 他们 他人 它 它们 她 她们 倘 倘或 倘然 倘若 倘使 腾 替 通过 同 同时 哇 万一 往 望 为 为何 为了 为什么 为着 喂 嗡嗡 我 我们 呜 呜呼 乌乎 无论 无宁 毋宁 嘻 吓 相对而言 像 向 向着 嘘 呀 焉 沿 沿着 要 要不 要不然 要不是 要么 要是 也 也罢 也好 一 一般 一旦 一方面 一来 一切 一样 一则 依 依照 矣 以 以便 以及 以免 以至 以至于 以致 抑或 因 因此 因而 因为 哟 用 由 由此可见 由于 有 有的 有关 有些 又 于 于是 于是乎 与 与此同时 与否 与其 越是 云云 哉 再说 再者 在 在下 咱 咱们 则 怎 怎么 怎么办 怎么样 怎样 咋 照 照着 者 这 这边 这儿 这个 这会儿 这就是说 这里 这么 这么点儿 这么些 这么样 这时 这些 这样 正如 吱 之 之类 之所以 之一 只是 只限 只要 只有 至 至于 诸位 着 着呢 自 自从 自个儿 自各儿 自己 自家 自身 综上所述 总的来看 总的来说 总的说来 总而言之 总之 纵 纵令 纵然 纵使 遵照 作为 兮 呃 呗 咚 咦 喏 啐 喔唷 嗬 嗯 嗳""" 
EnPunctuation="""!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""

def word_list(split_words):
    """

    Parameters
    ----------
    split_words : TYPE
        DESCRIPTION.['I','could',"n't",'believe','it','.','I','do',"n't",'like','it','.']

    Returns
    -------
    final_dic : TYPE
        DESCRIPTION. [('I', 2), ("n't", 2), ('it', 2), ('.', 2), ('could', 1), ('believe', 1), ('do', 1), ('like', 1)]

    """
    from collections import Counter
    my_dic=dict(Counter(split_words))
    final_dic=sorted(my_dic.items(),key=lambda x:x[1],reverse=True)
    return final_dic    
	
def clean_list(meta):
    """
    Parameters
    ----------
    meta : TYPE
        DESCRIPTION. list type # ['\n\n\t\t\t\t\t','来源：新民晚报','\xa0\xa0\xa0\xa0\n\t\t\t\t\t','\n\n\t\t\t\t\t\n\t\t\t\t\t\t','记者：陆梓华']

    Returns
    -------
    result : TYPE
        DESCRIPTION.
        string:
            来源：新民晚报
            记者：陆梓华
            作者：陆梓华
            编辑：裘颖琼
            2022-07-21 17:47
    """
    result="\n".join([line.strip() for line in meta if line.strip()!="|" and len(line.strip())!=0])
    return result

yhd=["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36','Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)','Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0','Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)','Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5','Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5','Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5','Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','NOKIA5700/ UCWEB7.0.2.37/28/999','Openwave/ UCWEB7.0.2.37/28/999','Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10','Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11','UCWEB7.0.2.37/28/999']
