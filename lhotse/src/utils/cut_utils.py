from typing import LiteralString
import numpy as np
import lhotse


def _get_feat_extract_output_lengths(input_lengths: int):
    """
    Computes the output length of the convolutional layers for Whisper
    """
    input_lengths = (input_lengths - 1) // 2 + 1

    return input_lengths

def get_it_values(it, custom_keys=[], align_keys=[]) -> list[dict[str, str|float]]:
    """
    Преобразует список кутов в список значений, для последующего извлечения информации
    """
    if isinstance(it, lhotse.cut.mixed.MixTrack):
        #print('mix',it.cut)
        add_it = {'offset': it.offset,
                  'type': 'offset'}        
        return [add_it] + get_it_values(it.cut, custom_keys, align_keys)
    elif isinstance(it, lhotse.cut.mono.MonoCut):
        if len(it.supervisions) > 0:
            list_timeline = []
            for supervision in it.supervisions:
                duration = supervision.duration
                speaker = supervision.speaker
                gender = supervision.gender
                language = supervision.language
                #print(it)
                add_it = {'duration': duration,
                          'type': 'supervision',
                          'speaker': speaker,
                          'filename': it.recording.sources[0].source,
                          'recordnig_duration': it.recording.duration,
                          'text': supervision.text,
                          'language': language,
                          'gender': gender}
                for custom_key in custom_keys:
                    if custom_key in supervision.custom.keys() and custom_key != 'text':
                        add_it[custom_key] = supervision.custom[custom_key]
                    else:
                        add_it[custom_key] = ''
                for custom_key in align_keys:
                    if custom_key in supervision.alignment.keys():
                        add_it[custom_key] = supervision.alignment[custom_key]
                    else:
                        add_it[custom_key] = ''
                list_timeline.append(add_it)
            return list_timeline
        if it.recording:
            #print(it)
            list_timeline = []
            duration = it.duration
            add_it = {'duration': duration,
                      'type': 'monocut recording'}
            list_timeline.append(add_it)
            return list_timeline
    elif isinstance(it, lhotse.cut.mixed.MixedCut):
        #print('MixedCut:',it)
        list_timeline = []
        for mix_track in it.tracks:
            list_add_it = get_it_values(mix_track, custom_keys, align_keys)
            
            list_timeline.extend(list_add_it)
            #print(calc_duration(list_add_it))
        return list_timeline
    elif isinstance(it, lhotse.cut.padding.PaddingCut):
        return [{'duration': it.duration,'type': 'pause'}]
    
    print('not found type:', type(it))
    print('not found obj:', it)
    return None

def round_to_nearest(value, multiple):
    return round(value / multiple) * multiple

def get_text_from_batch(batch_cuts, pause_token=' ', text_column:str = None, with_time = False) -> str:
    """
    Вытягивает из списка информации текст и тайм метки
    Выставление метод сделано на подобие модели whisper-large-v3-turbo
    """
    list_timeline = get_it_values(batch_cuts, [text_column])
    if text_column is None:
        text_column = 'text'
    list_text = []
    list_pause = []
    end_text = 0
    offset = 0
    for time_item in list_timeline:
        if 'type' in time_item.keys() and time_item['type'] == 'offset':
            offset = time_item['offset']
        if 'type' in time_item.keys() and time_item['type'] == 'pause':
            list_pause.append(pause_token)
        if 'type' in time_item.keys() and time_item['type'] == 'supervision':
            if time_item[text_column]:
                if with_time:
                    offset = round_to_nearest(offset, 0.02)
                    list_text.append(f'<|{offset:.2f}|>')
                list_text.extend(list_pause)
                list_text.append(time_item[text_column])
            else:
                list_text.extend(list_pause)
            list_pause = []
            end_text = offset + time_item['duration']
            if with_time:
                end_text = round_to_nearest(end_text, 0.02)
                list_text.append(f'<|{end_text:.2f}|>')
    text = ''.join(list_text)    
    return text

def get_align_from_batch(batch_cuts, align_column:str = None) -> str:
    """
    Вытягивает из списка информации о aligned временных метках
    """
    list_timeline = get_it_values(batch_cuts, align_keys=[align_column])
    list_text = []
    end_text = 0
    offset = 0
    for time_item in list_timeline:
        if 'type' in time_item.keys() and time_item['type'] == 'offset':
            offset = time_item['offset']
        if 'type' in time_item.keys() and time_item['type'] == 'pause':
            pass
        if 'type' in time_item.keys() and time_item['type'] == 'supervision':
            if time_item[align_column]:
                for align_item in time_item[align_column]:
                    dict_item = {'start': align_item.start,
                                 'duration': align_item.duration,
                                 'symbol': align_item.symbol,
                                 'speaker': time_item['speaker'],
                                 'score': align_item.score}
                    dict_item['start'] += offset
                    list_text.append(dict_item)
            else:
                pass
            end_text = offset + time_item['duration']
    return list_text, end_text

def create_futures_labels(batch_cuts, align_column, hop_length, sample_rate, class_column = None, max_class = 1):
    '''
    Данный класс специально заточен под Whisper
    из за функции _get_feat_extract_output_lengths
    '''
    time_line, duration = get_align_from_batch(batch_cuts, align_column)
    time_calc = lambda x: int(_get_feat_extract_output_lengths(x*sample_rate//hop_length))
    time_duration = time_calc(duration)
    if class_column is None: # VAD
        np_labels = np.zeros(time_duration, dtype=np.int32)
    else:
        np_labels = np.zeros([time_duration, max_class], dtype=np.int32)
    list_class = []
    for time_item in time_line:
        time_start = time_item['start']
        time_end = time_item['start'] + time_item['duration']
        time_start = time_calc(time_start)
        time_end = time_calc(time_end)
        
        time_start = max(0, time_start)
        time_end = min(time_duration, time_end)
        
        if class_column:
            class_item = time_item[class_column]
            if not class_item in list_class:
                list_class.append(class_item)
            index_class = list_class.index(class_item)
            if index_class < max_class:
                np_labels[time_start:time_end,index_class] = 1
        else:    
            np_labels[time_start:time_end] = 1
        
    return np_labels[np.newaxis,...]
