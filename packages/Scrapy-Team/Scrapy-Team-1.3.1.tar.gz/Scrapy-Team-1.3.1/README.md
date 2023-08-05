![016af05cdfc247a801214168e1c955](https://ryan-1307030779.cos.ap-nanjing.myqcloud.com/vscode-md016af05cdfc247a801214168e1c955.jpg)
scrapy-team
=========
Scrapy-team A framework for teamwork based on scrapy

- Package many pipeline files

- Package the Item pipeline files involved in PDF processing

- A Spidermiddleware file is packaged to handle item requests 

scrapy-team 基于scrapy的团队合作模式框架

主要：

- 打包了诸多pipeline管道文件

- 打包处理了涉及pdf处理的item管道文件

- 打包处理了关于item请求的spidermiddleware文件


[ContactProjectTeam](https://github.com/buliqioqiolibusdo)


Usage：
========
#### 2023/04/04 scrapy-team==1.3.1
* ADD : 新增 bloomfilter 爬虫类 >> [跳转查看示例](#bloomfilter_spider)
* DEBUG : BloomFilterPipeline dropitem
* CHANGE : BloomFilterPipeline 调高默认配置管道优先级

#### 2023/03/31 scrapy-team==1.3.0
* ADD : 新增 oracle 存储管道
* ADD : 新增参数`TARGET_TABLE` 指定存储`item.table`集合位置,不分月表
* CHANGE : MQ管道配置获取变更
* DEBUG : OssOtherFilesPipeline Item 判断异常
* DEBUG : OssPDFPipeline 拼接异常

#### 2022/10/11 scrapy-team==1.2.16
* CHANGE : 对象存储命名规则变更成hash文件流得值
* DEBUG : otherpdfpipeline组件 item 类筛选判断异常
* DEBUG : otherpdfpipeline组件 空url时异常
* DEBUG : mongopipeline组件 空dict 类型判断异常

#### 2022/9/30 scrapy-team==1.2.15
* 增加功能 : mongo管道对`all_json`/`list_json`/`raw_other_pdf_url`/`other_pdf_url`纠正数据类型
* DEBUG : 管道继承出错,图片管道出现img转pdf情况,
  * 注册文件中增加pdf管道选项,用于区分原先文件管道
#### 2022/9/29 scrapy-team==1.2.14
* DEBUG : 修复安装错误,约束依赖版本
* DEBUG : 修改otherpdfpipeline管道中,文件是否有效的判断逻辑
* DEBUG : `SSL.SSLv3_METHOD` 报错
#### 2022/9/28 scrapy-team==1.2.13
* 增加功能 : 文件管道运行过程中遇到指定位置pdf文件时, 做失效PDF处理 >> [跳转查看示例](#invalid_pdf)
* 增加功能 : 文件管道传入图片链接后,输出转化成pdf链接 >> [跳转查看示例](#pipeline_img_to_pdf)
* 增加功能 : otherfile转存管道 >> [跳转查看示例](#otherfilepipelines)
* 增加功能 : 上传oss对象存储增加响应判断, 对于非200状态码的上传操作,PDF做失效处理
* 增加功能 : etl进度提示功能 >> [跳转查看示例](#etl_progress)
* DEBUG : 修复下载中间件引用空cfg配置
* DEBUG : 修复item._refer 和 item._header 相关功能
* 优化功能 : 优化pdf损坏判断 
#### 2022/8/3 scrapy-team==1.2.12
* 修复:下载管道检测文件不符合时返回空字符串,出现pdf_urls="|".join(["pdf_url",""])局面
* 整合自建代理池功能,增加随机代理权重参数 >> [跳转查看示例](#proxy_random_weights)
* 新增 prjclear 用于清理切换分支遗留的缓存文件和文件夹 >> [跳转查看示例](#prjclear)
* 新增 etl 用于转移数据 >> [跳转查看示例](#etl)
#### 2022/7/7 scrapy-team==1.2.11
* 回滚:mysql管道异步存储,存在断开连接情况
* 新增:资讯item
* 新增:参数CLOSESPIDER_ERROR_STATUS<tuple> :: (<错误状态码>, <出现次数>)
    * 表示出现指定多少次状态码之后主动关闭爬虫
#### 2022/6/13 scrapy-team==1.2.10
* 保留scrapy基础命令,将team模式命令独立出来,创建团队项目使用newteam代替startproject,创建爬虫用jointeam代替genspider,运行爬虫用runteam或者crawl
* 新增命令辅助创建爬虫注册配置
* 存库管道集体变更成异步存储
#### 2022/5/31 scrapy-team==1.2.8
* 更改mongo管道存储月表
#### 2022/5/12 scrapy-team==1.2.5
* 参数`ITEM_HEADER`用作配置下载字段,不同域名的文件链接使用不同的请求头下载
     ```
     # eg. setting中配置
     'ITEM_HEADER' : {
            "4donline.ihs.com":{
                'Host': '4donline.ihs.com',
                'Referer': 'https://www.findchips.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                    },
            'datasheet.datasheetarchive.com':{
                'Host': 'datasheet.datasheetarchive.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                    },
    }
     ```
* 修正布隆过滤器日志警告异常
* 更新环境依赖shell
#### 2022/5/10 scrapy-team==1.2.0
* 新增布隆过滤器item管道,指定Data_Size(估算数据量)和Aim_Set(除重字段)后对爬虫名下整周期item进行除重过滤
* 向下兼容scrapyer 1.5.6版本 对不存在scrapy.cfg项目进行部分兼容
* 为避免重复引用中间件和管道,对custom_settings中引用"scrapy.xcc_"开头模块进行限制
    * 示例:
    ```python
    # 如果以scrapy.xcc_配置中间件 DOWNLOADER_MIDDLEWARES将整体失效
    custom_settings = dict(
        DOWNLOADER_MIDDLEWARES = {
            'gerapy_pyppeteer.downloadermiddlewares.PyppeteerMiddleware': 542,
            'scrapy.xcc_downloadermiddlewares.randuamiddleware.RandownUserAgent': 543,
        }
    )
    ```
* 管道与中间件配置从cfg硬替换custom_settings模式,切换成cfg配置update补充custom_settings模式
* 修正了双日志异常情况
* 新增shell脚本安装更新环境,对冲突依赖进行剔除
* 增加pdf检测损坏功能,并对eof缺失部分进行补全后检测(持续跟进pdf种类变化)

#### 2022/5/6 scrapyer==1.5.11
* 新增 spider_register 爬虫注册机制，爬虫名集中配置，爬虫类中不用name属性，组件使用开关情况也在配置中写明
* 修改阶梯配置 spider_register未指定的取custom_settings模块管道配置
* 默认将所有scrapy框架非基础组件关闭


#### 2022/4/25 scrapyer==1.5.8
* ~~设置switch_register 管道组件注册机智~~
* ~~重新规则settings文件，默认将所有scrapy框架组件打开~~
* scrapy.cfg中正式，测试双配置，中间件通过.bashrc IF_PROD 判断是否是正式环境
* 爬虫随机代理修改为请求随机代理
* 修改创建项目和爬虫命令，按人物>项目>爬虫名分层结构创建，一并生成main文件
* 阿里云资源链接目录更改为hash方式处理

### 目录结构
```
├─Command(命令流程)
├─Scrapy_Prj(Scrapy物料采集项目)
|  ├─middlewares
|  ├─pipelines
|  ├─items.py
|  ├─settings
|  └─spiders
|      ├─xxxx(role)
|      └─...
├─Non_Scrapy_Prj(非Scrapy项目)
│  ├─...(feapder/asycio/multiprocessing)
├─.gitignore(git忽略文件)
├─requirements.txt(依赖库)
├─Team_Public(公共方法公共配置)
└─....
```

* 拉代码,ide创建个人分支

* 创建环境
* 安装依赖
    > 运行init环境依赖
    ``` 
   $pwd$ \Command\_win_env_init.bat
   eg: e:\news\Command\_win_env_init.bat
    ```


* 创建爬虫项目
    ```
    scrapy newteam <someprj>
    eg: scrapy newteam saas
    ```
    * 备注: 创建项目(scrapy.cfg保有单一存库方式正式和测试各一套配置,如果存在不同项目存不同mongo情况建议分出来单独项目)

* 创建爬虫文件以及配置
    ```
    scrapy jointeam <somebody> <somewebsite> <somecrawl>
    eg: scrapy jointeam zhizhong semiee detailcrawl
    ```

* 单项目完成后推代码到gitlab
* 定期review合并代码,pull到DEMP中设置周期调度并监控速度及异常



<p id="proxy_random_weights"></p> 

##### 新增随机代理权重值

* 用法一：在scrapy.cfg文件的代理配置的WEIGHTS中添加权重参数（scrapy.cfg为项目公用文件，不可私自配参）

```
    ## 例如：
    [proxy_no.1_cfg]
    # Self-built domestic tunnels
    PROXY_USER= iceasy
    PROXY_PASS= xcc2022
    PROXY_SERVER= http://10.8.108.201:9900 
    WEIGHTS = 7/10
```


* 用法二：项目在爬虫文件custom_settings中添加（特殊项目需要调整，询问后在爬虫文件中调参）
```
    ## 表示取scrapy.cfg中诸多代理隧道配置，其中如proxy_no.1_cfg配置的权重为1/<权重值合计>，例如当前表示随机到proxy_no.1_cfg代理配置的概率为1/7
    custom_settings = dict(
        PROXIES_WEIGHTS={
            "proxy_no.1_cfg":1,
            "proxy_no.1.1_cfg":1,
            "proxy_no.1.2_cfg":1,
            "proxy_no.2_cfg":1,
            "proxy_no.3_cfg":1,
            "proxy_no.4_cfg":1,
            "proxy_no.5_cfg":1,
        }
    )
```

<p id="prjclear"></p> 

##### scrapy prjclear 用法说明

* 用法：  "scrapy prjclear <path>"

```
    ## 例如：
    scrapy prjclear 
    或者：
    scrapy prjclear Scrapy_Prj
```


<p id="etl"></p> 

##### scrapy etl 用法说明

* 用法：  "scrapy etl <Set Name> <Filter Key> <Filter Value> <Aim Set Name>"
* 注意 可支持pymongo==3.12.0版本，高版本可能不支持

```
    ## 例如：将scrapy.cfg 中dev库筛选数据转移到prod库
    scrapy etl ware_category_copy brand_name Winsemi
```


<p id="invalid_pdf"></p> 


##### 对于oss文件管道
  * 设置中指定失效的PDF路径 `FILTER_INVALID_FILE_PATHS`<list> 在爬取过程中判断并作失效PDF处理.


<p id="pipeline_img_to_pdf"></p> 


##### 对于oss文件管道
  * 示例:传入图片地址后自行转化成pdf转存链接
    ```
        2022-09-28 22:46:25 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.baidu.com>
        {'pdf_url': 'https://xcc2.oss-cn-shenzhen.aliyuncs.com/items/202209/31e50a13c/b68a2160bd3874a5fcb0184c0e86b7727618e10d.pdf',
        'raw_pdf_url': 'https://pic1.zhimg.com/50/v2-eeb4193a1ac0dac9237197f7838aec6a_720w.jpg?source=b1f6dc53|https://pic2.zhimg.com/50/v2-f463d84e2fe64b7580bfaee676b003b6_720w.jpg?source=b1f6dc53'}
        2022-09-28 22:46:25 [scrapy.core.engine] INFO: Closing spider (finished)
    ```



<p id="etl_progress"></p> 

##### 提示

```
D:\de-factory>scrapy etl ware_detail_dataplatform sources sexxxx  
208263it [09:57, 348.58it/s]
completed~
```


<p id="otherfilepipelines"></p> 

##### ossotherfilepipelines 用法说明

* 同`ossfilepipelines`,在注册文件管道tuple中添加 `other_file`或者`other_file_bak`
* 配置参数


- **实现功能**

\# 下载失败留空字符串
\# 检测文件类型不为html否则置空
\# 若为pdf类型则检测是否为有效文件



- **spider配置文件**

```python
增加：
FILE_PIPE_CONFIG={
    'OssOtherFilesPipeline':
        {'FILES_OSS_URLS_FIELD': 'raw_other_pdf_url',
         'FILES_OSS_RESULT_FIELD': 'other_pdf_url',
         'RESOURCE_CLASSNAME': 'FactoryMaterialItem'},
    'OssOtherFilesPipelineBak':
        {'FILES_OSS_URLS_FIELD': 'raw_other_pdf_url',
         'FILES_OSS_RESULT_FIELD': 'other_pdf_url',
         'RESOURCE_CLASSNAME': 'FactoryMaterialItem'},
}
```

- **raw_other_pdf_url  other_pdf_url 的字段数据结构**

```python
{
"file_name_1": "url"<string>,
"file_name_2": "url"<string>,
"file_name_3": "url|url"<string>,
}

示例：
raw_other_pdf_url = {"数据表": "https://xcc2.oss-cn-shenzhen.aliyuncs.com/paper/Paper_caj/b7da5fe15fce7b8b8f66d865f58c3e6c91c75c00.caj|https://xcc2.oss-cn-shenzhen.aliyuncs.com/paper/Paper_caj/5b9cd0ca29a03ba0686854a4607396ea4a9d1f071111111111.caj",
                     'aaa':"https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201801&filename=1017836624.nh&uniplatform=NZKPT&v=DklNvEDPEikIGdvw3PeDxOxJWn44i8PZJVwTj7gznh1YmjxppRdDBaf8ykoSjhNu",
                     'zip':"https://xcc2.oss-cn-shenzhen.aliyuncs.com/li_pdf/Manufacturers_Pdf/143497617822cc442c2014c593c46c53f4cf5254111111.zip",
                     "jpg":"https://xcc2.oss-cn-shenzhen.aliyuncs.com/items/7505d64a5/87dc6fd833f4eb078a63520aed2143e3abbe6057.jpeg|https://www.mouser.cn/images/lairdconnectivity/images/LI0201B800R_series_SPL.jpg",
                     "环境文件":"https://www.mouser.com/catalog/additional/ADI_5843_RoHS_Certificate.pdf|https://www.mouser.com/catalog/additional/ADI_5843_RoHS_Certificat1111111111e.pdf",
                     'error':"https://xcc2.oss-cn-shenzhen.aliyuncs.com/li_pdf/Manufacturers_Pdf/0a6474a5d3afe86d5c7ab2c17057f1e5973fc27e.pdf",
                     "test":"https://xcc2.oss-cn-shenzhen.aliyuncs.com/ye_img/Manufacturers_Img/41ffafc006d5ad73d60851eede7ba3d3fcc296c2.bmp"}
```




<p id="bloomfilter_spider"></p> 

##### 新增bloomfilter 爬虫类

```

继承爬虫类 BloomFilerSpider / BloomFilterRedisSpider(功能同scrapy-redis:RedisSpider)
from scrapy.spiders.bloomfilter import BloomFilterSpider,BloomFilterRedisSpider

usage:
...
def parse(self, response):
    item = {"title":"stm32f","sources":"findchips","brand_name":"te",}
    if self.bloomfilter.throw(item):  # throw to 集合 存在返回True 不存在insert并返回 False
        print("集合存在")
    else: 
        print("集合不存在,并入集合")

    print("检查字符串是否in集合: ",self.bloomfilter.lookup("findchips_te_stm32f")) # 检查字符串是否in集合
...
```


