# nextion_easy

### Table of Contents

1. [Installation](#installation)
2. [Used](#used)
3. [Nextion programing](#nextion)

## Installation <a name="installation"></a>
pip3 install NextionEasy

## Used <a name="used"></a>
from NextionEasy.nextion_easy import Display<br/>
<br/>
Display.write("bt0", True) # установить состояние объекта кнопки bt0 в ON<br/>
<br/>
Display.read() # прочитать изменения с дисплея<br/>
/# Пример ответа: (bt0, False)<br/>
<br/>

## Nextion programing <a name="nextion"></a>
/# Пример программирвоания кнопки на дисплее Nextion
print "bt0="
print bt0.val
print "\r"