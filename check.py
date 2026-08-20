import pandas as pd # читать таблицы
import requests #отправлять запросы в api
import time #делать задержку между запросами


dataset = pd.read_csv('data/dataset.csv')
answers = pd.read_csv('data/answers.csv')

#адрес апи
url = "http://127.0.0.1:8001/v1/authz"

results = []

#отправка запросов в цикл
for idx, row in dataset.iterrows():
    response = requests.post(url, json ={
        "t": int(row['t']),
        "d": int(row['d']),
        "a": int(row['a']),
        "c": int(row['c'])
    })
    pred = response.json()
    results.append({
        'user': row['user'],
        'predicted_R': pred['riskScore'],
        'predocted_pdase': pred['phase']
    })

    time.sleep(0.05)

df_results = pd.DataFrame(results)
df_results.to_csv('data/predictions.csv', index=False)

print("Сохранение результата обработки в data/predictions.csv")
print(f"Всего обработано: {len(results)} записей")

