# xiezuocat-python
对智能纠错、智能改写、AI写作、单点登录签名算法进行封装
## 一、pip引入
```python
pip install xiezuocat
```

## 二、调用示例
### 1、智能纠错
#### 调用示例
```python
import xiezuocat
import json
my_xiezuocat = xiezuocat.Xiezuocat({your-secretKey})
check_data = json.dumps({
            "texts": [
                "哈哈哈。我天今吃了一顿饭",
                "我想念十分赵忠祥。嘿嘿嘿。"
            ]
        })
check_result = my_xiezuocat.check(check_data)
print(check_result)
```
#### 返回结果
```json
{
  "errCode" : 0,
  "errMsg" : "",
  "data" : null,
  "alerts" : [ [ {
    "alertType" : 4,
    "alertMessage" : "建议用“今天”替换“天今”。",
    "sourceText" : "天今",
    "replaceText" : "今天",
    "start" : 5,
    "end" : 6,
    "errorType" : 3,
    "advancedTip" : true
  }, {
    "alertType" : 2,
    "alertMessage" : "根据段落，句子应已完结，句尾建议添加句号",
    "sourceText" : "饭",
    "replaceText" : "。",
    "start" : 11,
    "end" : 11,
    "errorType" : 2,
    "advancedTip" : false
  } ], [ {
    "alertType" : 4,
    "alertMessage" : "建议用“十分想念”替换“想念十分”。",
    "sourceText" : "想念十分",
    "replaceText" : "十分想念",
    "start" : 1,
    "end" : 4,
    "errorType" : 3,
    "advancedTip" : false
  } ] ],
  "checkLimitInfo" : {
    "checkWordCountLeftToday" : "997268",
    "totalCheckWordCountLeft" : "997268",
    "expireDate" : "2024-02-02 00:00:00"
  }
}
```
### 2、智能改写
##### 调用示例
```python
import xiezuocat
import json
my_xiezuocat = xiezuocat.Xiezuocat({your-secretKey})
rewrite_data = json.dumps({
  "items": [
    "一般"
  ],
  "level": "middle"
})
rewrite_result = my_xiezuocat.rewrite(rewrite_data)
print(rewrite_result)
```
##### 返回结果
```json
{
  "errcode" : 0,
  "errmsg" : null,
  "items" : [ "普通" ],
  "stat" : "997268"
}
```

### 3、AI写作
#### 创建生成任务
##### 调用示例
```python
import xiezuocat
import json
my_xiezuocat = xiezuocat.Xiezuocat({your-secretKey})
generate_params = json.dumps({
    "type": "Step",
    "title": "飞机",
    "length": "default"
})
result = my_xiezuocat.generate(generate_params)
print(result)
```
##### 返回结果
```json
{
  "errCode" : 0,
  "errMsg" : "success",
  "data" : {
    "docId" : "ffa614ac-631f-4e7d-b0ea-b5ac43670e59"
  }
}
```

