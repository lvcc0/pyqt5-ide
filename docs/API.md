# pyqt5-ide interpreter API

Файл с разрешением ***\*.py*** должен находиться в директории ***interpreters***.

### Должен иметь в себе:
<table>
  <tr>
    <td>Класс <b>Interpreter</b></td>
    <td>Основной класс с главными функциями</td>
  </tr>
  <tr>
    <td>Функция <b>run(code, con)</b> в классе <b>Interpreter</b></td>
    <td>Функция, исполняющаяся при запуске написанного кода <i>(code)</i>, для вывода использующая <i>(con)</i></td>
  </tr>
</table>

### У объекта <i>(con)</i> имеются функции:
<table>
  <tr>
    <td><b>print(arg)</b></td>
    <td>Вывод аргумента <i>(arg)</i></td>
  </tr>
</table>

### [Пример интерпретатора](../interpreters/example.py)
