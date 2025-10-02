import json
import os
import pandas as pd


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
    
    
def load_logs_from_json(filepath):
    """
    Загружает логи из JSON файла и преобразует их в pandas DataFrame.
    
    :param filepath: str, путь к JSON файлу с логами
    :return: pd.DataFrame, DataFrame с данными логов
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            logs_data = json.load(f)
        
        if not logs_data:
            print("Файл с логами пуст")
            return pd.DataFrame()
        
        # Создаем список для хранения строк DataFrame
        rows = []
        
        for log_entry in logs_data:
            # Создаем базовую строку с параметрами
            row = log_entry['parameters'].copy()
            
            # Добавляем итоговый счет оптимизации
            if 'final_optimization_score' in log_entry:
                row['final_optimization_score'] = log_entry['final_optimization_score']
            
            # Добавляем результаты тестов
            for key, value in log_entry.items():
                if key.startswith('test case'):
                    row[key] = value
            
            row['ga_time'] = log_entry['ga_time']
            row['dp_time'] = log_entry['dp_time']
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        print(f"Успешно загружено {len(df)} записей из {filepath}")
        return df
        
    except FileNotFoundError:
        print(f"Файл {filepath} не найден")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return pd.DataFrame()