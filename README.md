# ASCII Art
Автор: Сычев Иван Валерьевич ФТ-104-2

## Описание
Консольная утилита и приложение с графическим интерфейсом, преобразующие обычную картинку в ASCII Art.
### Консольная утилита
На вход подается путь до изображения для ASCII Art.
Можно вывести ASCII Art на консоль или записать его в файл.
Также есть возможность указать ширину, высоту и символы ASCII Art.
Если ввести что-то одно (ширину или высоту), второе посчитается автоматически,
на основе соотношения сторон изображения.

Дополнительная информация в help по команде: `python -m cli.ascii_art -h`

### Приложение с графическим интерфейсом
Графический интерфейс встречает пользователя одной кнопкой `Выбрать картинку`.
Выбор происходит в диалоговом окне.
Далее после выбора, отрисовывается картинка и появляется кнопка `Сделать ASCII Art`.
Нажав на нее, появляется диалоговое окно, где можно указать параметры ASCII Art: символы, ширину, высоту.
Если ввести что-то одно (ширину или высоту), второе посчитается автоматически,
на основе соотношения сторон изображения.
После нажатия кнопки `Подтвердить` в диалоговом окне, то на главном окне появится ASCII Art и
две кнопки: скопировать в буфер обмена, сохранить в файл. Выбор пути для сохранения в файл происходит в
диалоговом окне.
Далее можно повторить все сначала.

## Требования
* Использование библиотеки PyQt5 для графического интерфейса
* Использование любой библиотеки для работы с изображениями, которая раскладывает изображение на 3 матрицы
* Не использовать библиотеки для работы с матрицами
* Соблюдать паттерн MVC

## Состав
* Запуск консольной утилиты из `ascii-art` командой `python -m cli.ascii_art`
* Запуск приложения с графическим интерфейсом из `gui/ascii_art.py`
* Работа с изображениями: `model/image.py`
* Конвертация в ASCII Art: `model/ascii_art_converter.py`
* Запись файлов: `model/utils.py`
* Контроллер для консольной утилиты: `controllers/cli_controller.py`
* Контроллер для приложения с графическим интерфейсом: `controllers/gui_controller.py`

## Примеры верных команд для консольной утилиты

python -m cli.ascii_art -h

python -m cli.ascii_art `IMAGE_PATH`

python -m cli.ascii_art `IMAGE_PATH` -op `OUT_PATH`

python -m cli.ascii_art `IMAGE_PATH` -c

python -m cli.ascii_art `IMAGE_PATH` -c -w 100

python -m cli.ascii_art `IMAGE_PATH` -c -w 100 -he 100

python -m cli.ascii_art `IMAGE_PATH` -c -w 100 -ch /@*
