# Knowledge-Map-and-Question-Answer
毕业设计--面向高考招生咨询的问答系统设计与实现

## 如何导入该项目？
```shell
# 1. git clone 当前项目
git clone https://github.com/SangYuhiter/Knowledge-Map-and-Question-Answer.git

# 2. 新建Python 环境
python -m venv .venv

# 3.安装依赖库
pip install --upgrade pip
pip install -r requirements.txt

# 4.准备数据库信息
# 确定数据库链接的信息，默认是root@localhost 密码:123456
# 执行 InfomationGet/InsertAdmissionData.py 插入数据
cd InfomationGet
# create database and sheet
python MysqlOperation.py
# insert data
python InsertAdmissionData.py

# 5.打开软件
cd SystemUi
python QASystem.py
```


##### 【原题：毕业设计--基于知识图谱的大学领域知识自动问答系统的设计与实现】
### 一、InfomationGet:完成领域知识的获取和数据库构建工作
#### 1、Infomation:存储获取到的信息
##### (1)、九校联盟：C9数据--表格型（招生计划、录取分数(分省、分专业)）
##### (2)、大学：大学学科字段（百度百科）、常用问题集（C9常用问题集.csv）
#### 2、py文件
##### (1)、CreateFolder.py(创建文件夹--九校联盟)
##### (2)、InternetConnect.py(网络连接)
##### (3)、GetDictionaryData.py(获取相关词典数据)
##### (4)、GetPlanInfo.py(获取招生计划数据)
##### (5)、GetScoreInfo.py(获取录取分数数据)
##### (6)、MysqlOperation.py(MySQL数据库操作)
##### (7)、Neo4jOperation.py(Neo4j数据库操作)
##### (8)、InsertAdmissionData.py(MySQL数据库插入数据)
##### (9)、GetFrequentQuestion.py(获取高考网常用问题集数据)

### 二、FileRead:获取招生数据过程中的文件读取
#### 1、py文件
##### (1)、FileNameRead.py(读取文件名)
##### (2)、ImageRead.py(读取图片)
##### (3)、PDFRead.py(读取PDF(表格、文字))
##### (4)、XLSRead.py(读取excel表格)

### 三、HanLP：中文自然语言处理工具
#### 1、py文件
##### (1)、HanLPTest.py(HanLP测试)

### 四、LTP：中文自然语言处理工具
#### 1、ltp_data:LTP模型库+自定义词典文本
#### 2、py文件
##### (1)、LTPInterface.py(LTP使用接口)
##### (2)、XFYunWebAPI.py(讯飞云网络接口)

### 五、QuestionAnalysis:自然语言问句分析
#### 1、py文件
##### (1)、QuestionPretreatment.py(自然语言问句预处理（关键词：（**年份、学校、专业、地区**）识别与预处理）)
##### (2)、KeywordNormalize.py(关键词正则化)

### 六、SimilarityCalculate:相似度计算
#### 1、py文件
##### (1)、SemanticSimilarity.py(语义相似度计算，需要api)

### 七、TemplateLoad：模板加载
#### 1、Template:模板文件
#### 2、py文件
##### (1)、QuestionTemplate.py(问题模板的创建与加载)

### 八、QuestionQuery：自然语言问句查询
#### 1、py文件
##### (1)、MysqlQuery.py(MySQL表（admission_plan、admission_score_pro、admission_score_major）查询（可缺省关键词）)

### 九、SystemUI：自动问答系统设计
#### 1、images：UI图片
#### 2、py文件
##### (1)、QASystem.py(自动问答系统界面设计（自动问答+可选数据库目录查询）)

### 十、Log：日志系统
#### 1、py文件
##### (1)、Logger.py(自定义日志类（all.log+error.log,all.log可按时间每日切分）)