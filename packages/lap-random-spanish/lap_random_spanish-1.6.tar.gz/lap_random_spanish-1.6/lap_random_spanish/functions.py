import pandas as pd


def getRandomMaleName(numberNames=1, fullName=False, files=None):

    name = pd.read_csv(files[0])
    if numberNames >= 2:
        result_array = []
        surname = pd.read_csv(files[1])
        for i in range(numberNames):
            temporal_return = name.sample()["nombre"].to_string(
                index=False).strip()
            if fullName:
                temporal_return += " "
                temporal_return += surname.sample(
                )["apellido"].to_string(index=False)
                temporal_return += " "
                temporal_return += surname.sample(
                )["apellido"].to_string(index=False)
            result_array.append(temporal_return)
        return result_array
    else:
        result_string = name.sample()["nombre"].to_string(index=False).strip()
        return result_string


def getRandomFemaleName(numberNames=1, fullName=False, files=None):

    name = pd.read_csv(files[0])
    if numberNames >= 2:
        result_array = []
        surname = pd.read_csv(files[1])
        for i in range(numberNames):
            temporal_return = name.sample()["nombre"].to_string(
                index=False).strip()
            if fullName:
                temporal_return += " "
                temporal_return += surname.sample(
                )["apellido"].to_string(index=False)
                temporal_return += " "
                temporal_return += surname.sample(
                )["apellido"].to_string(index=False)
            result_array.append(temporal_return)
        return result_array
    else:
        result_string = name.sample()["nombre"].to_string(index=False).strip()
        return result_string


def getRandomSurname(numberSurnames=1, pairs=False, files=None):

    surname = pd.read_csv(files[0])
    if numberSurnames >= 2:
        result_array = []
        tmp = ""
        for i in range(numberSurnames):
            if pairs:
                tmp = surname.sample()["apellido"].to_string(index=False)
            result_array.append(
                surname.sample()["apellido"].to_string(index=False) + " " + tmp)
        return result_array
    else:
        tmp = ""
        if pairs:
            tmp = surname.sample()["apellido"].to_string(index=False)
        return f"{surname.sample()['apellido'].to_string(index=False) + ' ' + tmp}"
