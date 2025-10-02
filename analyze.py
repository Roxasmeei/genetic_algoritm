import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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


def analyze_grid_search_results(df):
    """
    Анализирует результаты GridSearch.
    
    :param df: pd.DataFrame, DataFrame с результатами GridSearch
    """
    if df.empty:
        print("DataFrame пуст, анализ невозможен")
        return
    
    print("=== АНАЛИЗ РЕЗУЛЬТАТОВ GRID SEARCH ===\n")
    
    # Основная информация о данных
    print(f"Общее количество экспериментов: {len(df)}")
    print(f"Количество параметров: {len([col for col in df.columns if col not in ['final_optimization_score'] and not col.startswith('test case')])}")
    print(f"Количество тестовых случаев: {len([col for col in df.columns if col.startswith('test case')])}")
    
    # Статистика по итоговому счету оптимизации
    if 'final_optimization_score' in df.columns:
        print(f"\n=== СТАТИСТИКА ПО ИТОГОВОМУ СЧЕТУ ОПТИМИЗАЦИИ ===")
        print(f"Минимальный счет: {df['final_optimization_score'].min():.6f}")
        print(f"Максимальный счет: {df['final_optimization_score'].max():.6f}")
        print(f"Средний счет: {df['final_optimization_score'].mean():.6f}")
        print(f"Медианный счет: {df['final_optimization_score'].median():.6f}")
        print(f"Стандартное отклонение: {df['final_optimization_score'].std():.6f}")
        
        # Лучшая комбинация параметров
        best_idx = df['final_optimization_score'].idxmin()
        print(f"\n=== ЛУЧШАЯ КОМБИНАЦИЯ ПАРАМЕТРОВ ===")
        print(f"Индекс: {best_idx}")
        print(f"Итоговый счет: {df.loc[best_idx, 'final_optimization_score']:.6f}")
        
        # Параметры лучшей комбинации
        param_columns = [col for col in df.columns if col not in ['final_optimization_score'] and not col.startswith('test case')]
        print("Параметры:")
        for param in param_columns:
            print(f"  {param}: {df.loc[best_idx, param]}")
    
    # Корреляционный анализ
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 1:
        print(f"\n=== КОРРЕЛЯЦИОННАЯ МАТРИЦА ===")
        correlation_matrix = df[numeric_columns].corr()
        print(correlation_matrix.round(4))


