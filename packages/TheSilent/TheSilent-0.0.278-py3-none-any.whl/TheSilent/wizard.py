import TheSilent.TheSilent as ts

import argparse

og_parser = argparse.ArgumentParser(prog = "TheSilent")

#tools
og_parser.add_argument("--link_scanner", dest = "link_scanner", required = False, help = "[tool]: crawl urls")

#parameters
og_parser.add_argument("--crawl", dest = "crawl", required = False, help = "[parameter]: Crawl 'all' like google or crawl 'x' links. Defaults to all.")
og_parser.add_argument("--delay", dest = "delay", required = False, help = "[parameter]: Delay (in seconds). Defaults to 1.")
og_parser.add_argument("--my_file", dest = "my_file", required = False, help = "[parameter]: Outputs urls to text file. Example: links.txt. defaults to none.")
og_parser.add_argument("--parse", dest = "parse", required = False, help = "[parameter]: Parse url for specific string. Example: .onion, .com, .org, etc. Defaults to none.")
og_parser.add_argument("--secure", dest = "secure", required = False, help = "[parameter]: https:// = True, http:// = False. Defaults to True")
og_parser.add_argument("--title", dest = "title", required = False, help = "[parameter]: Get the title of the website. Defaults to False.")
og_parser.add_argument("--tor", dest = "tor", required = False, help = "[parameter]: Send get requests over tor. Defaults to False.")
og_parser.add_argument("--url", dest = "url", required = False, help = "[parameter]: The url. Example: example.com. Defaults to none.")

args = og_parser.parse_args()

if args.link_scanner == "True":
    if args.crawl == None:
        crawl = "all"
        
    elif args.crawl == "all":
        crawl = "all"
        
    else:
    	crawl = int(args.crawl)

    if args.delay == None:
        delay = 1
        
    elif args.delay != None:
        depth = args.delay

    if args.my_file == None:
        my_file = " "

    else:
        my_file = str(args.my_file)

    if args.parse == None:
        parse = " "

    else:
        parse = str(args.parse)

    if args.secure == None:
        secure = True

    else:
        secure = bool(args.secure)

    if args.title == None:
        title = False

    else:
        title = bool(args.title)

    if args.tor == None:
        tor = False

    else:
        tor = bool(args.tor)

    if args.url == None:
        print("ERROR! URL required! Use --url=example.com")

    if args.url != None:
        result = ts.link_scanner(str(args.url), secure = secure, tor = tor, my_file = my_file, crawl = crawl, parse = parse, title = title)

        ts.clear()
        for i in result:
            print(i)
