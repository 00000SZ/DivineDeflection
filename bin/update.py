import subprocess
import requests
from requests.exceptions import HTTPError

feedurl = 'https://example.com/blacklist-domains.csv'
bindconf = '../conf/named.conf.blockeddomains'
certbundle = '../conf/CertBundle.pem'

try:
    print('Fetching new blacklist from '+feedurl)
    r = requests.get(feedurl,verify=certbundle)
    r.raise_for_status()
except HTTPError as http_err:
    print(http_err)
except Exception as err:
    print(err)
else:
    print('Success!')
    print(r.status_code)
    list = []
    lines = r.text.split(',')
    for l in lines:
        try:
            domain = str(l).strip()
            print('Found domain: '+domain)
            line = 'zone "'+domain+'" {type master; file "sinkhole.zone";};'
            list.append(line)
        except:
            pass
    print('Contructed list:')
    print(list)
    print('Opening BIND conf: '+bindconf)
    with open(bindconf, 'w') as f:
        for i in list:
            f.write("%s\n" % i)
    print('Wrote config.... Done!')
    print('Reloading zones')
    subprocess.call(['/usr/sbin/rndc','reload'])