def visualize_results(df):
    """
    Создает визуализации результатов GridSearch.
    
    :param df: pd.DataFrame, DataFrame с результатами GridSearch
    """
    if df.empty:
        print("DataFrame пуст, визуализация невозможна")
        return
    
    # Настройка стиля
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Создаем фигуру с подграфиками
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Гистограмма итогового счета оптимизации
    if 'final_optimization_score' in df.columns:
        plt.subplot(2, 3, 1)
        plt.hist(df['final_optimization_score'], bins=20, alpha=0.7, edgecolor='black')
        plt.title('Распределение итогового счета оптимизации')
        plt.xlabel('Итоговый счет')
        plt.ylabel('Частота')
        plt.grid(True, alpha=0.3)
    
    # 2. Boxplot для итогового счета
    if 'final_optimization_score' in df.columns:
        plt.subplot(2, 3, 2)
        plt.boxplot(df['final_optimization_score'])
        plt.title('Boxplot итогового счета оптимизации')
        plt.ylabel('Итоговый счет')
        plt.grid(True, alpha=0.3)
    
    # 3. Корреляционная матрица (heatmap)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 1:
        plt.subplot(2, 3, 3)
        correlation_matrix = df[numeric_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('Корреляционная матрица')
    
    # 4. Scatter plot лучших результатов
    if 'final_optimization_score' in df.columns and len(df) > 1:
        plt.subplot(2, 3, 4)
        plt.scatter(range(len(df)), df['final_optimization_score'], alpha=0.6)
        plt.title('Итоговый счет по экспериментам')
        plt.xlabel('Номер эксперимента')
        plt.ylabel('Итоговый счет')
        plt.grid(True, alpha=0.3)
    
    # 5. Анализ параметров (если есть категориальные)
    param_columns = [col for col in df.columns if col not in ['final_optimization_score'] and not col.startswith('test case')]
    if param_columns and 'final_optimization_score' in df.columns:
        plt.subplot(2, 3, 5)
        # Выбираем первый параметр для анализа
        first_param = param_columns[0]
        unique_values = df[first_param].unique()
        if len(unique_values) <= 10:  # Если значений немного, делаем boxplot
            df.boxplot(column='final_optimization_score', by=first_param, ax=plt.gca())
            plt.title(f'Итоговый счет по {first_param}')
            plt.suptitle('')  # Убираем автоматический заголовок
        else:  # Иначе scatter plot
            plt.scatter(df[first_param], df['final_optimization_score'], alpha=0.6)
            plt.xlabel(first_param)
            plt.ylabel('Итоговый счет')
            plt.title(f'Зависимость итогового счета от {first_param}')
        plt.grid(True, alpha=0.3)
    
    # 6. Топ-10 лучших результатов
    if 'final_optimization_score' in df.columns and len(df) >= 10:
        plt.subplot(2, 3, 6)
        top_10 = df.nsmallest(10, 'final_optimization_score')
        plt.bar(range(len(top_10)), top_10['final_optimization_score'])
        plt.title('Топ-10 лучших результатов')
        plt.xlabel('Ранг')
        plt.ylabel('Итоговый счет')
        plt.xticks(range(len(top_10)), [f'{i+1}' for i in range(len(top_10))])
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def save_analysis_report(df, output_file='analysis_report.txt'):
    """
    Сохраняет отчет анализа в текстовый файл.
    
    :param df: pd.DataFrame, DataFrame с результатами GridSearch
    :param output_file: str, имя файла для сохранения отчета
    """
    if df.empty:
        print("DataFrame пуст, отчет не может быть создан")
        return
    
    # Создаем директорию, если она не существует
    directory = os.path.dirname(output_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== ОТЧЕТ АНАЛИЗА GRID SEARCH ===\n\n")
        
        # Основная информация
        f.write(f"Общее количество экспериментов: {len(df)}\n")
        f.write(f"Количество параметров: {len([col for col in df.columns if col not in ['final_optimization_score'] and not col.startswith('test case')])}\n")
        f.write(f"Количество тестовых случаев: {len([col for col in df.columns if col.startswith('test case')])}\n\n")
        
        # Статистика
        if 'final_optimization_score' in df.columns:
            f.write("=== СТАТИСТИКА ПО ИТОГОВОМУ СЧЕТУ ОПТИМИЗАЦИИ ===\n")
            f.write(f"Минимальный счет: {df['final_optimization_score'].min():.6f}\n")
            f.write(f"Максимальный счет: {df['final_optimization_score'].max():.6f}\n")
            f.write(f"Средний счет: {df['final_optimization_score'].mean():.6f}\n")
            f.write(f"Медианный счет: {df['final_optimization_score'].median():.6f}\n")
            f.write(f"Стандартное отклонение: {df['final_optimization_score'].std():.6f}\n\n")
            
            # Лучшая комбинация
            best_idx = df['final_optimization_score'].idxmin()
            f.write("=== ЛУЧШАЯ КОМБИНАЦИЯ ПАРАМЕТРОВ ===\n")
            f.write(f"Итоговый счет: {df.loc[best_idx, 'final_optimization_score']:.6f}\n")
            
            param_columns = [col for col in df.columns if col not in ['final_optimization_score'] and not col.startswith('test case')]
            f.write("Параметры:\n")
            for param in param_columns:
                f.write(f"  {param}: {df.loc[best_idx, param]}\n")
    
    print(f"Отчет сохранен в файл: {output_file}")


def main():
    """
    Основная функция для анализа результатов GridSearch.
    """
    # Путь к файлу с логами
    logs_file = 'results/logs.json'
    
    print("Загрузка данных из results/logs.json...")
    df = load_logs_from_json(logs_file)
    
    if not df.empty:
        print("\nИнформация о загруженных данных:")
        print(f"Размер DataFrame: {df.shape}")
        print(f"Столбцы: {list(df.columns)}")
        print(f"\nПервые 5 строк:")
        print(df.head())
        
        print("\n" + "="*50)
        analyze_grid_search_results(df)
        
        print("\n" + "="*50)
        print("Создание визуализаций...")
        visualize_results(df)
        
        print("\n" + "="*50)
        print("Сохранение отчета...")
        save_analysis_report(df, 'results/analysis_report.txt')
        
        # Сохранение DataFrame в CSV для дальнейшего использования
        csv_file = 'results/logs_dataframe.csv'
        directory = os.path.dirname(csv_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"DataFrame сохранен в CSV: {csv_file}")
    
    else:
        print("Не удалось загрузить данные для анализа")


if __name__ == "__main__":
    main()