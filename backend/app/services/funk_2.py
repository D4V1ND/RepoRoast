"""
Aufgabe: 
Bereite eine Funktion (foo) vor, die als Argument einen Str 
und eine Liste von Strings erhält.
Die Funktion gibt einen neuen String zurück, 
in dem der Inhalt des ersten Arguments zwischen die Elemente
der Liste eingefügt wird.

Bsp: 
foo("?", ['felix', 'ist', 'nett'])
=> 'felix?ist?nett'
"""

def foo(phrase: str, words): 
    new_word = words[0]

    for elem in words[1:]:
        new_word += phrase 
        new_word += elem 
    
    return new_word

"""
a % b = 0 heisst dass a durch b teilbar ist.
Aufgabe: Die sollte erst überprüfen, 
ob die Division durchgeführt werden kann. 
Die Funktion soll danach zurückgeben,
ob die Zahl durch den Divisor teilbar ist.
"""
def teilbar(zahl, divisor):
    if divisor == 0: 
        return "Man kann nicht durch 0 teilen."
    elif zahl % divisor == 0: 
        return f"Die Zahl {zahl} ist durch {divisor} teilbar."
    else: 
        return f"Die Zahl {zahl} ist NICHT durch {divisor} teilbar."
    
print(teilbar(10, 3))

# Type Hinting

def sum(a1: int, a2: int) -> int: 
    print(a1+a2)

sum("hallo ", "welt")

def rechteck(a: float, b: float): 
    umfang = 2*a + 2*b 
    return umfang

"""
Aufgabe: 
Bereite eine Funktion vor, die eine Liste als Argument erhält, 
in der Duplikate vorkommen können
und eine Liste mit einzigartigen Elementen zurückgibt. 
Bsp: check_duplicate([1, 2, 3, 3, 3, 5, 5]) => [1, 2, 3, 5]
"""



def check_duplicate(liste):
    new_list = []
    for elem in liste: 
        if elem not in new_list: 
            new_list.append(elem)
    return new_list



print(check_duplicate([1, 2, 3, 3, 3, 5, 5]))