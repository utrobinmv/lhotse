from typing import LiteralString
import lhotse



def get_it_values(it, custom_keys=[]) -> list[dict[str, str|float]]:
    """
    Преобразует список кутов в список значений, для последующего извлечения информации
    """
    if isinstance(it, lhotse.cut.mixed.MixTrack):
        #print('mix',it.cut)
        add_it = {'offset': it.offset,
                  'type': 'offset'}        
        return [add_it] + get_it_values(it.cut)
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
                    if custom_key in supervision.custom.keys():
                        add_it[custom_key] = supervision.custom[custom_key]
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
            list_add_it = get_it_values(mix_track)
            
            list_timeline.extend(list_add_it)
            #print(calc_duration(list_add_it))
        return list_timeline
    elif isinstance(it, lhotse.cut.padding.PaddingCut):
        return [{'duration': it.duration,'type': 'pause'}]
    
    print('not found type:', type(it))
    print('not found obj:', it)
    return None


def get_text_from_batch(batch_cuts, pause_token=' ', text_column:str = 'text', with_time = False) -> str:
    """
    Вытягивает из списка информации текст и тайм метки
    """
    list_timeline = get_it_values(batch_cuts)
    list_text = []
    end_text = 0
    offset = 0
    for time_item in list_timeline:
        if 'type' in time_item.keys() and time_item['type'] == 'offset':
            offset = time_item['offset']
        if 'type' in time_item.keys() and time_item['type'] == 'pause':
            list_text.append(pause_token)
        if 'type' in time_item.keys() and time_item['type'] == 'supervision':
            if time_item[text_column]:
                if with_time:
                    list_text.append(f'<|{offset:.2f}|>')
                list_text.append(time_item[text_column])
            end_text = offset + time_item['duration']
    if with_time:
        list_text.append(f'<|{end_text:.2f}|>')
    text = ''.join(list_text)    
    return text