#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tqdm import tqdm
from pathlib import Path


# In[2]:


from lhotse.audio import RecordingSet
from lhotse.supervision import SupervisionSet
from lhotse import CutSet
from lhotse.src.data_fs import LoadFileByFS
from lhotse.supervision import AlignmentItem


# In[3]:


from lhotse.audio import RecordingSet
from lhotse.workflows.activity_detection import SileroVAD16k


# In[4]:


tar_path = '/mnt/dtfast/tts_create_clone/datasets/audioset_nkrya_ruslan_full_asr_clean/'
output_dir = Path(tar_path)
output_dir


# In[5]:


device = "cuda" 
prefix = 'nkrya_ruslan_full_asr_clean'
lang = 'ru'
desired_sample_rate = 16000


# In[6]:


supervision_filename = output_dir / f"{prefix}-{lang}_supervisions.jsonl.gz"
recording_filename = output_dir / f"{prefix}-{lang}_recordings.jsonl.gz"
supervision_filename, recording_filename


# In[7]:


recording_set = RecordingSet.from_file(recording_filename)
len(recording_set), recording_set[0]


# In[8]:


supervision_set = SupervisionSet.from_file(supervision_filename)
len(supervision_set), supervision_set[0]


# In[9]:


vad = SileroVAD16k(device=device) # or device="cuda" or device="cpu"


# In[10]:


new_list_segments = []
for segment, record in tqdm(zip(supervision_set.segments, recording_set.recordings)):
    vad_segments = vad(record)
    list_align = []
    for vad_segm in vad_segments:
        al = AlignmentItem(symbol='',start=vad_segm.start,duration=vad_segm.duration, score=1.0)
        list_align.append(al)
    alignment = segment.alignment
    alignment = {}
    alignment['vad'] = list_align
    segment.alignment = alignment
    new_list_segments.append(segment)
    break


# In[12]:


#new_list_segments


# In[13]:


new_supervision_set = SupervisionSet.from_segments(new_list_segments)


# In[19]:


new_supervision_set[0]


# In[18]:



# In[14]:


#a = new_supervision_set.to_dicts()


# In[15]:


#a


# In[16]:


new_supervision_set.to_file(
    output_dir / f"{prefix}-{lang}_supervisions_words_vad.jsonl.gz"
)


# In[ ]:




