#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


root_dir = '/share/disk_audio/create_audio_dataset/Mozilla_Common_Voice_dataset/'


# In[3]:


out_dir = os.path.join(root_dir, 'lhotse')


# In[4]:



# In[5]:


corpus_name = 'cv-corpus-10.0-2022-07-04-ru.tar'


# In[6]:


corpus_dir = os.path.join(root_dir, corpus_name)


# In[7]:


import lhotse


# In[8]:


from lhotse.src import LoadFileByFS


# In[10]:


tar_basename = 'tar://' + corpus_name


# In[11]:


# fs = LoadFileByFS()

# data = fs.load_fs_filename(root_dir=root_dir, fullname=tar_basename)


# In[12]:


parts = ['validated', 'train', 'other', 'dev', 'test', 'invalidated']
# parts = ['test']
#lhotse.recipes.prepare_commonvoice(corpus_dir, out_dir, prefix = 'cv-corpus-10.0-2022-07-04', languages=['ru'], splits = ['validated', 'train', 'other', 'dev', 'test', 'invalidated'], num_jobs=1)
lhotse.recipes.prepare_commonvoice(corpus_dir, out_dir, prefix = 'cv-corpus-10.0-2022-07-04', languages=['ru'], splits = parts, num_jobs=1)

corpus_name = 'cv-corpus-11.0-2022-09-21-zh-CN.tar'
corpus_dir = os.path.join(root_dir, corpus_name)

lhotse.recipes.prepare_commonvoice(corpus_dir, out_dir, prefix = 'cv-corpus-11.0-2022-09-21', languages=['zh-CN'], splits = parts, num_jobs=1)

corpus_name = 'cv-corpus-10.0-2022-07-04-en.tar'
corpus_dir = os.path.join(root_dir, corpus_name)

lhotse.recipes.prepare_commonvoice(corpus_dir, out_dir, prefix = 'cv-corpus-10.0-2022-07-04', languages=['en'], splits = parts, num_jobs=1)


# In[ ]:




