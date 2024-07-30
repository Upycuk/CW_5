from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """

    :param filename:
    :param section:
    :return:
    """
    parser = ConfigParser()
    parser.read(filename)
    a = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            a[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))
    return a
