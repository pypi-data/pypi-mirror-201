# coding:utf-8
import argparse
from io import StringIO
import os
import sys
from collections import deque
from urllib.parse import urlparse


class shlex2:
    "A lexical analyzer class for simple shell-like syntaxes."
    "为了兼容python3.9移除的功能"
    def __init__(self, instream=None, infile=None, posix=False,
                 punctuation_chars=False):
        if isinstance(instream, str):
            instream = StringIO(instream)
        if instream is not None:
            self.instream = instream
            self.infile = infile
        else:
            self.instream = sys.stdin
            self.infile = None
        self.posix = posix
        if posix:
            self.eof = None
        else:
            self.eof = ''
        self.commenters = '#'
        self.wordchars = ('abcdfeghijklmnopqrstuvwxyz'
                          'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        if self.posix:
            self.wordchars += ('ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
                               'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ')
        self.whitespace = ' \t\r\n'
        self.whitespace_split = False
        self.quotes = '\'"'
        self.escape = '\\'
        self.escapedquotes = '"'
        self.state = ' '
        self.pushback = deque()
        self.lineno = 1
        self.debug = 0
        self.token = ''
        self.filestack = deque()
        self.source = None
        if not punctuation_chars:
            punctuation_chars = ''
        elif punctuation_chars is True:
            punctuation_chars = '();<>|&'
        self._punctuation_chars = punctuation_chars
        if punctuation_chars:
            # _pushback_chars is a push back queue used by lookahead logic
            self._pushback_chars = deque()
            # these chars added because allowed in file names, args, wildcards
            self.wordchars += '~-./*?='
            #remove any punctuation chars from wordchars
            t = self.wordchars.maketrans(dict.fromkeys(punctuation_chars))
            self.wordchars = self.wordchars.translate(t)

    @property
    def punctuation_chars(self):
        return self._punctuation_chars

    def push_token(self, tok):
        "Push a token onto the stack popped by the get_token method"
        if self.debug >= 1:
            print("shlex: pushing token " + repr(tok))
        self.pushback.appendleft(tok)

    def push_source(self, newstream, newfile=None):
        "Push an input source onto the lexer's input source stack."
        if isinstance(newstream, str):
            newstream = StringIO(newstream)
        self.filestack.appendleft((self.infile, self.instream, self.lineno))
        self.infile = newfile
        self.instream = newstream
        self.lineno = 1
        if self.debug:
            if newfile is not None:
                print('shlex: pushing to file %s' % (self.infile,))
            else:
                print('shlex: pushing to stream %s' % (self.instream,))

    def pop_source(self):
        "Pop the input source stack."
        self.instream.close()
        (self.infile, self.instream, self.lineno) = self.filestack.popleft()
        if self.debug:
            print('shlex: popping to %s, line %d' \
                  % (self.instream, self.lineno))
        self.state = ' '

    def get_token(self):
        "Get a token from the input stream (or from stack if it's nonempty)"
        if self.pushback:
            tok = self.pushback.popleft()
            if self.debug >= 1:
                print("shlex: popping token " + repr(tok))
            return tok
        # No pushback.  Get a token.
        raw = self.read_token()
        # Handle inclusions
        if self.source is not None:
            while raw == self.source:
                spec = self.sourcehook(self.read_token())
                if spec:
                    (newfile, newstream) = spec
                    self.push_source(newstream, newfile)
                raw = self.get_token()
        # Maybe we got EOF instead?
        while raw == self.eof:
            if not self.filestack:
                return self.eof
            else:
                self.pop_source()
                raw = self.get_token()
        # Neither inclusion nor EOF
        if self.debug >= 1:
            if raw != self.eof:
                print("shlex: token=" + repr(raw))
            else:
                print("shlex: token=EOF")
        return raw

    def read_token(self):
        quoted = False
        escapedstate = ' '
        while True:
            if self.punctuation_chars and self._pushback_chars:
                nextchar = self._pushback_chars.pop()
            else:
                nextchar = self.instream.read(1)
            if nextchar == '\n':
                self.lineno += 1
            if self.debug >= 3:
                print("shlex: in state %r I see character: %r" % (self.state,
                                                                  nextchar))
            if self.state is None:
                self.token = ''        # past end of file
                break
            elif self.state == ' ':
                if not nextchar:
                    self.state = None  # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print("shlex: I see whitespace in whitespace state")
                    if self.token or (self.posix and quoted):
                        break   # emit current token
                    else:
                        continue
                elif nextchar in self.commenters:
                    self.instream.readline()
                    self.lineno += 1
                elif self.posix and nextchar in self.escape:
                    escapedstate = 'a'
                    self.state = nextchar
                elif nextchar in self.wordchars:
                    self.token = nextchar
                    self.state = 'a'
                elif nextchar in self.punctuation_chars:
                    self.token = nextchar
                    self.state = 'c'
                elif nextchar in self.quotes:
                    if not self.posix:
                        self.token = nextchar
                    self.state = nextchar
                elif self.whitespace_split:
                    self.token = nextchar
                    self.state = 'a'
                else:
                    self.token = nextchar
                    if self.token or (self.posix and quoted):
                        break   # emit current token
                    else:
                        continue
            elif self.state in self.quotes:
                quoted = True
                if not nextchar:      # end of file
                    if self.debug >= 2:
                        print("shlex: I see EOF in quotes state")
                    # XXX what error should be raised here?
                    raise ValueError("No closing quotation")
                if nextchar == self.state:
                    if not self.posix:
                        self.token += nextchar
                        self.state = ' '
                        break
                    else:
                        self.state = 'a'
                elif (self.posix and nextchar in self.escape and self.state
                      in self.escapedquotes):
                    escapedstate = self.state
                    self.state = nextchar
                else:
                    self.token += nextchar
            elif self.state in self.escape:
                if not nextchar:      # end of file
                    if self.debug >= 2:
                        print("shlex: I see EOF in escape state")
                    # XXX what error should be raised here?
                    raise ValueError("No escaped character")
                # In posix shells, only the quote itself or the escape
                # character may be escaped within quotes.
                if (escapedstate in self.quotes and
                        nextchar != self.state and nextchar != escapedstate):
                    self.token += self.state
                self.token += nextchar
                self.state = escapedstate
            elif self.state in ('a', 'c'):
                if not nextchar:
                    self.state = None   # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print("shlex: I see whitespace in word state")
                    self.state = ' '
                    if self.token or (self.posix and quoted):
                        break   # emit current token
                    else:
                        continue
                elif nextchar in self.commenters:
                    self.instream.readline()
                    self.lineno += 1
                    if self.posix:
                        self.state = ' '
                        if self.token or (self.posix and quoted):
                            break   # emit current token
                        else:
                            continue
                elif self.state == 'c':
                    if nextchar in self.punctuation_chars:
                        self.token += nextchar
                    else:
                        if nextchar not in self.whitespace:
                            self._pushback_chars.append(nextchar)
                        self.state = ' '
                        break
                elif self.posix and nextchar in self.quotes:
                    self.state = nextchar
                elif self.posix and nextchar in self.escape:
                    escapedstate = 'a'
                    self.state = nextchar
                elif (nextchar in self.wordchars or nextchar in self.quotes
                      or self.whitespace_split):
                    self.token += nextchar
                else:
                    if self.punctuation_chars:
                        self._pushback_chars.append(nextchar)
                    else:
                        self.pushback.appendleft(nextchar)
                    if self.debug >= 2:
                        print("shlex: I see punctuation in word state")
                    self.state = ' '
                    if self.token or (self.posix and quoted):
                        break   # emit current token
                    else:
                        continue
        result = self.token
        self.token = ''
        if self.posix and not quoted and result == '':
            result = None
        if self.debug > 1:
            if result:
                print("shlex: raw token=" + repr(result))
            else:
                print("shlex: raw token=EOF")
        return result

    def sourcehook(self, newfile):
        "Hook called on a filename to be sourced."
        if newfile[0] == '"':
            newfile = newfile[1:-1]
        if isinstance(self.infile, str) and not os.path.isabs(newfile):
            newfile = os.path.join(os.path.dirname(self.infile), newfile)
        return (newfile, open(newfile, "r"))

    def error_leader(self, infile=None, lineno=None):
        "Emit a C-compiler-like, Emacs-friendly error-message leader."
        if infile is None:
            infile = self.infile
        if lineno is None:
            lineno = self.lineno
        return "\"%s\", line %d: " % (infile, lineno)

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_token()
        if token == self.eof:
            raise StopIteration
        return token

def split2(s, comments=False, posix=True):
    """Split the string *s* using shell-like syntax."""
    lex = shlex2(s, posix=posix)
    lex.whitespace_split = True
    if not comments:
        lex.commenters = ''
    return list(lex)

class CurlParser(argparse.ArgumentParser):
    def error(self, message):
        error_msg = \
            'There was an error parsing the curl command: {}'.format(message)
        raise ValueError(error_msg)

# 自定义解析的内容
curl_parser = CurlParser()
curl_parser.add_argument('url')
curl_parser.add_argument('-H', '--header', dest='headers', action='append')
curl_parser.add_argument('-X', '--request', dest='method', default='get')
curl_parser.add_argument('-d', '--data-raw','--data-binary', dest='data')
curl_parser.add_argument('-u', '--user', dest='auth')
curl_parser.add_argument('-A', '--user-agent', dest='UA')
curl_parser.add_argument('-b', '--cookie', dest='cookie')





safe_to_ignore_arguments = [
    ['--compressed'],
    # `--compressed` argument is not safe to ignore, but it's included here
    # because the `HttpCompressionMiddleware` is enabled by default
    ['-s', '--silent'],
    ['-v', '--verbose'],
    ['-#', '--progress-bar'],
    ['-f','--fail']
]
for argument in safe_to_ignore_arguments:
    curl_parser.add_argument(*argument, action='store_true')


def curl_to_request_kwargs(curl_command):
    """Convert a cURL command syntax to Request kwargs.
    :param str curl_command: string containing the curl command
    :return: dictionary of Request kwargs
    """
    curl_args = split2(curl_command)
    # print(curl_args)

    if curl_args[0] != 'curl':
        raise ValueError('A curl command must start with "curl"')
    parsed_args, argv = curl_parser.parse_known_args(curl_args[1:])
    if argv:
        msg = 'Unrecognized options: {}'.format(', '.join(argv))

        raise ValueError(msg)
    url = parsed_args.url
    # curl automatically prepends 'http' if the scheme is missing, but Request
    # needs the scheme to work
    parsed_url = urlparse(url)
    # print(parsed_url, "parsed_url---")
    if not parsed_url.scheme:
        url = 'https://' + url
    result = {'method': parsed_args.method.upper(), 'url': url}
    headers = {}

    for header in parsed_args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        if name in headers:
            headers[name]+=";"+val
        else:
            headers[name]=val
    if parsed_args.UA:
        val=str(parsed_args.UA)
        if 'User-Agent' in headers :
            headers['User-Agent']+=";"+val
        elif 'user-agent' in headers:
            headers['User-Agent']=headers['user-agent']+";"+val
            del headers['user-agent']
        else:
            headers['User-Agent']=val
    if parsed_args.cookie:
        val=str(parsed_args.cookie)
        if 'Cookie' in headers :
            headers['Cookie']+=";"+val
        elif 'cookie' in headers:
            headers['Cookie']=headers['cookie']+";"+val
            del headers['cookie']
        else:
            headers['Cookie']=val
    if parsed_args.auth:
        user, password = parsed_args.auth.split(':', 1)
        result['auth']=(user, password)
    if headers:
        result['headers'] = headers
    if parsed_args.data:
        result['data'] = parsed_args.data.encode('utf-8')
    return result

# curl_command = """
# curl 'https://preopen.yuewen.com/api/component/setDefaultPriceAndChapter' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: zh-CN,zh;q=0.9' \
#   -H 'Connection: keep-alive' \
#   -H 'Content-Type: application/json;charset=UTF-8' \
#   -H 'Cookie: csrfToken=-bC6cAn81mBLi9NCoUyJdoBE; Today_show_bind_statuslixuecheng%40yuewen.com=true; OPENSESSID=dd16c322c07d367910abd22060a606f3; yw_open_token=62e793c06c3ad; is_read_notice=62e793c06c3ad; HRIS_USER=00ca531016abf81379d5634cfc3408f6eff6b24289166dffc2ca8dd51cc8bbb4d0c2007cc4c966abd4c0b6a2637891ec561b8b668751ea5a263b877e19205e5d1126e895dcfd7c1727d223e9822c02806f9ee8f568ac619046920cc0b17c9c00e0307c214841d15a1502a83ab2db1e167cefeeb3e3a7cd1c441102eeb4377413e6cbc5781271b3552a36909109c972d55d2f59b086fa6e67650441452cea8b70e81eef460c6e33377a85bc959844a06da90f6a45d23169c29e0b3a43cf797097fa95135c7728c4debcf3f13aafd1c4ef3f96fe860b120a8a73bfb89493d74a5854262fa1395769202846cb0110ded5b29bf4b70e4db4111a1a5ce0f8bbc6628d9411f3bf8fef2e7076c695f8d9f98bd87a305083cdb58e2ba2e47933c9208687ba4c6f6459219e976bcb4a9e9c010eb2ecba8ab1518e7b3514e96aa542390fc5f7aafe8fb5e25f5bd5af422235bbf3f20a03725f906cae976e23366444f41eb5e0fa88479e9f4fcf46b9ec9297af30aa237e25ddeaa0e91d0e35d9c3978fa8051816c5308746109bdb000786a0fb5e7a7843f9b4890a2bfc81b34812a4c96478' \
#   -H 'Origin: https://preopen.yuewen.com' \
#   -H 'Referer: https://preopen.yuewen.com/new/videoLibrary' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' \
#   -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   --data-raw '{"chapterChargeType":4,"price":1.2,"forceCover":0,"copy":0,"copyList":[]}' \
#   --compressed
#                """
# result = curl_to_request_kwargs(curl_command)
# print(result)