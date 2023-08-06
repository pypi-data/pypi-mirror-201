#!/usr/bin/env python3
import pprint
from flask_babelex import gettext as _
import pathlib
from hiddifypanel.models import  *

from datetime import datetime,timedelta,date
import os,sys
import json
import urllib.request
import subprocess
import re
from hiddifypanel.panel import hiddify,usage
from hiddifypanel.panel import hiddify_api
from flask import current_app,render_template,request,Response,Markup,url_for
from hiddifypanel.panel.hiddify import flash

from flask_classful import FlaskView,route

class CommercialInfo(FlaskView):

    def index(self):
        return render_template('commercial_info.html')
#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
