# nicodown
获取nicovideo(n站)视频的真实下载地址<br>
## 原理
1.抓包发现n站的视频地址会以两种形式出现，一种是hls，一种是传统的http，hls是切片之后视频地址，很多的ts链接，而http就跟我们普通的那种下载地址一样。<br>
2.获取n站的视频地址需要往 https://api.dmc.nico/api/sessions?_format=json post获取视频地址需要的json参数，也就是视频页面的dmcinfo，格式为: https://gist.github.com/Aruelius/6c9bf38737dffbf823f7d1350ded8065 <br>
3.之后得到返回的json，里面就有真实的视频地址。<br>
4.需要注意的是，n站对会员提供了非常nb的下载服务器，但是，如果把会员帐号获取到的真实地址单线程下载的话，速度依旧很慢，需要多线程才能达到你带宽的满速，实测多线程能跑到400Mbps，单线程1-2MB/s(注意单位)。如果你在n站没开会员，那么获取到的地址不管你用单线程还是多线程，速度都一样，没差。<br>
5.默认获取的视频地址为最高分辨率视频地址，会员如此，非会员会在不同的时间段获取到不同清晰度的视频地址。<br>
6.如果要直接用下载可以使用我修改的[nndownload](https://github.com/Aruelius/nndownload)
## 运行
``` sh
#修改nicodown.py里的username跟passwd，这两个是n站的帐号密码。<br>
python nicodown.py <视频URL>
例如：python nicodown.py https://www.nicovideo.com/watch/sm123456
``` 
返回如下：
```html
https://pa02639ea10.dmc.nico/vod/ht2_nicovideo/nicovideo-sm123456_e492691c176811d3ad1135f3c5b3a4f2870489df5ad6082b08243db8719cf046?ht2_nicovideo=.8uo9ye_poyuev_lg5tl2uls8ra
```
