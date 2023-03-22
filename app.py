
import streamlit as st
import scrapy
import re

class VideoSpider(scrapy.Spider):
    name = 'video-spider'
    start_urls = ['https://example.com/videos']

    def parse(self, response):
        dicionario = {}
        videos = response.xpath('//div[@class="video"]')
        for video in videos:
            title = video.xpath('.//h3/text()').get()
            script = video.xpath('.//script/text()').get()
            mp4_link = re.search(r"file: '(.*?)'", script).group(1)
            poster = re.search(r"poster: '(.*?)'", script).group(1)
            if title not in dicionario:
                dicionario[title] = (mp4_link, poster)

        def escrever_playlist(dicionario):
            with open('videos.m3u8', 'w') as f:
                for titulo, dados in dicionario.items():
                    f.write(f'#EXTINF:0,{titulo}\n')
                    f.write(f'#EXTVLCOPT:network-caching=1000\n')
                    f.write(f'{dados[0]}\n')
                    f.write(f'#EXT-X-IMAGE-URI:{dados[1]}\n')

        escrever_playlist(dicionario)

        next_page = response.xpath('//a[@rel="next"]/@href')
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

st.title('Gerador de Playlist de Vídeos')

if st.button('Iniciar'):
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(VideoSpider)
    process.start()

    st.success('Playlist gerada com sucesso!')

    with open('videos.m3u8', 'r') as f:
        playlist = f.read()
    
    st.code(playlist)
```
