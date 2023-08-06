# -*- coding: utf-8 -*-
# from lxml import etree
from lxml import html
import re

def extract_nodes(long_nodes_list:list,short_nodes_list:list):
	"""提取两个节点列表的差集"""
	if short_nodes_list:
		result = []
		for node in long_nodes_list:
			if node not in short_nodes_list:
				result.append(node)
			else:
				return result
	else:
		return long_nodes_list

def concat_nodes_value(nodes_list,task:str):
	"""合并节点列表的值"""

	if nodes_list:
		if task == 'citation':
			try:
				result = sorted({int(i) for i in [node.text for node in nodes_list if node.text is not None]})
			except ValueError:
				result = sorted({int(i) for i in [eval(node.text)[0] for node in nodes_list if node.text is not None]})
			return result
		
		else:
			result = ' '.join([node.text.strip() for node in nodes_list if node.text is not None])
			return result.strip()
	return None

def process_level_2_chapter(level_2_chapter:list):
	"""处理第二级章节标题"""
	chapters = []
	unnormal_chapters = {}
	for idx, chapter in enumerate(level_2_chapter):
		if re.match(r'^\d{1}[\.．]{1}\d{1}\.?\d?\s*\w+',chapter):
			chapters.append(chapter)
		elif re.match(r'^\d{1}[\.．]{1}\d{1}\.?\d?\s*$',chapter):
			chapters.append(level_2_chapter[idx+1])
			unnormal_chapters[chapter] = level_2_chapter[idx+1]
	return chapters, unnormal_chapters

def process_level_1_chapter(level_1_chapter:list):
	"""处理第一级章节标题"""
	chapters = []
	unnormal_chapters = {}
	for idx, chapter in enumerate(level_1_chapter):
		if re.match(r'^[0-9一二三四五六七八九][\s\.、．]*\D*[\u4e00-\u9fa5]+',chapter):
			chapters.append(chapter)
		elif re.match(r'^[0-9一二三四五六七八九][\s\.、．]*[^\u4e00-\u9fa5]*',chapter):
			chapters.append(level_1_chapter[idx+1])
			unnormal_chapters[chapter] = level_1_chapter[idx+1]
		elif re.match('作者贡献声明|利益冲突声明|参考文献|注释',chapter):
			chapters.append(chapter)
	# 去重
	chapters_ = []
	for i in chapters:
		if i not in chapters_:
			chapters_.append(i)
	return chapters_, unnormal_chapters

