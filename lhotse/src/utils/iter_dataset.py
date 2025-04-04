import numpy as np
from torch.utils.data import IterableDataset


class IterableDatasetWithLang(IterableDataset):
    def __init__(self, ds: IterableDataset, restart=False, dict_columns: dict[str,str] = {}, debug = False):
        self.dict_columns = dict_columns
        self.ds = ds
        self.restart = restart
        self.debug = debug
        super().__init__()
    def __iter__(self):
        while True:
            for item in self.ds:
                len_cut = len(item['cut'])
                for key in self.dict_columns.keys():
                    item[key] = [self.dict_columns[key]] * len_cut
                yield item
            if not self.restart:
                break
            elif self.debug:
                print('restart dataset:', self.dict_columns)


class IterableDatasetRandom(IterableDataset):
    def __init__(self, list_ds: list[IterableDataset]):
        self.list_ds = [ds for ds in list_ds]
        self.iter_ds = [iter(ds) for ds in self.list_ds]
        self.ds_num = len(list_ds)
        self.ds_prob = np.zeros(self.ds_num)
        self.weights = np.zeros(self.ds_num)
    def __iter__(self):
        # Добавить выбор датасета из списка случайным образом при этом больший приоритет
        # имеет тот датасет который выбирался меньше всего
        # при выборе из N датасета информация записывалась бы в счетчик self.ds_prob[N]
        while True:  # Бесконечный итератор
            # Вычисляем веса на основе количества выборов
            weights = 1 / (self.ds_prob + 1)  # Чем меньше выборов, тем больше вес
            weights /= weights.sum()  # Нормализуем веса
            self.weights = weights
            chosen_index = np.random.choice(self.ds_num, p=weights)  # Выбираем индекс датасета
            self.ds_prob[chosen_index] += 1  # Увеличиваем счетчик для выбранного датасета
            
            # Возвращаем элементы из выбранного датасета
            batch = next(self.iter_ds[chosen_index], 'end')
            if batch == 'end': # Перезагрузим датасет
                self.iter_ds[chosen_index] = iter(self.list_ds[chosen_index])
                batch = next(self.iter_ds[chosen_index])

            yield batch