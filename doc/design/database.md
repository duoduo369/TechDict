数据库设计
===

抓取表(PaperEduRaw)
---
数据原始表,除了需要的字段外保留抓回的整个页面

中文表 PaperEduKeyWordCN
---
word(词) unique
ManyToMany --> 抓取表(一个词对应多个原始数据,一个原始数据对应多个词)

英文表 PaperEduKeyWordEN
---
word(词) unique
ManyToMany --> 抓取表(一个词对应多个原始数据,一个原始数据对应多个词)
ManyToMany --> 中文表(一个中文对应多个英文，一个英文对应多个中文)
