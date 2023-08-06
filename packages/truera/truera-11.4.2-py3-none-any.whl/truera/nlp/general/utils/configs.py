from enum import Enum
from enum import unique

import truera.rnn.general.utils.colors as Colors


@unique
class QoIType(Enum):
    MAX_CLASS = 'max_class'
    CLASS_WISE = 'class'

    def get_attr_artifact_save_name(self, signs: bool = False) -> str:
        return self.value + '_token_attrs' + ("_signs" if signs else "")

    def get_human_readable(self) -> str:
        # e.g. MAX_CLASS -> Max-Class
        return self.name.title().replace('_', '-')

    @classmethod
    def from_str(cls, type_str: str):
        if (type_str.lower() in ['max', 'max_class']):
            return cls.MAX_CLASS
        elif (type_str.lower() in ['class', 'class_wise']):
            return cls.CLASS_WISE
        else:
            raise NotImplementedError(
                'The {} QoI Type is not supported.'.format(type_str)
            )

    def get_class_idx_name(self, class_idx=None):
        if self.value == 'class':
            assert class_idx is not None
            return 'class_{}'.format(int(class_idx))
        elif self.value == 'max_class':
            return 'class_max'
        raise NotImplementedError('The QoI Type is not supported.')

    def get_class_idx(self, qoi_class_name: str):
        if self.value == "class":
            return int(qoi_class_name.split("_")[-1])
        elif self.value == "max_class":
            raise ValueError(
                "Cannot extra class index when QoIType == 'max_class'"
            )
        raise NotImplementedError('The QoI Type is not supported.')

    def get_qoi_type_widget_options(self, num_class):
        if self.value == 'class':
            return ['class_{}'.format(int(i)) for i in range(num_class)]
        elif self.value == 'max_class':
            return ['class_max']
        raise NotImplementedError('The QoI Type is not supported.')

    def get_class_colors(self, num_class):
        if self.value == 'class':
            return [
                # hack because we only have 5 colors
                Colors.DEFAULT_COLOR_WHEEL[int(i) % 5]
                for i in range(num_class)
            ]
        elif self.value == 'max_class':
            return [Colors.DEFAULT_COLOR_WHEEL[0]]
        raise NotImplementedError('The QoI Type is not supported.')

    def get_influence_class_dimension(self, num_class):
        if self.value == 'class':
            return num_class
        elif self.value == 'max_class':
            return 1
        raise NotImplementedError('The QoI Type is not supported.')


def get_class_idx_from_qoi_widget_options(qoi_class):
    if (qoi_class == 'class_max'):
        return 0
    elif qoi_class.split('_')[0] == 'class':
        try:
            class_ind = int(qoi_class.split('_')[1])
            return class_ind
        except:
            print('cannot parse widget name')
    raise NotImplementedError('the qoi widget name is not supported')


def get_influence_from_qoi_widget_options(qoi_class, influence):
    class_ind = get_class_idx_from_qoi_widget_options(qoi_class)
    return influence[class_ind]


@unique
class OutputLayerType(str, Enum):
    LOGIT = 'logit'
    PROBIT = 'probit'

    @staticmethod
    def from_str(type):
        if type == 'logit':
            return OutputLayerType.LOGIT
        elif type == 'probit':
            return OutputLayerType.PROBIT
        raise NotImplementedError(f'OutputLayerType {type} not supported')


@unique
class TokenType(str, Enum):
    WORD = 'word'
    TOKEN = 'token'

    @classmethod
    def from_str(cls, type_str):
        if (type_str.lower() in ['word', 'combined_word']):
            return cls.WORD
        elif (type_str.lower() in ['token']):
            return cls.TOKEN
        else:
            raise NotImplementedError(
                'The {} TokenType is not supported.'.format(type_str)
            )
