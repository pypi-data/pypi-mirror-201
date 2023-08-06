from TheSilent.clear import *
from TheSilent.subdomain_takeover import *
from TheSilent.sql_injection_scanner import *
from TheSilent.xss_scanner import *

cyan = "\033[1;36m"

#scans for all security flaws    
def security_scanner(url, secure = True, tor = False, depth = 1, my_file = " ", crawl = "0", parse = " ", delay = 1):
    clear()
    
    my_sql_injection_scanner = sql_injection_scanner(url = url, secure = secure, tor = tor, crawl = crawl, parse = parse, delay = delay)
    my_xss_scanner = xss_scanner(url = url, secure = secure, tor = tor, crawl = crawl, parse = parse, delay = delay)

    clear()
    
    print(cyan + "sql injection:")

    for i in my_sql_injection_scanner:
        print(cyan + i)

    print("")
    print(cyan + "xss:")

    for i in my_xss_scanner:
        print(cyan + i)
