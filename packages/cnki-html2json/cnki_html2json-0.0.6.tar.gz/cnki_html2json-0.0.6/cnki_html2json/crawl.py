from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
import random
import sys
import math
from loguru import logger
from datetime import datetime

from cnki_html2json import _html2json
from cnki_html2json import parse_metadata
from cnki_html2json import recognize_slider_coordinate


def obtain_page_papers_url(driver) -> list:
    url_list = [i.get_attribute('href') for i in driver.find_elements(By.XPATH,'//*[@id="gridTable"]/table/tbody/tr/td[2]/a')]
    return url_list

def process_slider(driver):
    """判断是否进入验证码页面并进行验证"""
    recogize_count = 0
    while driver.find_elements(By.XPATH,'//span[@class="verify-msg" and text()="向右滑动完成验证"]'):
        
        recogize_count +=1 
        logger.info('进入验证码页面')
        time.sleep(3)
        back_img_str = driver.find_element(By.XPATH,'//div[@class="verify-img-panel"]/img[1]').get_attribute('src').split(',')[-1]
        cut_img_str = driver.find_element(By.XPATH,'//div[@class="verify-sub-block"]/img[1]').get_attribute('src').split(',')[-1]

        # 调用函数，获取缺口坐标
        x = recognize_slider_coordinate.recognize_slider(back_img_str, cut_img_str)[0]

        slider = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div[2]/div/div")
        ActionChains(driver).drag_and_drop_by_offset(slider, x*1.29, 0).perform()
        time.sleep(5)
    return recogize_count

def obtain_paper_html(paper_url:str,driver,mode:str)->dict:
    """获取论文的html页面,返回全部内容"""

    driver.execute_script("window.open('about:blank', '_blank');")
    # 获取所有窗口的句柄
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    driver.get(paper_url)
    time.sleep(3)

    metadata_html = driver.page_source
    metadata = parse_metadata.Parse(metadata_html).extract_metadata()
    
    # 点击进入html页面
    try:
        driver.find_element(By.XPATH,'//*[@id="DownLoadParts"]/div[2]/ul/li[2]/a').click()
    except:
        logger.error('论文未提供html页面')
        return concat_content(metadata,{'body_text':None,'citation':None})
    
    else:
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        time.sleep(10)

        # 调用判断验证码函数
        recogize_count = process_slider(driver)
        
        if recogize_count > 0:
            logger.info(f'验证码识别{recogize_count}次后通过')

        paper_raw_html = driver.page_source
        paper_dict = _html2json.ExtractContent(paper_raw_html,mode).extract_all()
        driver.close()
        if not paper_dict:
            logger.error('无法解析html页面')
        return concat_content(metadata,paper_dict)
      
    finally:
        driver.switch_to.window(handles[0]) 

def concat_content(metadata,paper_dict:dict)->dict:
    """将论文的元数据和正文内容合并"""
    return {**metadata,**paper_dict}

def jump_page(current_page:int,start_page:int,driver):
    """
    current_page:当前页面
    start_page:开始下载页面
    """
    while current_page < start_page:
        if current_page == 1:
            visible_page_index = list(range(1,10))
        else:
            visible_page_elements = driver.find_elements(By.XPATH,'//div[@class="pages"]/a[position() >= 3 and position() <= last()-1]')
            visible_page_index = [int(i.text) for i in visible_page_elements]

        if start_page in visible_page_index:
            driver.execute_script('window.scrollTo(0,0)')
            driver.find_element(By.XPATH,f'//a[@id="page{start_page}"]').click()
            time.sleep(3)
            logger.info(f'已跳转到指定的第{start_page}页')
            break
        
        else:
            driver.execute_script('window.scrollTo(0,0)')
            driver.find_element(By.XPATH,f'//a[@id="page{visible_page_index[-1]}"]').click()
            time.sleep(3)
            current_page = visible_page_index[-1]

        
