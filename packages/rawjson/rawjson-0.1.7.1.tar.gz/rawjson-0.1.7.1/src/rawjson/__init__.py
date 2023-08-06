__version__ = "0.1.7.1"

# from .exceptions import MessageNotFound
import json
from urllib.parse import unquote
class MessageNotFound(Exception): ...

class RawJSON:
    def __init__(self): self.__raw__ = {}

class Item:
    def __init__(self, id: str, count: int = None, tag: str = None) -> None:
        self.__raw__ = {'id': id}
        if count != None:
            self.__raw__['count'] = count
        if tag != None:
            self.__raw__['tag'] = tag

class Entity:
    def __init__(self, type: str, name: RawJSON = None, id: str = "0"):
        self.__raw__ = {"type": type, "id": id}
        if name != None:
            self.__raw__['name'] = name.forValue()

class HoverContent:
    def __init__(self):
        self.__raw__ = {}
    
    def setValue(self, value: RawJSON|Item|Entity):
        self.__raw__ = value.__raw__
        if isinstance(value, RawJSON):
            self.__raw__ = value.forValue()
        
        return self
                    

class RawJSON:
    def __init__(self, text: str):
        self.__raw__ = [{"text": text}]
        self.defaultIndex = 0

    def forValue(self):
        return self.__raw__[0]

    def __indexcheck__(self, index: int|None):
        index = self.defaultIndex if self.defaultIndex != None and index == None else index
        if len(self.__raw__) > index:
            if not self.__raw__[index]:
                raise MessageNotFound(f"Message with index {index} not found!")
        else:
            raise MessageNotFound(f"Message with index {index} not found!")
        return index
        
    def setDefaultIndex(self, index: int|None):
        self.defaultIndex = index
        
        return self

    def addMessage(self, text: str):
        self.__raw__.append({"text": text})

        return self

    def setText(self, text: str, index: int = None):
        index = self.__indexcheck__(index)
        self.__raw__[index]["text"] = text

        return self

    def setExtra(self, extra: list, index: int = None):
        index = self.__indexcheck__(index)
        self.__raw__[index]['extra'] = extra

        return self

    def appendExtra(self, extra: str, index: int = None):
        index = self.__indexcheck__(index)
        if 'extra' in self.__raw__[index]:
            self.__raw__[index]['extra'].append(extra)
        else:
            self.__raw__[index]['extra'] = [extra]

        return self

    def setColor(self, color: str, index: int = None):
        index = self.__indexcheck__(index)
        self.__raw__[index]["color"] = color

        return self

    def setFont(self, font: str, index: int = None):
        index = self.__indexcheck__(index)
        self.__raw__[index]['font'] = f'assets/{font}/font'

        return self

    def __setbool__(self, field: str, value: bool, index: int):
        self.__raw__[index][field] = value
        if not value and field in self.__raw__[index]:
            self.__raw__[index].pop(field)

        return self
    
    def setBold(self, bold: bool, index: int = None):
        index = self.__indexcheck__(index)
        self.__setbool__('bold', bold, index)

        return self

    def setItalic(self, italic: bool, index: int = None):
        index = self.__indexcheck__(index)
        self.__setbool__('italic', italic, index)

        return self

    def setUnderlined(self, underlined: bool, index: int = None):
        index = self.__indexcheck__(index)
        self.__setbool__('underlined', underlined, index)

        return self

    def setStrikethrough(self, strikethrough: bool, index: int = None):
        index = self.__indexcheck__(index)
        self.__setbool__('strikethrough', strikethrough, index)

        return self

    def setObfuscated(self, obfuscated: bool, index: int = None):
        index = self.__indexcheck__(index)
        self.__setbool__('obfuscated', obfuscated, index)

        return self

    def setInsertion(self, insertion: str, index: int = None):
        index = self.__indexcheck__(index)
        self.__setbool__('insertion', insertion, index)

        return self

    def addClickEvent(self, index: int = None):
        index = self.__indexcheck__(index)
        self.__raw__[index]['clickEvent'] = {}

        return self

    def removeClickEvent(self, index: int = None):
        index = self.__indexcheck__(index)
        if 'clickEvent' in self.__raw__[index]:
            self.__raw__[index].pop('clickEvent')

        return self


    def setClickAction(self, action: str, value: str, index: int = None):
        index = self.__indexcheck__(index)
        if 'clickEvent' not in self.__raw__[index]:
            self.addClickEvent(index)

        self.__raw__[index]['clickEvent']['action'] = action
        self.__raw__[index]['clickEvent']['value'] = value

        return self

    def addHoverEvent(self, index: int = None):
        index = self.__indexcheck__(index)
        self.__raw__[index]['hoverEvent'] = {}

        return self

    def removeHoverEvent(self, index: int = None):
        index = self.__indexcheck__(index)
        if 'hoverEvent' in self.__raw__[index]:
            self.__raw__[index].pop('hoverEvent')

        return self

    def setHoverAction(self, action: str, value: HoverContent, index: int = None):
        index = self.__indexcheck__(index)
        if 'hoverEvent' not in self.__raw__[index]:
            self.addHoverEvent(index)

        self.__raw__[index]['hoverEvent']['action'] = action
        self.__raw__[index]['hoverEvent']['contents'] = value.__raw__

        return self

    def toCommand(self, target: str):
        raw = unquote(str(self.__raw__)).replace("'", '"')
        return f'/tellraw {target} {raw}'
    
    def fromCommand(command: str):
        command_list = command.split(' ')
        for i in range(2):
            target = command_list.pop(0)
        return json.loads(" ".join(command_list))



if __name__ == "__main__":
    a = RawJSON('Привет, мир!').setHoverAction('show_text', HoverContent().setValue(RawJSON('Пока').setColor('yellow')))
    print(a.toCommand('@a'))
    print(RawJSON.fromCommand('/tellraw @s [{"text": "test"}, {"text": "test2"}]'))