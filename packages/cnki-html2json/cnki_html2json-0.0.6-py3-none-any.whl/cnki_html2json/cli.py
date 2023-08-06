import argparse
from cnki_html2json.core import start_crawl

def main():
    parser = argparse.ArgumentParser(description='CNKI crawler. Convert the html format of papers to json format.')
    parser.add_argument('-s','--start_paper_index',type=int,default=1,help='开始下载索引, 默认为1')
    parser.add_argument('-e','--end_paper_index',type=int,default=None,help='结束下载索引, 默认为None, 即下载到最后')
    parser.add_argument('-m','--mode',type=str,default='structure',help='模式: structure|plain|raw, 默认为structure')
    parser.add_argument('-save','--save_path',type=str,default='data',help='文件保存路径, 默认为当前目录的data文件夹')
    parser.add_argument('-wait','--wait_time',type=int,default=120,help='为检索预留的等待时间, 默认为120秒')
    parser.add_argument('-b','--browser_type',type=str,default='Chrome',help='浏览器类型: Chrome(default)|Firefox|Edge')
    parser.add_argument('--debug',action='store_false')
    args = parser.parse_args()
    start_crawl(start_paper_index = args.start_paper_index,
                end_paper_index = args.end_paper_index,
                mode = args.mode,
                save_path = args.save_path,
                log = args.debug,
                wait_time = args.wait_time,
                browser_type = args.browser_type,
                )
    
if __name__ == '__main__':
    main()