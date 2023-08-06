"""html2json核心模块, 提供功能入口"""

from cnki_html2json import _html2json
from cnki_html2json import crawl
import json

def export_json(text,json_path):
    """导出json文件"""
    with open(json_path,'w',encoding='utf-8') as f:
        json.dump(text,f,ensure_ascii=False,indent=4)

def html2json(paper_html:str,mode:str='structure',export=False,export_path=None):
    """将论文的html字符串转换为字典
    paper_html: 论文的html字符串
    mode: 模式，structure|plain|raw，默认为structure
    export: 是否导出json文件，默认为False
    export_path: 导出json文件的路径，默认为None，如果导出json文件，该参数必须指定
    """
    result = _html2json.ExtractContent(paper_html,mode).extract_all()
    if not export:
        return result
    else:
        if export_path is None:
            raise ValueError('请设置导出参数')
        else:
            export_json(result,export_path)


def start_crawl(start_paper_index=1,end_paper_index=None,mode:str='structure',save_path='data',log=True,wait_time=120,browser_type='Chrome'):
    """爬取cnki网站的论文
    start_paper_index: 开始爬取的论文索引，默认为1
    end_paper_index: 结束爬取的论文索引，默认为None，即爬取到最后
    mode: 模式，structure|plain|raw，默认为structure
    save_path: 下载文件的保存路径，默认为当前目录的data文件夹
    log: 是否保存日志，默认为True
    wait_time: 为检索预留的等待时间，单位为秒
    browser_type: Chrome(默认)|Firefox|Edge|Safari
    """
    crawl.start_crawl(start_paper_index = start_paper_index,
                      end_paper_index = end_paper_index,
                      mode = mode,
                      save_path = save_path,
                      log = log,
                      wait_time = wait_time,
                      browser_type = browser_type)
