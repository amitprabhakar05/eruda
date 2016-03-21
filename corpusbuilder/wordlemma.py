# Copyright 2016, Sauvik Biswas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Env imports
import urllib2
import urllib
from bs4 import BeautifulSoup as bsoup
import re
import string

bulletnore = re.compile('<b>(\d+|[a-z])\. </b>')
typere = re.compile('n\.|adj\.|adv\.|v\.|n\.pl\.')

def fetch_raw_data(url, values={}, headers={}, method='POST'):
    data = urllib.urlencode(values)
    if method == 'GET':
        url = url + '?' + data
    req = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'Couldn\'t reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfil the request'
            print 'Error code:', e.code
    else:
        page = response.read()
        return page


#Class to store data
#Loation of page and fetching the data - currently for the plain text English
# dictionary.


vocab_base_address='http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913'


def _locate_page_address(word,source='plaindict'):
    '''The page address depends on the source of vacabulary'''
    address=''
    if not(len(word)):
        address=''
    else:
        address = vocab_base_address+'_'+word[0]+'.html'
    return address


# The following method,
#   1. Searches the word in online dictionary
#   2. Find its types and lemmas
# Inefficient at the moment. Does work on past for of verbs only. Adjective/nouns
# to be done later

def _get_words_lemma(word):
    '''The the words list in the vocab and lemma'''
    web_address = _locate_page_address(word)
    print "Web address is", web_address
    page = fetch_raw_data(web_address)
    #print page

    
    # For return
    # Data returned in this form - (form (flag) and, lemma)
    all_tuples=[]
    
    # Regualr expressions for different POS - needs to be populated
    re_nnp = re.compile('n\.')
    re_vbp = re.compile('v\. t|i\.')
    re_det = re.compile('a\.')
    re_mod = re.compile('adj\.')
    re_ppt = re.compile('p\. p\.')

    reg_pattern = re.compile('\s*<P><B>'+word+'</B>(.+)</P>\s*', re.I)
    ans = reg_pattern.findall(page)
    print "Got the answer from findall ", len(ans)
    for w in ans:
        print "Mathced pattern: ", w
        patt_type = re.compile('\s*\(<I>(.+)</I>\)\s*(.+)',re.I)
        ans_type = patt_type.search(w)
        if not ans_type:
            print "Could not find anything about the word type."
            continue
        ans_type1 = ans_type.group(1)
        print "Type is ", ans_type1
        
        # check the category/type of the dictionary POS
        if (re_nnp.search(ans_type1) ):
            tup1 = ( 'NNP', word)
            all_tuples.append(tup1)
        elif(re_vbp.search(ans_type1)):
            print "An action type"
            all_tuples.append(('VB',word))
        elif(re_det.search(ans_type1)):
            print "a DET type"
            all_tuples.append(('DET',word))
        elif(re_mod.search(ans_type1)):
            all_tuples.append(('MOD',word))
        elif(re_ppt.search(ans_type1)):
            print "The word has a past tense form", ans_type1, ans_type.group(2)
            patt_lemma = re.compile('of (.+)', re.I)
            lemma = patt_lemma.search(ans_type.group(2))
            if not lemma:
                print "NO lemma found"
                continue
            print "The lemma", lemma.group(1)
            all_tuples.append(('VPT', lemma.group(1)))
        else:
            print "Pata nahi"
              
    print "All the lemmas collected are"
    return all_tuples


# testing - for word fly
print _get_words_lemma('said')




