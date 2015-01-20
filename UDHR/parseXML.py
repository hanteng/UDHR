# -*- coding: utf-8 -*-
from lxml import etree
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
        if isinstance(element.tag, basestring):
            #stripping leading and ending spaces, including /n
            content=element.text 
            content=content.strip()
            content_tag=string.replace(element.tag, '{'+ns['n']+'}', '')
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
    print "No of elements in results:", len(results)
    print "No of elements with non-empty text in results:", len(r_non_empty)
    r_no_empty_tags=[x.keys()[0] for x in r_non_empty]
    r_no_empty_content=[x.values()[0] for x in r_non_empty]
    print "The set of tags that contain text:",set(r_no_empty_tags)
    for i in set(r_no_empty_tags):
        print "\t",i,":",r_no_empty_tags.count(i)

    r=doc_tree.xpath("//*/n:para", namespaces={'n': 'http://www.unhchr.ch/udhr'})
    print """Double check with xpath "//*/n:para":""", len(r)

    return r_no_empty_tags, r_no_empty_content


## MAIN
parser = etree.XMLParser(encoding='utf-8')
lang_codes =["jpn","eng","cmn_hant","cmn_hans"]

import pandas as pd
df_all=pd.DataFrame()

for lang_code in lang_codes:
    filename = "XML\udhr_%s.xml" % lang_code
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

print len(df_all)


### Caculate ratios based on cmn_hant
#base='cmn_hant'
#sel='length' #'length_encoded_utf8'
def calculate_ratio(df, base, sel):
    import numpy as np
    ## Constructing a list of base lengths 
    times=len(lang_codes)
    a=(0.0+df[df['lang']==base][sel].values)
    l_one=a.tolist()
    l=[]
    for i in range(times):
        l=l+l_one
    col_new=sel.replace("length","length_r")
    df[col_new]=df[sel]/l
    return df

df=calculate_ratio(df_all, base='cmn_hant', sel='length') 
df=calculate_ratio(df, base='cmn_hant', sel='length_encoded_utf8') 
df.to_pickle("r_UDHR.pkl")

##checking
# df[df['lang']=="eng"]['length_r'].values
# df[df['lang']=="eng"]['length_r_encoded_utf8'].values



##r_pivot_para =calculate_ratio(pivot_para,  base='cmn_hant')
##r_pivot_title=calculate_ratio(pivot_title, base='cmn_hant')
##
##r_pivot_para.to_pickle("r_UDHR_para.pkl")
##r_pivot_title.to_pickle("r_UDHR_title.pkl")
