import pandas as pd

"""
Сейчас наличие этого файла может казаться комичным, учитывая его объем =)
Его необходимость была обусловленна в течение работы, так как я использовал разные преобразования данных. В конечном счёте только эти две функции действительно пригодились для итогового результата.
"""

def type_to_rang(tp):
    dct = {
        'Overweight_Level_II': 4,
        'Normal_Weight': 2,
        'Insufficient_Weight': 1,
        'Obesity_Type_III': 7,
        'Obesity_Type_II': 6,
        'Overweight_Level_I': 3,
        'Obesity_Type_I': 5        
    }
    return dct[tp]

def make_BMI(data: pd.DataFrame):
    return pd.DataFrame({'BMI': data['Weight'] / data['Height'] ** 2}) 
    