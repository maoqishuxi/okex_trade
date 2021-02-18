#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


logging.basicConfig(filename='example.log', format='%(asctime)s %(message)s', datefmt='%m %d %Y %I:%M:%S', level=logging.DEBUG)

logging.debug('This message should appear %s on the console' % 'fjdks')
logging.info('So should this')
logging.warning('And this, too')