def start_crawl(start_paper_index=1,end_paper_index=None,mode='structure',save_path='data',log=True,wait_time=120,browser_type='Chrome'):
    """
    start_paper_index:开始下载论文的索引
    end_paper_index:结束下载论文的索引
    mode:解析html页面的模式, 可选值为structure、plain和raw
    save_path:文件保存路径
    log:是否记录日志
    """
    if log:
        if not os.path.exists(f'{save_path}/log'):
            os.mkdir(f'{save_path}/log')
            logger.info(f'已在{save_path}文件夹下创建log文件夹')

        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        logger.add(f"{save_path}/log/{current_time}.log",format="{time} {level} {message}",level="INFO",mode='w')
        logger.info('本次任务记录日志')
    else:
        logger.info('本次任务不记录日志')

    visited_urls = set()

    if not os.path.exists(save_path):
        # os.mkdir(save_path)
        # logger.info(f'已在当前目录创建{save_path}文件夹')
        pass
    else:
        save_path_files = [i for i in os.listdir(save_path) if i.endswith('.json')]
        if save_path_files and start_paper_index==1:
            cover_risk = input(f'{save_path}文件夹中已存在json文件, 覆盖请输入y, 不覆盖请输入n, 程序将退出, 请输入: ')
            if cover_risk == 'y':
                logger.warning(f'新下载的文件将覆盖{save_path}文件夹里的文件')
            else:
                sys.exit('程序已退出')
            
    # 启动浏览器
    if browser_type=='Chrome':
        driver = webdriver.Chrome()
    elif browser_type=='Firefox':
        driver = webdriver.Firefox()
    elif browser_type=='Edge':
        driver = webdriver.Edge()
    # elif browser_type=='Safari':
    #     driver = webdriver.Safari()
    else:
        logger.error('不支持的浏览器类型')
        sys.exit('请选用合适的浏览器，程序已退出')

    logger.info(f'已启动 {browser_type} 浏览器')
    driver.get('https://kns.cnki.net/kns8/AdvSearch')
    
    # 完成检索的等待时间
    time.sleep(wait_time)
    logger.info(f'请在弹出的浏览器窗口中完成检索，{wait_time}秒后将自动开始下载')

    papers_per_page = 20 

    # 每页显示50条文献
    # driver.find_element(By.XPATH,'//*[@id="perPageDiv"]/div/i').click()
    # driver.find_element(By.XPATH,'//*[@id="perPageDiv"]/ul/li[3]/a').click()
    # papers_per_page = 50
    # time.sleep(3)
    
    # 总文献数量
    total_records_num = int(''.join(driver.find_element(By.XPATH,'//*[@id="countPageDiv"]/span[1]/em').text.split(',')))
    if end_paper_index:
        avaiable_records_num = min([total_records_num,end_paper_index,6000])
    else:
        avaiable_records_num = min([total_records_num,6000])
    
    need_download_num = avaiable_records_num-start_paper_index+1
    logger.info(f'总文献数量 {total_records_num} \t可下载文献数 {avaiable_records_num}' )
    
    start_page = start_paper_index//papers_per_page+1
    
    # 总页数
    # total_page_num = int(driver.find_element(By.XPATH,'//*[@id="countPageDiv"]/span[2]').text.split('/')[1])
    # print(f'总页数{total_page_num}')
    
    # 跳转到指定开始页面
    current_page = int(driver.find_element(By.XPATH,'//*[@id="countPageDiv"]/span[2]').text.split('/')[0])
    if current_page < start_page:
        jump_page(current_page,start_page,driver)
        current_page = start_page
    logger.info(f'将从第 {start_paper_index} 篇文献开始下载')
    logger.info(f'模式设置为 {mode}')
    minutes = math.ceil(need_download_num/3)
    if minutes < 60:
        logger.info(f'预计耗时 {minutes}分钟')
    else:
        logger.info(f'预计耗时 {minutes//60}小时 {minutes%60}分钟')
    
    # 下载文献数据
    current_paper_index = start_paper_index

    while current_paper_index < avaiable_records_num+1:
        current_url_list = obtain_page_papers_url(driver)[current_paper_index%papers_per_page-1:]  
        for url in current_url_list:
            
            # 避免重复下载
            if url in visited_urls:
                logger.error(f'已下载过 {url}')
                continue
            else:
                visited_urls.add(url)

            paper_content = obtain_paper_html(url,driver,mode)
            if paper_content['body_text'] is not None:
                with open(f'{save_path}/{current_paper_index}.json','w',encoding='utf-8') as f:
                    json.dump(paper_content,f,ensure_ascii=False,indent=4)
                    logger.info(f'success {current_paper_index} {paper_content["metadata"]["title"]}')
            else:
                logger.error(f'fail {current_paper_index} {paper_content["metadata"]["title"]}')
            time.sleep(random.randint(3,5))
            current_paper_index += 1
        
            if current_paper_index == avaiable_records_num+1:
                logger.info('下载完成')
                driver.quit()
                sys.exit('下载完成，程序已退出')
                
        logger.info(f'第 {current_page} 页下载完成')
        
        # 点击下一页
        driver.find_element(By.ID,'PageNext').click()

        time.sleep(5)

        # 关闭第一页之外的其他窗口
        handles = driver.window_handles
        for i in range(1,len(handles)):
            driver.switch_to.window(handles[i])
            time.sleep(1)
            driver.close()
    
        driver.switch_to.window(handles[0])
        time.sleep(60)
        current_page += 1

        if current_page%100 == 0:
            time.sleep(300)
            