#### 获取生成结果
##### 调用示例
```python
import xiezuocat
my_xiezuocat = xiezuocat.Xiezuocat({your-secretKey})
doc_id = "ffa614ac-631f-4e7d-b0ea-b5ac43670e59" # 此处docId为第一步生成的结果
result = my_xiezuocat.get_generate_result(doc_id)
print(result)
```
##### 返回结果
```json
{
  "errCode" : 0,
  "errMsg" : "success",
  "data" : {
    "status" : "FINISHED",
    "result" : "飞机\n飞机是一种用于军事、民用、工业及运输的飞行器。在20世纪，飞机被广泛应用于军事和民用领域，成为现代军事和民用工业中最主要的组成部分。它在现代社会有着非常重要的作用，是一个国家综合实力及经济实力的体现。它与航空、航天事业一起成为世界上具有最广泛影响力的三大航空产业之一。\n发展历史\n飞机的发展史，其实是人类不断探索和发展的历史。从最早的飞机，到二战期间以英国人发明的F-104 “闪电”战机为标志的喷气式战斗机，再到上世纪50年代以后，各国在飞机技术上取得的重大突破，几乎都是在二战期间才开始形成并发展起来的。从20世纪50年代末直到今天，世界航空科技研究在高速发展。以美国为例，20世纪50年代至60年代初仅进行了一系列重大试验就获得了大量专利。而70多年来世界航空科技研究才有了长足发展，但也正是这样的高速发展使一些发达国家逐渐在世界处于领先地位。而在目前世界上的几个主要航空大国中，美国已经拥有了多项技术专利和发明专利。\n飞机分类\n按用途分，有军用飞机、民用飞机和军用运输机。在民用飞机中，按动力系统的不同又可分为喷气客机、涡桨喷气客机及喷气式支线客机三大类，其中，喷气客机的主要特点是：机身短小、机动灵活、速度快而平稳；发动机耗油量低；在较短时间内能飞得较高。从用途分，可分为侦察型飞机、攻击型飞机和战略运输机。侦察型飞机是由侦察机改装而来的，一般用于攻击敌方地面或空中目标；攻击型战斗机是具有较强攻击力的战略战斗机，主要用于攻击敌方地面或空中目标；战略运输机是一种大型运输飞机，可以运送一定数量的人员和物资。\n飞机制造\n飞机制造是一项集科学、技术、艺术与工程于一体的高科技工业，它的研制必须有严格的质量管理体系来保证。飞机制造是指从产品设计、原材料采购、生产过程控制到成品装配检验等整个过程。其主要包括材料、工艺和结构三大类内容。材料是指各种飞机部件及其零件，如机身（结构）、机翼（机尾）、尾翼、起落架等；工艺是指制造零件及生产过程的工艺方法和手段；结构是指对飞机整体进行结构设计，根据其使用要求来布置各种设备和结构以及保证性能要求；结构必须能承受各种载荷，如机翼上重量（包括载荷所带来的机械应力）和其他载荷；它包括各种装配方法，装配质量也直接影响产品的可靠性和使用寿命。\n飞机发展现状\n飞机是由发动机的飞机，由于喷气发动机的推力大、效率高、噪音小；燃料多，燃料消耗少。飞机的外形和构造与汽车十分相似，可以在空中自由升降、滑行而不会受到地面阻力影响。因此是一个理想的交通工具。目前在全世界范围内，世界上主要用于军用的飞机有：F-16隐身战斗机（北约代号F35）、F-16猛禽战斗机（北约代号F35）、F-35联合攻击战斗机（KF-X）以及C-17 “大力神”运输机；民用领域的飞机有：客机（波音777/747等）、支线客机（空客A320等，波音737等）和特种飞机（如图2-1所示）。从各国的军用和民用航空史上看，世界上有相当一部分先进的军用装备，是在20世纪中期由军事大国发展起来的。\n",
    "wordCount" : "1194",
    "restCount" : "135608"
  }
}
```
### 4、单点登录签名算法
##### 调用示例
```python
import xiezuocat
my_xiezuocat = xiezuocat.Xiezuocat({your-secretKey})
sign_result = my_xiezuocat.get_sso_signature({your-appId}, {your-uid})
print(sign_result)
```
##### 返回结果
```json
eydhcHBJZCc6ICd4eCcsICd1aWQnOiAnbGwnLCAndGltZXN0YW1wJzogMTY4MDUxMTExNy42NjIyMTc2LCAnc2lnbic6ICdmZTM2MmU4MzBkMTFlZDc3ZDkwZjhhNzk0NzkwM2RlMDY1ODA2NjY2NDEzMjg4ZGJjNzFmMzk5MjhmODBlOTAxJ30=
```
##### 拿到签名之后访问下述URL即可登录写作猫
```js
// p为签名算法生成的结果
https://xiezuocat.com/api/open/login?p=eydhcHBJZCc6ICd4eCcsICd1aWQnOiAnbGwnLCAndGltZXN0YW1wJzogMTY4MDUxMTExNy42NjIyMTc2LCAnc2lnbic6ICdmZTM2MmU4MzBkMTFlZDc3ZDkwZjhhNzk0NzkwM2RlMDY1ODA2NjY2NDEzMjg4ZGJjNzFmMzk5MjhmODBlOTAxJ30=
```