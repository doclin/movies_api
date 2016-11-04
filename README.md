# movies_api
网络电影票购票平台综合信息接口(Movie Tickets Information API)  
可实时查询国内多家电影购票平台（现支持淘宝电影，猫眼（美团）电影，糯米电影）场次，票价等信息。   
文档地址：http://movies-api-docs.readthedocs.io/zh_CN/latest

## V0.2
* 基于Python Django
* 使用celery异步获取三家信息
* 按城市-影院-场次-票价分层查询