class ExtractContent:
	"""提取文献内容"""

	def __init__(self,resp_content:str,mode:str="structure") -> None:

		"""
		resp_content: html字符串
		mode: structure:提取结构化文本(默认); plain:提取纯文本; raw:原生格式，会在正文中保留参考文献文献的索引
		"""
		self.content = resp_content
		# self.content = resp_content.replace('<!DOCTYPE html>','').strip()
		self.html_general = html.fromstring(self.content)
		
		if mode != "raw":
			self.html_text = html.fromstring(re.sub('<citation.*?</citation>|<sup>.*?</sup>|<i>.*?</i>','',self.content,flags=re.S))
		
		elif mode=="raw":
			
			# 匹配并替换
			pattern = r'<citation.*?>.*?</citation>'
			content_ = self.content
			for match in re.findall(pattern,self.content):
				match_result = '{}'.format([int(i) for i in re.findall(r'<a class="sup">(\d+)</a>',match)])
				content_ = content_.replace(match,match_result)
			self.html_text = html.fromstring(re.sub(r'<sup>.*?</sup>|<i>.*?</i>','',content_,flags=re.S))

		self.error = False
		self.annotation = False
		self.no_structure = False
		self.prefix = False
		self.mode = mode
		
		try:
			level_1_chapter:list = self.html_general.xpath('//h3//text()')
			self.level_1_chapter,self.unnormal_level_1_chapter = process_level_1_chapter(level_1_chapter)
			if self.unnormal_level_1_chapter:
				self.unnoraml_level_1_chapter_reverse = {v:k for k,v in self.unnormal_level_1_chapter.items()}
			
		except AttributeError:
			self.error = True
		
		else:
			# 判断是否是正常文章
			if "参考文献" not in self.level_1_chapter:
				self.error = True
			
		if not self.error:

			self.level_1_chapter_num = len(self.level_1_chapter)

			original_level_2_chapter:list = self.html_general.xpath('//h4//text()')
			self.level_2_chapter,self.unnormal_level_2_chapter = process_level_2_chapter(original_level_2_chapter)

			self.text = {}
			
			# 判断是否存在没有章节标题的前言
			if prefix := self.html_text.xpath('//h3[1]/preceding-sibling::div[@class="p1"]/p'):
				prefix_text = concat_nodes_value(prefix,'text')
				prefix_citaion_index = concat_nodes_value(
					self.html_general.xpath('//h3[1]/preceding-sibling::div[@class="p1"]/p/citation/sup/a'),'citation')
				self.text = {'0':{'citation':prefix_citaion_index,'text':prefix_text}}
				self.prefix=True

			# 处理没有篇章结构的文章
			if self.level_1_chapter_num==0:
				prefix_ = self.html_text.xpath('//div[@class="brief"][last()]/following-sibling::div[@class="p1"]/p')
				if prefix_:
					prefix_text = concat_nodes_value(prefix_,'text')
					prefix_citaion_index = concat_nodes_value(
						self.html_general.xpath('//div[@class="brief"][last()]/following-sibling::div[@class="p1"]/p/citation/sup/a'),'citation')
					self.text = {'0':{'citation':prefix_citaion_index,'text':prefix_text}}
					self.no_structure = True
			
			self.text |= {k:{} for k in self.level_1_chapter if k!='参考文献'}
	
	def generate_xpath(self,chapter_name:str,chapter_class:int,task:str,add_b_label = False,add_font_label=False):
		"""生成xpath
		:param chapter_name: 章节名称
		:param chapter_class: 章节等级,取1或2
		"""

		if add_font_label==True:
			xpath_ = f'//h{chapter_class+2}/font[text()="{chapter_name}"]/../following-sibling::div/p/font'
			if task == 'citation':
				xpath_ += '/citation/sup/a'
			return xpath_
		
		elif add_b_label==True:
			xpath_ = f'//h{chapter_class+2}/b[text()="{chapter_name}"]/../following-sibling::div/p'
			if task == 'citation':
				xpath_ += '/citation/sup/a'
			return xpath_
		
		else:
			xpath_ = f'//h{chapter_class+2}[text()="{chapter_name}"]/following-sibling::div/p'
			if task == 'citation':
				xpath_ += '/citation/sup/a'
			return xpath_
		
	def obtain_nodes_list(self,chapter_name:str,chapter_class:int,task:str):
		"""获取节点列表，依次尝试三种xpath表达式"""
		
		if task == 'text':
			self.html = self.html_text
		elif task == 'citation':
			self.html = self.html_general

		xpath_expression = self.generate_xpath(chapter_name,chapter_class,task)
		if result:=self.html.xpath(xpath_expression):
			return result
		
		else:
			xpath_expression = self.generate_xpath(chapter_name,chapter_class,task,add_b_label=True)
			if result:=self.html.xpath(xpath_expression):
				return result
		
			else:
				xpath_expression = self.generate_xpath(chapter_name,chapter_class,task,add_font_label=True)
				return self.html.xpath(xpath_expression)
	
	def extract_plain_text(self):
		
		"""提取纯文本"""
		if self.no_structure:
			return self.text['0']['text'] # type: ignore
		
		else:
			total_nodes_list = self.obtain_nodes_list(self.level_1_chapter[0],1,'text')
			total_text = concat_nodes_value(total_nodes_list,'text')
			
			if self.prefix:
				return self.text['0']['text']+' '+total_text # type:ignore
			else:
				return total_text

	def extract(self,task:str)->None:
		
		if self.error:
			self.text = None
			return None
		
		offset = 1
		if not self.annotation and "注释" in self.level_1_chapter:
			offset = 2

		idx = 0
		while idx < self.level_1_chapter_num-offset:
			first_nodes_list = self.obtain_nodes_list(self.level_1_chapter[idx],1,task)
			second_nodes_list = self.obtain_nodes_list(self.level_1_chapter[idx+1],1,task)

			# 筛选出二级章节
			current_node_idx = self.level_1_chapter[idx].strip()[0]
			
			if current_node_idx in list('123456789'):
				current_level_2_chapter_list = [i for i in self.level_2_chapter if i[0]==current_node_idx]
				if self.unnormal_level_2_chapter:
					current_level_2_chapter_list += [self.unnormal_level_2_chapter[i] for i in self.unnormal_level_2_chapter if i[0]==current_node_idx]
			else:
				current_level_2_chapter_list = []
			
			if current_level_2_chapter_list:
				
				text_ = {}
				current_level_2_chapter_num = len(current_level_2_chapter_list)
				idx_ = 0
				while idx_ < current_level_2_chapter_num:
					first_nodes_list_ = self.obtain_nodes_list(current_level_2_chapter_list[idx_],2,task)
		
					if idx_ == current_level_2_chapter_num-1:
						second_nodes_list_ = second_nodes_list

					else:
						second_nodes_list_ = self.obtain_nodes_list(current_level_2_chapter_list[idx_+1],2,task)
			
					if idx_ == 0:
						following_node_ = extract_nodes(first_nodes_list,first_nodes_list_)
						text_[current_node_idx+'.0'] = concat_nodes_value(following_node_,task)

					current_node_ = extract_nodes(first_nodes_list_,second_nodes_list_)

					current_level_2_chapter = current_level_2_chapter_list[idx_]
					unnoraml_level_2_chapter_reverse = {v:k for k,v in self.unnormal_level_2_chapter.items()}

					if current_level_2_chapter in unnoraml_level_2_chapter_reverse:
						text_[unnoraml_level_2_chapter_reverse[current_level_2_chapter]+current_level_2_chapter] = concat_nodes_value(current_node_,task)
					else:
						text_[current_level_2_chapter_list[idx_]] = concat_nodes_value(current_node_,task)

					idx_ += 1
				self.text[self.level_1_chapter[idx]][task] = text_ # type: ignore

			else:
				current_node_ = extract_nodes(first_nodes_list,second_nodes_list)
				current_level_1_chapter = self.level_1_chapter[idx]

				self.text[current_level_1_chapter][task] = concat_nodes_value(current_node_,task) # type: ignore
		
			idx += 1

	def extract_citation_index(self):
		"""提取章节引用的文献索引"""

		self.extract(task='citation')
		return self.text
	
	def extract_text(self):
		"""提取正文"""
		
		self.extract(task='text')
		return self.text

	def extract_citation(self):
		"""提取参考文献"""
		citation = [doc.strip() for doc in self.html_general.xpath('//div[@id="a_bibliography"]/p/a/text()') if doc.strip()!='']
		citation_with_index = [f'[{idx}] '+re.sub(r'^[\.]+','',doc).strip() for idx,doc in enumerate(citation,1)]
		return citation_with_index

	def extract_all(self)->dict:
		"""提取全部"""
		if self.error:
			return {'body_text':None,'参考文献':None}
		
		result = {}
		citing_docs = self.extract_citation()
		if self.mode != 'plain':
			self.extract_citation_index()
			self.extract_text()
			result = {'body_text':self.text}
		
		elif self.mode == 'plain':
			result = {'body_text':self.extract_plain_text()}
		
		# result |= {'参考文献':citing_docs}
		return {**result,**{'参考文献':citing_docs}}
	
if __name__ == '__main__':
	with open('test/fulltext.html','r',encoding='utf-8') as f:
		content = f.read()
	import json
	with open('examples/raw_text.json','w',encoding='utf-8') as f:
		json.dump(ExtractContent(content,'raw').extract_all(),f,ensure_ascii=False,indent=4)
