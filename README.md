# Прогноз погоды по маршруту

Этот проект предоставляет возможность построить маршрут с прогнозом погоды для выбранных городов. Вы можете указать начальный и конечный пункты, добавить промежуточные города, а также выбрать количество дней для прогноза.

## Функциональность

- Ввод начального, конечного и промежуточных пунктов маршрута.
- Выбор количества дней для прогноза.
- Отображение:
  - Графиков изменения погодных параметров (температура, скорость ветра, вероятность осадков).
  - Маршрута на карте с указанием температуры в каждой точке.

---

## Скриншоты

### Форма ввода маршрута

<img width="1440" alt="Снимок экрана 2024-12-23 в 23 55 01" src="https://github.com/user-attachments/assets/399a67c5-ef89-42b4-8b4a-e80271b0b15e" />

### Прогноз погоды и маршрут

<img width="1440" alt="Снимок экрана 2024-12-23 в 23 55 11" src="https://github.com/user-attachments/assets/7471c4e1-2d09-4ca1-870b-5524a8e1d092" />

---

## Ответы на вопросы

### 1. Какие графики лучше всего подходят для визуализации погодных данных? Объясни свой выбор.

Для визуализации погодных данных наиболее эффективны следующие типы графиков:

- **Линейные графики (line charts)**:
  - Эти графики отлично подходят для отображения изменений погодных параметров во времени (например, температуры или вероятности осадков).
  - Линии помогают увидеть тренды и аномалии, такие как резкие изменения температуры.
  - Использование точек на линиях (markers) помогает пользователю сфокусироваться на конкретных данных.


- **Карта маршрута с данными (map visualizations)**:
  - Карты помогают пользователям видеть погодные условия в разных точках маршрута, что полезно для планирования поездок.
  - Интерактивные карты с текстовыми аннотациями позволяют узнать данные о температуре, ветре и осадках для каждой точки.

Объединение этих графиков делает проект более информативным и удобным для пользователя.

### 2. Как можно улучшить пользовательский опыт с помощью интерактивных графиков?

Интерактивные графики позволяют пользователю более эффективно взаимодействовать с данными. Возможные улучшения включают:

1. **Всплывающие подсказки (tooltips)**:
   - Показывают подробную информацию о конкретной точке данных (например, дата, температура, вероятность осадков) при наведении мыши.
   - Это упрощает анализ данных без необходимости изучения всего графика.

2. **Фильтры и переключатели**:
   - Позволяют пользователям выбрать, какой параметр отображать (например, температуру, скорость ветра или осадки).
   - Можно добавить возможность фильтровать данные по времени, чтобы сфокусироваться на конкретных днях маршрута.

3. **Масштабирование и перемещение (zoom and pan)**:
   - Позволяет пользователю увеличивать масштаб графиков для детального анализа данных и перемещаться по времени.

4. **Сравнение параметров**:
   - Добавление возможности накладывать несколько графиков друг на друга для сравнения параметров, таких как температура и скорость ветра.

5. **Анимация данных**:
   - Анимация изменений погоды с течением времени помогает визуализировать, как параметры меняются вдоль маршрута.

Эти улучшения сделают проект более удобным и полезным для конечных пользователей.

---

## Установка и запуск

### 1. Установка зависимостей
Убедитесь, что у вас установлен Python (версии 3.7 и выше). Затем установите зависимости:
```bash
pip install -r requirements.txt
```

### 2. Запуск приложения
Выполните следующую команду, чтобы запустить Flask-сервер:
```bash
python app.py
```

### 3. Использование
Откройте браузер и перейдите по адресу:
```
http://127.0.0.1:5000
```

---

## Автор

Проект создал Тюрин Антон.
