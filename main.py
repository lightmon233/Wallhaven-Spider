import requests
import parsel

for page in range(1, 10):
    # url是网页的地址，这里是wallhaven的搜索结果页，搜索关键词是angel beats
    url = "https://wallhaven.cc/search?q=angel%20beats&page=" + str(page)
    # 发送请求
    response = requests.get(url=url)
    # 获取网页源代码
    data_html = response.text
    # 使用parsel解析网页源代码
    selector = parsel.Selector(data_html)
    # 获取图片的url
    a_href_list = selector.css('#thumbs > section > ul > li > figure > a::attr(href)').getall()

    # 遍历图片的url, 下载图片
    for a_href in a_href_list:
        res = requests.get(url=a_href)
        data = res.text
        selector = parsel.Selector(data)
        img_url = selector.css('#wallpaper::attr(src)').get()
        img_name = 'wallhaven-' + selector.css('#wallpaper::attr(data-wallpaper-id)').get()
        # 下载图片, 保存到脚本同级目录下的img文件夹中
        with open(f'img/{img_name}.jpg', mode='wb') as f:
            img_data = requests.get(url=img_url).content
            f.write(img_data)
        print(f'{img_name}下载完成')

    print("第" + str(page) + "页下载完成")
