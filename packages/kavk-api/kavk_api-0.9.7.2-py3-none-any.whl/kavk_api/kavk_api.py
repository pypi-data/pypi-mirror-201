from typing import Callable
import aiohttp, asyncio_atexit
from .exceptions import VkError
from .types.methods import *

class Captcha:
    def __init__(self, captcha:dict) -> None:
        self.raw = captcha
        self.img = captcha['captcha_img']
        self.sid = captcha['captcha_sid']


class Vk:
    def __init__(self, token:str, captcha_handler:Callable[[Captcha], str]|None=None,
                version="5.131", _url:str="https://api.vk.com/method/") -> None:
        '''
        Класс для работы с API ВКонтакте

        ...
        token:str
            Токен ВК
        captcha_handler:Callable[[Captcha], str]
            Функция-обработчик капчи
        version:str
            Версия API VK
        _url:str
            URL для последующих запросов к API
        '''
        self.token = token
        self.captcha_handler = captcha_handler
        self.client = aiohttp.ClientSession(conn_timeout=60)
        self.URL = _url
        self.version = version
        self._params = {'access_token': self.token,
                        'v' : self.version}

        asyncio_atexit.register(self._on_exit)
        # Дальше скучно
        self.account = Account(self)
        self.ads = Ads(self)
        self.adsweb = Adsweb(self)
        self.apps = Apps(self)
        self.auth = Auth(self)
        self.board = Board(self)
        self.database = Database(self)
        self.docs = Docs(self)
        self.donut = Donut(self)
        self.fave = Fave(self)
        self.friends = Friends(self)
        self.gifts = Gifts(self)
        self.groups = Groups(self)
        self.likes = Likes(self)
        self.market = Market(self)
        self.messages = Messages(self)
        self.newsfeed = Newsfeed(self)
        self.notes = Notes(self)
        self.notifications = Notifications(self)
        self.orders = Orders(self)
        self.pages = Pages(self)
        self.photos = Photos(self)
        self.podcasts = Podcasts(self)
        self.polls = Polls(self)
        self.search = Search(self)
        self.secure = Secure(self)
        self.stats = Stats(self)
        self.status = Status(self)
        self.storage = Storage(self)
        self.store = Store(self)
        self.stories = Stories(self)
        self.streaming = Streaming(self)
        self.users = Users(self)
        self.utils = Utils(self)
        self.video = Video(self)
        self.wall = Wall(self)
        self.widgets = Widgets(self)
        # Скука закончилась!

    async def call_method(self, method:str, **params) -> dict:
        params.update(self._params)
        params = {k:v for k, v in params.items() if v is not None} #  убираем все с значением None
        async with self.client.get(self.URL+method, params=params) as r:
            r = await r.json()
            if self._check_for_error(r) > 0:
                code = self._check_for_error(r)
                if code == 14 and self.captcha_handler != None: # Код ошибки каптчи и проверка на существование хендлера
                    captcha = r['error']
                    captcha_key = self.captcha_handler(captcha)
                    try:
                        params.update({'captcha_sid': captcha.sid,
                                       'captcha_key': captcha_key})
                        r = await self.call_method(method, **params)
                        if self._check_for_error(r) > 0:
                            raise VkError(r['error'])
                    except: pass
                else:
                    error = r['error']
                    raise VkError(error)
            return r['response']

    def _check_for_error(self, r:dict) -> int:
        try: 
            code = r['error']['error_code']
        except: code = 0
        finally: return code

    async def _on_exit(self) -> None:
        await self.client.close()



__all__ = ("Vk", "Captcha")



