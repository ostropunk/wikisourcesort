#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re


# In[2]:


def get_excel_dict(excelfile, key=None, index_col=0, header=0):
    dataframe = pd.read_excel(excelfile, index_col=index_col, header=header)
    dictionary = dataframe.to_dict()
    if key is None:
        return dictionary
    else:
        return dictionary[key]
    
    


# In[3]:


def textreader(text):
    '''Opens textfile and returns the content as a string'''
    with open(text, 'rt', encoding="utf8") as wiki:
        txtstring = wiki.read()
    return txtstring


# In[44]:


def replace_from_dict(text, dictionary):
    '''Replaces words in text with new words in dictionary'''
    for word in dictionary:
        text = text.replace(word, dictionary[word])
    return text


# In[172]:


def get_ref(text):
    '''
       Finds references between the <ref>- and </ref>-tags 
       and returns them as a list of strings
    '''
    ref = re.findall("\<ref.+?\<\/ref\>", text)
    return ref


# In[171]:


def getrefurl(ref):
    '''Finds the reference url in references and returns it as a string'''
    url = re.search("http.+?(?=\s|\|title=|\|titel|\}\})", ref)
    url = url.group()
    return url


# In[30]:


def get_domain_name(url):
    '''
    Finds the domain name of the reference url and 
    returns that name as a string.
    '''
    domain_name = re.search('(?<=\/\/).+?(?=\/)', url)
    domain_name = domain_name.group()
    if domain_name.startswith('www.'):
        domain_name = domain_name.replace('www.', '')
    return domain_name


# In[32]:


def update_ref_dict(ref, ref_dict, ref_counts):
    refurl = getrefurl(ref)
    domain_name = get_domain_name(refurl)
    if refurl not in ref_dict:
        if domain_name not in ref_counts: 
            ref_counts.update({domain_name:1})
            refname = domain_name + '.' + str(ref_counts[domain_name])
        else:
            ref_counts[domain_name] = ref_counts[domain_name] + 1
            refname = domain_name + '.' + str(ref_counts[domain_name])
        ref_dict.update({refurl:{'refs': [ref], 'refname': refname, 'refurl': refurl}})
    else:
        if ref not in ref_dict[refurl]['refs']:
            ref_dict[refurl]['refs'].append(ref)
    return ref_dict, ref_counts


# In[36]:


def create_ref_dict(refs):
    '''
    Takes a list of references, extracts the reference url and name, 
    and returns a dictionary sorted on the referenceurl as key.
    '''
    ref_dict = {}
    ref_counts = {}
    for ref in refs:
        ref_dict, ref_counts = update_ref_dict(ref, ref_dict, ref_counts)
    return ref_dict
    


# In[79]:


def get_ref_tag(text):
    '''
       Finds references between the <ref>- and </ref>-tags 
       and returns them as a list of strings
    '''
    ref = re.findall("\<ref name\=.+?\/\>", text)
    #ref = re.findall("\<ref.+?\<\/ref\>|\<ref name\=.+?\/\>", text)
    #ref = re.findall("\<ref.+?(?!\"\s\/\>)\<\/ref>", text)
    #ref = re.findall("\<ref.+?\<\/ref\>", text)
    return set(ref)


# In[130]:


def get_spec_ref(text, ref_tag):
    '''
       Finds references between the <ref>- and </ref>-tags 
       and returns them as a list of strings
    '''
    #ref = re.findall("\<ref name\=.+?\/\>", text)
    #ref = re.findall("\<ref.+?\<\/ref\>|\<ref name\=.+?\/\>", text)
    #ref = re.findall("\<ref.+?(?!\"\s\/\>)\<\/ref>", text)
    ref = re.findall(f'\<ref name\=\"{ref_tag}\"\>.+?\<\/ref\>', text)
    ref = ref[0]
    return ref


# In[115]:


def get_ref_tag_name(ref_tag):
    ref_tag_name = re.findall('\".+\"', ref_tag)
    ref_tag_name = ref_tag_name[0].replace('"', '')
    return ref_tag_name


# In[136]:


def replace_tags(text):
    ref_tags = get_ref_tag(text)
    for tag in ref_tags:
        name = get_ref_tag_name(tag)
        spec_ref = get_spec_ref(text, name)
        text = text.replace(tag, spec_ref)
    return text


# In[49]:


def replace_countries(text):
    countries = get_excel_dict('countries2.xlsx', 'Länder')
    text = replace_from_dict(text, countries)
    return text


# In[66]:


def replace_headers(text):
    headers = {'English title':'Engelsk titel', 
               'Original title':'Originaltitel', 
               'Director(s)':'Regissör(er)', 
               'Country':'Land', 
               'School':'Skola'}
    text = replace_from_dict(text, headers)
    return text


# In[169]:


def reference_sorter(text):
    '''
    Does a bunch of stuff that should be broken out in different functions.
    '''
    references = get_ref(text)
    reference_dict = create_ref_dict(references)
    reference_list =  []
    reference_text = '== Referenser ==\n<references>\n'

    text = text.replace('== Källor ==', '== Referenser ==')
    text = text.replace('<references/>', '')

    for entry in reference_dict:
        for reference in reference_dict[entry]['refs']:
            text = text.replace(reference, '<ref name="{}" />'.format(reference_dict[entry]['refname']))
        reference_list.append('<ref name="{}">{}</ref>'.format(reference_dict[entry]['refname'], entry))
    for reference in reference_list:
        reference_text += reference +'\n'
    reference_text += '</references>'
    text = re.split('== Referenser ==', text)
    text = text[0] + reference_text + text[-1]

    return text


# In[134]:


def fix_wiki_entry(textfile):
    with open(textfile, 'r', encoding="utf8") as txt:
        text = txt.read()
        text = replace_tags(text)
        text = reference_sorter(text)
        text = replace_countries(text)
        text = replace_headers(text)
        with open('new_' + textfile, 'w', encoding='utf8') as new_text:
            new_text.write(text)
        return text
        


# In[173]:


def main():
    fix_wiki_entry(input('Please enter input textfile:'))

if __name__ == "__main__":
    main()

