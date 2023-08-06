import traceback
from telegram import Bot

class telegram:
    def __init__(self, token=None, channel=None, logger=None, full_error=False, raise_error=False, resend_repeat_errors=True):
        if token:
            self.bot = Bot(token=token)
        self.channel = channel
        self.logger = logger
        self.full_error = full_error
        self.raise_error = raise_error
        self.resend_repeat_errors = resend_repeat_errors
        self.last_error = None
    def send(self, title='Error', exception=None):
        if self.full_error:
            error = traceback.format_exc()
        else:
            error = str(exception)
        message = f'{title}: {error}'
        if error == self.last_error and not self.resend_repeat_errors:
            self.printer(message, level='error')
        if error != self.last_error or self.resend_repeat_errors:
            self.printer(message, level='error')
            if self.channel:
                try:
                    self.bot.send_message(self.channel, message[:4096])
                except Exception as telegram_error:
                    self.printer('Error sending alert message to Telegram:', telegram_error, level='error')
            self.last_error = error
        if self.raise_error:
            raise Exception('Raiser') from exception
    def send_message(self, *messages, print_message=True, current_time=True):
        final_message = ''
        for message in messages:
            final_message += message
            final_message += ' '
        if print_message:
            self.printer(final_message, current_time=current_time)
        if self.channel:
            try:
                self.bot.send_message(self.channel, final_message[:4096])
            except Exception as telegram_error:
                self.printer('Error sending message to Telegram:', telegram_error, level='error')
    
    def printer(self, *items, level='info', current_time=True):
        if self.logger:
            if current_time:
                self.logger.current_time(*items, level=level)
            else:
                self.logger.log(*items, level=level)
            self.logger.log(level=level)
        elif level != 'debug': # Don't print debug only messages
            print(*items)
            print()