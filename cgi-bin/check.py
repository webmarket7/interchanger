#!/home/u/uebersth/.local/bin/python3.4
# -*- coding: utf-8 -*-

import cgi, json
from interchange_checker import check 

def main():
    myStr = 'Кіт та собака - два забіяки. Бігали, каталися, дуже матюкалися.' 
    print(myStr)
    checked = check(myStr)
    encoded = json.dumps(checked, ensure_ascii=False)
    print(encoded)
    
if __name__ == '__main__':
    main()
