def read_config(path: str) -> dict[str, str]:
    """Config file ma mieć strukturę jak poniżej
    key1=value1
    key2=value2
    key3=value3
    key4=value4
    """
    result={}
    with open(path) as f:
        for line in f:
            key, value = line.strip().split('=')
            result[key.strip()] = value.strip()

    return result

if __name__ == '__name__':
    result=read_config('temp.txt')
    print(result)