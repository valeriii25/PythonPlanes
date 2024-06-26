# Проект, реализующий API для системы авиарейсов
## Инструментарий
- Модели описаны с помощью `pydantic`
- Вебсервис реализован через `fastapi`
- Работа с базой даннфх `SQLite` осуществлялась через `SQLAlchemy`
> [!IMPORTANT]
> Запуск приложения осуществляется командой `fastapi run`
## Описание проекта
 Создан класс Plane для представления самолета, включающий следующие атрибуты:
   - Идентификатор самолета.
   - Модель самолета.
   - Максимальная вместимость пассажиров.
   - Максимальная дальность полета.
   - Текущий объем топлива.
   - Расход топлива (единица топлива на единицу расстояния, в которой дана дальность полета).

Создан класс Flight для представления авиарейса, включающий следующие атрибуты:
   - Идентификатор рейса.
   - Начальный аэропорт.
   - Конечный аэропорт.
   - Дальность полета.
   - Количество пассажиров.
   - Список самолетов, выполняющих данный рейс (самолет должен подходить по дальности, вместимости и количеству топлива, необходимого на рейс).

Разработана система авиарейсов и проведен анализ данных о самолетах:
   - Созданы функции для добавления нового самолета/рейса в систему.
   - Созданы функции для редактирования самолета/рейса в системе.
   - Созданы функции для удаления самолета/рейса из системы.
   - Созданы функции для получения всей информации о всех самолетах/рейсах в системе.
   - Реализованы функции для поиска доступных самолетов для рейсов с учетом вместимости пассажиров и дальности полета.
   - Реализованы функции для вычисления средней вместимости пассажиров и средней дальности полета среди всех самолетов в системе.
   - Разработаны функции для определения самого загруженного самолета (с наибольшим количеством пассажиров) и самого экономичного (с наибольшей дальностью полета на одном баке топлива).
   - Реализована функция для сохранения всей информации о самолетах и рейсах в JSON файл.
