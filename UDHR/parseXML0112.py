# -*- coding: utf-8 -*-
from lxml import etree
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

def parse_doc_tree_for_text(root):
    r_no_empty_tags=[]
    r_no_empty_content=[]
    import string
    #http://stackoverflow.com/questions/10798680/finding-text-into-namespaced-xml-elements-with-lxml-etree
    #results=root.xpath('//*/n:para', namespaces={'n': 'http://www.unhchr.ch/udhr'})
    ns={'n': 'http://www.unhchr.ch/udhr'}
    results=root.xpath('//*[text()]', namespaces=ns)

    r_non_empty=[]
    for element in results:
        if isinstance(element.tag, str):
            #stripping leading and ending spaces, including /n
            content=element.text 
            content=content.strip()
            content_tag=element.tag.replace('{'+ns['n']+'}', '')
            #if content <>'':
            if content =='':
                pass
                #print "Warning:%s - %s\t" % (content_tag, element.text),
            else:
                r_non_empty.append({content_tag:element.text})
        else:
            print("SPECIAL: %s - %s" % (element, element.text))

    ##TEST/DEBUG:Iterate every nodes under root
    ##for element in root.iter():
    ##    if isinstance(element.tag, basestring):
    ##        print("%s - %s" % (element.tag, element.text))
    ##    else:
    ##        print("SPECIAL: %s - %s" % (element, element.text))
    print ("No of elements in results:{}".format( len(results) ))
    print ("No of elements with non-empty text in results:{}".format( len(r_non_empty) ))
    print (len(r_non_empty))
    r_no_empty_tags=[list(x.keys())[0] for x in r_non_empty]
    r_no_empty_content=[list(x.values())[0] for x in r_non_empty]
    print ("The set of tags that contain text:{}".format( set(r_no_empty_tags) ))
    for i in set(r_no_empty_tags):
        print ("\t{}:".format( r_no_empty_tags.count(i) ))

    r=doc_tree.xpath("//*/n:para", namespaces={'n': 'http://www.unhchr.ch/udhr'})
    print ("""Double check with xpath "//*/n:para": {}""".format(len(r)))

    return r_no_empty_tags, r_no_empty_content


## MAIN
parser = etree.XMLParser(encoding='utf-8')
lang_codes =["mya", "njo", "ctd", "hlt", "cnh", "flm", "lus", "jpn","eng","cmn_hant","cmn_hans"]
#udhr f="flm" iso639-3="cfm" bcp47="cfm"

import pandas as pd
df_all=pd.DataFrame()

for lang_code in lang_codes:
    logger.info('Processing texts with language code {}'.format(lang_code))
    filename = '''..\\XML\\udhr_{}.xml'''.format(lang_code)
    doc_tree = etree.parse(filename, parser).getroot()
    #doc_tree = etree.parse(filename)
    r_tags, r_content=[],[]
    r_tags, r_content = parse_doc_tree_for_text(doc_tree)
    df=pd.DataFrame()
    df['tag']=r_tags
    df['content']=r_content
    df['sn']=range(1,len(df)+1)
    df['lang']=lang_code
    df['length']=[len(x) for x in r_content]
    df['length_encoded_utf8']=[len(x.encode('utf-8')) for x in r_content]

    
    if len(df_all)==0:
        df_all=df.copy()
    else:
        df_all=df_all.append(df)

print (len(df_all))
df_all.to_csv("r_UDHR.csv", encoding='utf-8')

## Constructing pivot tables for further analysis
pivot_para = df_all[df_all["tag"]=="para" ].pivot(index='sn', columns='lang', values='length')
pivot_title= df_all[df_all["tag"]=="title"].pivot(index='sn', columns='lang', values='length')

### Caculate ration based on cmn_hant
def calculate_ratio(df, base):
    df=df.astype(float)
    #base='cmn_hant'
    for lang in df.columns.values:
        if not (lang==base):
            df[lang]=df[lang]/df[base]
    lang=base
    df[lang]=df[lang]/df[base]
    return df

r_pivot_para =calculate_ratio(pivot_para,  base='cmn_hant')
r_pivot_title=calculate_ratio(pivot_title, base='cmn_hant')

r_pivot_para.to_pickle("r_UDHR_para.pkl")
r_pivot_title.to_pickle("r_UDHR_title.pkl")

r_pivot_para.to_csv("r_UDHR_para.csv")
r_pivot_title.to_csv("r_UDHR_title.csv")
