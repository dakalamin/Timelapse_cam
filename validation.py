import re
from configparser import ConfigParser


DEFAULT = re.compile(r'.*')
# SECTION            <section>
S   = r'\w*'
# SECTION-KEY        <section.key>          re.split('\.', line)
SK  = r'\w*(\.\w*)?'
# SECTION-KEY-VALUE  <section.key=value>    re.split('\.|\=', line)
SKV = r'\w*\.\w*=\w*'
# HH HH: HH:MM HH:MM: HH:MM:SS HH:: HH::SS  re.split('\-|\+', line)
#  _   :   :MM   :MM:   :MM:SS   ::   ::SS
#
# lets say [HH][:[MM][:[SS]]] = (T[n])
# {T} +(T) -(T) {T1}+{T2} (T1)-(T2) {T1}+{T2}-{T3}+...
#
# regex template without -+ operators
# r'([01][0-9]|2[0-3])?(:([0-5][0-9])?){0,2}'
h, m = '([01][0-9]|2[0-3])', '(:([0-5][0-9])?)'
TIME = re.compile(f'{h}?{m}{{0,2}}([-+]({h}{m}{{0,2}}|{m}{{1,2}}))*')
# FPd FPh FPm FPs FPi TBFh TBFm TBFs
UNIT = re.compile('FP[dhmsi]|TBF[hms]')
# any string missing ---vv-v-v-vvvvv--- symbols
PATH   = re.compile(r'[^:"\|\/\\*?<>]*')
TUPLE  = re.compile(r'[\d ]*')           #  re.split('.', line)
NUMBER = re.compile(r'\d*')
BOOL   = re.compile('|'.join(ConfigParser.BOOLEAN_STATES | {'y':True,'n':False}),
                    flags=re.IGNORECASE)

def get(pattern, line):
    return bool(re.fullmatch(pattern, line))
