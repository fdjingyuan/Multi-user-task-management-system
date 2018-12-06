class Response(object):

    def __init__(self, code=200, res='OK', headers={}, content=''):
        self.code = code
        self.headers = headers
        self.content = content
        self.res = res

    def __str__(self):
        if not(self.code >= 400 and self.code < 500):
            real_content = ''
            for key in self.headers:
                real_content += '%s:%s\r\n' % (key, str(self.headers[key]))
            real_content += '\r\n'
            real_content += self.content
            top_line = '%3s %-10s%-10d\r\n' % (self.code, self.res, len(real_content))
            return top_line + real_content
        else:
            return str(self.code) + ' ' + self.headers['Info']

    def toKivyLog(self, server_info):
        if not(self.code >= 400 and self.code < 500):
            log_top = '[color=888888]Respond <----- {} [/color]\n'.format(server_info)
            if self.res == 'OK':
                color = '#66FF66'
            elif self.res == 'ERROR':
                color = '#FF0033'
            else:
                color = '#FFFFFF'
            real_content = ''
            for key in self.headers:
                real_content += '%s:%s\r\n' % (key, str(self.headers[key]))
            real_content += '\r\n'
            real_content += self.content
            top_line = '%3s %-10s%-10d\r\n' % (self.code, self.res, len(real_content))
            top_line = top_line.replace(
                '%3s %-10s' % (self.code, self.res),
                '[b][color=%s]%3s %-10s[/color][/b]' % (color, self.code, self.res))
            top_line = '[font=resource/SourceHanSans-Bold.otf]' + top_line + '[/font]'
            return log_top + top_line + real_content
        else:
            return str(self.code) + ' ' + self.headers['Info']

if __name__ == '__main__':
    r = Response(400, 'ERROR', {}, "dsadasdas")
    print(str(r))
