from ..exceptions import NotificationError
from ..utils import log, request


class BaseNotifier(object):
    app = 'Genshin Impact Helper'
    status = ': Test'
    desp = 'ð Send from genshin-impact-helper project.'

    def __init__(self):
        self.name = None
        self.token = None
        self.retcode_key = None
        self.retcode_value = None

    def send(self):
        ...

    def push(self,
             method,
             url,
             params=None,
             data=None,
             json=None,
             headers=None):
        """
        ð«: disabled
        ð¥³: success
        ð³: failure
        """
        if not self.token:
            # log.info(f'{self.name} ð«')
            return
        try:
            response = request(method, url, 2, params, data, json, headers).json()
        except Exception as e:
            raise NotificationError(f'{self.name} ð³\n{e}')
        else:
            retcode = response.get('data', {}).get(
                self.retcode_key,
                -1) if self.name == 'Server Chan Turbo' else response.get(
                self.retcode_key, -1)
            if retcode == self.retcode_value:
                log.info(f'{self.name} ð¥³')

            # Telegram Bot
            elif self.name == 'Telegram Bot' and retcode:
                log.info(f'{self.name} ð¥³')
            elif self.name == 'Telegram Bot' and response[self.retcode_value] == 400:
                raise NotificationError(f'{self.name} ð³\nè¯·ä¸»å¨ç» bot åéä¸æ¡æ¶æ¯å¹¶æ£æ¥ TG_USER_ID æ¯å¦æ­£ç¡®')
            elif self.name == 'Telegram Bot' and response[self.retcode_value] == 401:
                raise NotificationError(f'{self.name} ð³\nTG_BOT_TOKEN éè¯¯')
            else:
                raise NotificationError(f'{self.name} ð³\n{response}')
