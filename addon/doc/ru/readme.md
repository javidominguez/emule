# eMule 0.50A #

*	Авторы: Noelia, Chris, Alberto.
*	загрузить [стабильную версию][1]
*	загрузить [разрабатываемую версию][3]

Дополнение позволяет улучшить доступность eMule в NVDA. Также предоставляет
дополнительные клавиатурные команды для перемещения между окнами и даёт
полезную информацию об eMule.

Оно основано на  дополнении eMuleNVDASupport того же автора. Вы должны
удалить его старую копию перед использованием этой, потому что оба имеют
общие функции и комбинации клавиш.

Проверено на [eMule][2] 0.50a.

## Основные команды: ##

*	control+shift+h: перемещение фокуса и мыши к главной панели инструментов.
*	control+shift+t: Чтение текущего окна.
*	control+shift+n: Перемещение фокуса на поле Имя в окне поиска.
*	control+shift+p: В окне поиска, перемещает фокус и мышь в список
  параметров поиска или в поле редактирования вариантов.
*	control+shift+b: Перемещение фокуса в список результатов в окне поиска.
*	control+shift+z: перемещает фокус и мышь в  контекстную панель
  инструментов. По ней можно перемещаться с помощью клавиши TAB.
*	control+shift+o: Перемещает фокус в окно полученных сообщений IRC.
*	control+NVDA+f: Если курсор находится в поле редактирования только для
  чтения, откроет диалог поиска.
*	control+f3: Поиск следующего вхождения текста, который вы ранее искали в
  полях редактирования только для чтения.
*	control+shift+f3: Поиск предыдущего вхождения текста, который вы ранее
  искали в полях редактирования только для чтения.
*	control+shift+l: Перемещение объекта навигатора и мыши к заголовкам
  текущего списка.
*	control+shift+q: Читает первый объект в строке состояния; предоставляет
  информацию о последних действиях.
*	control+shift+w: Читает второй объект в строке состояния; содержит
  информацию о файлах и пользователях на текущем сервере.
*	control+shift+e: Читает третий объект строки состояния; полезно знать
  скорость загрузки / выгрузки.
*	control+shift+r: Читает четвёртый объект строки состояния; отчеты о
  подключении к eD2K и Kad сетям.
*	NVDA+control+shift+h: Открывает документацию. Если она не доступна на
  вашем языке по умолчанию, откроет на английском.

## Управление столбцами. ##

Находясь в списке, можно перемещать курсор между строк и столбцов с помощью
alt+ctrl+ стрелок. Следующие команды клавиш здесь также доступны:

*	nvda+control+1-0: читает первые 10 столбцов.
*	nvda+shift+1-0: читает столбцы с 11 по 20.
*	nvda+shift+C: копирует содержимое последнего прочитанного столбца в буфер
  обмена.

## Изменения в версии 1.1 ##
*	 Исправлена ошибка элемента меню eMule в пункте меню помощи NVDA, когда
   имя папки конфигурации Пользователя содержит не латинские буквы.
*	 Горячие клавиши могут теперь быть переназначены с помощью диалога жестов
   ввода NVDA.

## Изменения в версии 1.0 ##
*	 Начальная версия.

[[!tag dev stable]]

[1]: http://addons.nvda-project.org/files/get.php?file=em

[2]: http://www.emule-project.net

[3]: http://addons.nvda-project.org/files/get.php?file=em-dev