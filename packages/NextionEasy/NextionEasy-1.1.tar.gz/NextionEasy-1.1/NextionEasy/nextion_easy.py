from serial import Serial

class Display:
    command_failed_codes = {
        0x02: "Component ID invalid",
        0x03: "Page ID invalid",
        0x04: "Picture ID invalid",
        0x05: "Font ID invalid",
        0x11: "Baud rate setting invalid",
        0x12: "Curve control ID number or channel number is invalid",
        0x1A: "Variable name invalid",
        0x1B: "Variable operation invalid",
        0x1C: "Failed to assign",
        0x1D: "Operate EEPROM failed",
        0x1E: "Parameter quantity invalid",
        0x1F: "IO operation failed",
        0x20: "Undefined escape characters",
        0x23: "Too long variable name",
    }

    """serial  -  устройство передачи данных
    on  -  Байт/Строка объекта во включённом состоянии"""

    def __init__(self, serial="/dev/ttyS0", on=b"\x01") -> None:
        self.serial = Serial(serial)
        self.on = on

    def write(self, key: str, value, types: str="val") -> None:
        """key  -  Объект изменения
    value  -  Новое значение объекта
    types=val/txt/color  -  Тип значения

    Пример: write("bt0", 0) # Выключен объект bt0

    Пример: write("t0", "Answer?", "txt") # Текст заменён на "Answer?" у объекта t0"""

        if types == "val":
            data = f"{key}.val={value}"
        else:
            data = f"{key}.{types}=\"{value}\""

        self.serial.write(data.encode("utf-8")+b"\xFF\xFF\xFF")

    def read(self):
        """Возвращает tuple[key, value] или None если нет данных
        Пример данных отправляемых кнопкой bt0:
                                                    print "bt0="
                                                    print bt0.val
                                                    print "\\r" """

        buff = self.serial.readline()
        if not buff:
            return
        for i in self.command_failed_codes:
            if i not in buff: continue
            print(f"Error byte [{i}]: {self.command_failed_codes[i]}")
        buff = buff.split(b"=")
        return (buff[0].decode("utf-8", errors="ignore"), self.on in buff[1])

    #def rgb_to_hmi(self, r: int, g: int, b: int, a: int=255) -> str:
    #    """Перевод RGBA в формат HMI для дисплея Nextion"""

    #    h = round((180 / 255) * ((max(r, g, b) + min(r, g, b)) / 2 - min(r, g, b)))
    #    s = round((255 / max(r, g, b)) * (max(r, g, b) - min(r, g, b)))
    #    v = round((255 / max(r, g, b)) * max(r, g, b))
    #    a = round((255 / 255) * a)

    #    hmi = (h << 16) | (s << 8) | v | (a << 24)

    #    return f"{hmi:08X}"