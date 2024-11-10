# Лабораторная работа №4: Изучение корреляционных свойств последовательностей, используемых для синхронизации в сетях мобильной связи. 

## Цель работы

Получить представление о том, какие существуют псевдослучайные двоичные последовательности, какими корреляционными свойствами они обладают и как используются для синхронизации приемников и передатчиков в сетях мобильной связи.

## Реализация

Программа реализована на языке C++.

### Генерация последовательностей Голда

Функция `gen_gold_seq` генерирует последовательность Голда, принимая на вход начальные состояния регистров сдвига,  порождающие полиномы в двоичном формате.  В случае низкой автокорреляции, функция корректирует порождающие полиномы для получения более оптимальной последовательности.

### Вычисление корреляции

Функции `autocorr_check`, `autocorr`, `corr_print`, `correlation` и `normalized_correlation` реализуют вычисление автокорреляции и взаимной корреляции последовательностей.

## Результаты

Результаты работы программы C++ совпадают с результатами, полученными в MATLAB программе.  График автокорреляции, построенный в Matlab, демонстрирует ожидаемое поведение: острый пик при нулевом сдвиге и низкие значения при других сдвигах.

## Заключение

В ходе выполнения лабораторной работы были успешно решены поставленные задачи. Были получены практические навыки генерации и анализа ПСП, а также понимание их применения в системах мобильной связи.