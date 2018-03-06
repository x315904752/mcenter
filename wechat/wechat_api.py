import urllib.request,json,urllib





def GetUrl(CropID,Secret):
    GURL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (CropID, Secret)
    result = urllib.request.urlopen(urllib.request.Request(GURL)).read()
    dict_result = json.loads(result)
    Gtoken = dict_result['access_token']
    PURL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" %Gtoken
    return PURL


def SendTextcard(title,description,PURL,url,touser):
    PostData = {}
    MsgContent = {}
    MsgContent['title'] = title
    MsgContent['description'] = description
    MsgContent['url'] = url
    PostData['touser'] = touser
    PostData['msgtype'] = 'textcard'
    PostData['agentid'] = 1000007
    PostData['textcard'] = MsgContent
    Jsonpostdata = json.dumps(PostData, ensure_ascii=False).encode(encoding='UTF8')
    res = urllib.request.Request(PURL, Jsonpostdata)
    response = urllib.request.urlopen(res)
    msg = response.read()
    print("returned value : " + str(msg))

