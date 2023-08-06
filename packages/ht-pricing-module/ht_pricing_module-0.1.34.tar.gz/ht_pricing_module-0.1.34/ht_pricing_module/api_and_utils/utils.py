from .packages import DataFrame
from .packages import Union
from .packages import deepcopy


class _Const(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f"rebind const({name}) is not allowed")
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise TypeError(f"rebind const({name}) is not allowed")
        raise NameError(name)


class Struct(dict):
    """
    实现将dict类型转换成结构体类型，可以直接通过 ”.“ 调用其属性。
    服务器定价器接收参数为grpc定义的message类型，定价函数中全部使用 “self.param.” 进行调用。
    为统一标准，传入的参数dict需转化成该结构体类型进行使用。

    e.g.
    param = Struct()
    param['spot_price'] = 100 or param.spot_price = 100
    pricer = Vanilla(kwargs)
    pv = pricer.present_value()
    ...

    现版本中可接受直接传入dict类型或Struct类型
    """

    def __init__(self, *args, **kwargs) -> None:
        super(Struct, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = Struct(value)
        return value

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    @classmethod
    def RepeatedStruct(cls, input: Union[dict, list, DataFrame]) -> list:
        """
        该方法仅在调用蒙特卡洛MC方法时,需要传入指定观察日序列时使用。
        服务端定价器参数通过 ”.“ 调用其属性，直接调用定价函数时，需要使用该方法对传入的观察日dict或DataFrame序列进行转换
        :param input: dict or DataFrame
        :return: [Struct(), Struct(), Struct(), ...]

        e.g.
        discrete_asian_mc，param.obs_date参数
        param = Struct()
        param['obs_date'] = RepeatedStruct({'obs_index': [1, 2, 3, ... ],
                                            'obs_price': [100, 99, 100, ...]})
        ...
        """

        output = []
        if isinstance(input, dict):
            _keys = list(input.keys())
            _length = len(input[_keys[0]])
        elif isinstance(input, DataFrame):
            _keys = list(input.columns)
            _length = len(input)
        elif isinstance(input, list):
            for i in input:
                if not isinstance(i, Struct):
                    raise TypeError(f"check the type of element {i}")
            return input
        else:
            raise TypeError(type(input))

        for i in range(_length):
            struct = Struct()
            for k in _keys:
                setattr(struct, k, input[k][i])
            output.append(struct)
        return output
