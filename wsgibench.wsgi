#!/usr/bin/python

import time
import random
import sys

tests = ('cpubound', 'bigresponse', 'bigfile', 'slow', 'wedge', 'segfault',
         'leakmemory', 'largeupload', 'slowupload', 'slowdownload')

def application(environ, start_response):
    path = environ['PATH_INFO']
    if (path.find('random') >= 0) and (random.randint(1,100) == 1):
        path = '/wedge'

    status = '200 OK'
    output = 'Didn\'t match any existing test: ' + path

    if path.startswith('/cpubound'):
        output = 'cpu bound test executed'
        for i in xrange(10000000): 
            pass

    if path.startswith('/bigresponse'):
        output = 'bigresponse test executed ' + "x"*100000

    if path.startswith('/bigfile'):
        output = 'bigfile test executed ' + "x"*100000

    if path.startswith('/slow'):
        output = 'slow test executed'
        time.sleep(1)

    if path.startswith('/wedge'):
        output = 'wedge executed'
        while 1:
            pass

    if path.startswith('/segfault'):
        output = 'segfault executed'

    if path.startswith('/leakmemory'):
        output = 'leak memory executed'

    if path.startswith('/largeupload'):
        output = 'large upload executed'

    if path.startswith('/slowupload'):
        output = 'slow upload executed'

    if path.startswith('/slowdownload'):
        output = 'slow download executed'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

if __name__ == '__main__' :
    if (len(sys.argv) < 2) or (len(sys.argv) > 3):
        print """
http://code.google.com/p/wsgi-bench/

Argv1 = url to prepend to the tests
Argv2 = random  (add random to the urls)

Usage:
              """
        print sys.argv[0] + ' http://mysite.com/'
        print 'or'
        print sys.argv[0] + ' http://mysite.com/ random'

    else:

        random = ''
        if len(sys.argv) == 3:
             random = '/random'

        for test in tests:
            print sys.argv[1] + test + random
