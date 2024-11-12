import numpy as np
from torch.utils.data import IterableDataset


class IterableDatasetWithLang(IterableDataset):
    def __init__(self, ds: IterableDataset, dict_columns: dict[str,str] = {}):
        self.dict_columns = dict_columns
        self.ds = ds
        super().__init__()
    def __iter__(self):
        for item in self.ds:
            len_cut = len(item['cut'])
            for key in self.dict_columns.keys():
                item[key] = [self.dict_columns[key]] * len_cut
            yield item


class IterableDatasetRandom(IterableDataset):
    def __init__(self, list_ds: list[IterableDataset]):
        self.list_ds = [iter(ds) for ds in list_ds]
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
            yield next(self.list_ds[chosen_index])