class Request(object):

    def __init__(self, req='LIST', headers={}, content=''):
        self.req = req
        self.headers = headers
        self.content = content

    def __str__(self):
        real_content = ''
        for key in self.headers:
            real_content += '%s:%s\r\n' % (key, str(self.headers[key]))
        real_content += '\r\n'
        real_content += self.content
        top_line = '%-10s%-10d\r\n' % (self.req, len(real_content))
        return top_line + real_content

    def toKivyLog(self, server_info):
        log_top = '[color=888888]Request -----> {}[/color]\n'.format(server_info)
        if self.req == 'LOGIN':
            color = '#66FF66'
        elif self.req == 'LIST':
            color = '#33FFFF'
        elif self.req == 'ADD':
            color = '#33FF99'
        elif self.req == 'UPDATE':
            color = '#FFFF66'
        elif self.req == 'MOVE':
            color = '#FF99FF'
        elif self.req == 'ARCHIVE':
            color = '#CC9999'
        else:
            color = '#FFFFFF'
        real_content = ''
        for key in self.headers:
            real_content += '%s:%s\r\n' % (key, str(self.headers[key]))
        real_content += '\r\n'
        real_content += self.content
        top_line = '%-10s%-10d\r\n' % (self.req, len(real_content))
        top_line = top_line.replace(self.req, '[b][color={}]{}[/color][/b]'.format(color, self.req))
        top_line = '[font=resource/SourceHanSans-Bold.otf]' + top_line + '[/font]'
        return log_top + top_line + real_content



if __name__ == '__main__':
    r = Request('LIST', {}, "dsadasdas")
    print(str(r))
