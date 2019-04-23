
import xml.dom.minidom as md
import sys


try:
    DOMTree = md.parse("test.xml")
    collec = DOMTree.documentElement

    if collec.hasAttribute("name"):
        print("Root element : %s" % collec.getAttribute("name"))

    funcs = collec.getElementsByTagName("taci")

except:
    print("Error during the parsing of XML input, invalid XML input or file cannot be opened.", file=sys.stderr)
    exit(3)

a = 0
variables = {}
labels = {}
stack = []
callstack = []
pc = 0





while (len(funcs) > pc):
    global pc
    if funcs[pc].getAttribute("opcode") == "LABEL":

        dest = funcs[pc].getElementsByTagName('dst')

        if (len(dest) != 1):
            print("Semantic Error during the semantic checks.", pc + 1, file=sys.stderr)
            exit(5)

        try:
            dest = dest[0]
            data = dest.childNodes[0].data

        except:
            print("Semantic Error during the semantic checks.", pc + 1, file=sys.stderr)
            exit(5)

        if dest.childNodes[0].data in labels:
            print("Semantic Error during the semantic checks.", pc + 1, file=sys.stderr)
            exit(5)

        labels[dest.childNodes[0].data] = pc

    pc+=1

a = 0

def run():
    global pc
    read_labels()
    check_args()
    while pc < len(collec):
        op = collec[pc].attrib['opcode']
        if op == 'MOV':
            mov()
        elif op == 'ADD':
            add()
        elif op == 'SUB':
            sub()
        elif op == 'MUL':
            mul()
        elif op == 'DIV':
            div()
        elif op == 'READINT':
            read_int()
        elif op == 'PRINT':
            print_()
        elif op == 'LABEL':
            label()
        elif op == 'JUMP':
            jump()
        elif op == 'JUMPIFEQ':
            jumpifeq()
        elif op == 'JUMPIFGR':
            jumpifgr()
        elif op == 'CALL':
            call()
        elif op == 'RETURN':
            return_()
        elif op == 'PUSH':
            push()
        elif op == 'POP':
            pop()
        elif op == 'READSTR':
            readstr()
        elif op == 'CONCAT':
            concat()
        elif op == 'GETAT':
            getat()
        elif op == 'LEN':
            len()
        elif op == 'STRINT':
            strint()
        elif op == 'INTSTR':
            intstr()
        else:
            print('Semantic Error during the semantic checks: invalid operation.', file=sys.stderr)
            exit(5)
        pc = pc+1




def check_args():
    for n in collec:
        if len(n.attrib) > 3:
            print('Semantic Error during the semantic checks: more arguments than needed.', file=sys.stderr)
            exit(5)
        for arg in n:
            if arg.tag not in ['src1', 'src2', 'dst']:
                print("Semantic Error during the semantic checks: bad syntax for arguments.", file=sys.stderr)
                exit(5)
            elif arg.attrib['kind'] == 'variable' and not (
                    not arg.text[0].isdigit() and all(c.isalnum() or c == '_' for c in arg.text)):
                print('Semantic Error during the semantic checks: invalid variable name: ' + arg.text,
                      file=sys.stderr)
                exit(5)

def read_labels():
    for i in range(len(collec)):
        if collec[i].attrib['opcode'] == 'LABEL':
            if collec[i].find('dst').text in labels:
                print("Semantic Error during the semantic checks: label duplicated", file=sys.stderr)
                exit(5)
            elif collec[i].find('dst').attrib['kind'] != 'literal' or collec[i].find('dst').attrib['type'] != 'string':
                print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
                exit(14)
            else:
                labels[collec[i].find('dst').text] = i


def mov():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    src1 = collec[pc].getElementsByTagName('src1')

    if (len(dest) != 1 or len(src1) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)
    try:
        dest = dest.childNodes[0].data
        src1 = src1.childNodes[0].data

    except:
        print("Semantic Error during the semantic checks: Variable name or literal needed at instruction", pc + 1,
              file=sys.stderr)
        exit(5)

    sou1 = 0
    if (src1.hasAttribute("kind") and src1.getAttribute("kind") == "literal"):
        try:
            sou1 = int(src1.childNodes[0].data)
        except ValueError:
            sou1 = str(src1.childNodes[0].data)
    else:
        try:
            sou1 = variables[src1.childNodes[0].data][0]
        except KeyError:
            print("Run-time Error: Read access to non-defined or non-initialized variable at instruction", pc + 1,
                  file=sys.stderr)
            exit(11)

    try:
        variables[dest.childNodes[0].data] = [sou1, type(sou1)]
    except:
        print("Semantic Error", pc + 1, file=sys.stderr)
        exit(5)

def add():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')

    if (len(dest) != 1 or len(src1) != 1 or len(src2) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)


    sou1 = 0
    if (src1.hasAttribute("kind") and src1.getAttribute("kind") == "literal"):

        sou1 = int(src1.childNodes[0].data)


    sou2 = 0
    if (src2.hasAttribute("kind") and src2.getAttribute("kind") == "literal"):
        sou2 = int(src2.childNodes[0].data)

    res = sou1 + sou2

    try:
        variables[dest.childNodes[0].data] = [res, type(res)]
    except:
        print("Semantic Error", pc + 1, file=sys.stderr)
        exit(5)



    #TODO fill up the error codes

def sub():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')

    if (len(dest) != 1 or len(src1) != 1 or len(src2) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    sou1 = 0
    if (src1.hasAttribute("kind") and src1.getAttribute("kind") == "literal"):
        try:
            sou1 = int(src1.childNodes[0].data)
        except ValueError:
            sou1 = str(src1.childNodes[0].data)

    sou2 = 0
    if (src2.hasAttribute("kind") and src2.getAttribute("kind") == "literal"):
        try:
            sou2 = int(src2.childNodes[0].data)
        except ValueError:
            sou2 = str(src2.childNodes[0].data)

    res = sou1 - sou2

    try:
        variables[dest.childNodes[0].data] = [res, type(res)]
    except:
        print("Semantic Error", pc + 1, file=sys.stderr)
        exit(5)

    pc += 1

    #TODO fill up the error codes

def mul():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')

    if (len(dest) != 1 or len(src1) != 1 or len(src2) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    sou1 = 0
    if (src1.hasAttribute("kind") and src1.getAttribute("kind") == "literal"):
        try:
            sou1 = int(src1.childNodes[0].data)
        except ValueError:
            sou1 = str(src1.childNodes[0].data)

    sou2 = 0
    if (src2.hasAttribute("kind") and src2.getAttribute("kind") == "literal"):
        try:
            sou2 = int(src2.childNodes[0].data)
        except ValueError:
            sou2 = str(src2.childNodes[0].data)

    res = sou1 * sou2

    try:
        variables[dest.childNodes[0].data] = [res, type(res)]
    except:
        print("Semantic Error", pc + 1, file=sys.stderr)
        exit(5)

    pc = pc + 1

    # TODO fill up the error codes

def div():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')

    if (len(dest) != 1 or len(src1) != 1 or len(src2) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    if (src1.hasAttribute("kind") and src1.getAttribute("kind") == "literal"):
        try:
            sou1 = int(src1.childNodes[0].data)
        except ValueError:
            sou1 = str(src1.childNodes[0].data)

    if (src2.hasAttribute("kind") and src2.getAttribute("kind") == "literal"):
        try:
            sou2 = int(src2.childNodes[0].data)
        except ValueError:
            sou2 = str(src2.childNodes[0].data)

    try:
        res = sou1 / sou2
    except ZeroDivisionError:
        print("Run-time Error: Division by zero using DIV instruction at instruction", pc + 1, file=sys.stderr)
        exit(12)


    variables[dest.childNodes[0].data] = [res, type(res)]

    pc += 1

    # TODO fill up the error codes
    # TODO zero check? type error? (float - int conflict?)

def read_int():
    global pc
    dest = collec[pc].getElementsByTagName('dst')

    if (len(dest) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    try:
        res = int(input())
    except ValueError:
        print("Run-time Error: READINT got invalid value (not an integer).", pc + 1, file=sys.stderr)
        exit(14)

    variables[dest.childNodes[0].data] = [res, type(res)]
    pc += 1

def print_():
    global pc
    src1 = collec[pc].getElementsByTagName('src1')

    if (len(src1) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    print(src1.childNodes[0].data)
    pc += 1

def label():
    global pc

    dest = collec[pc].getElementsByTagName('dst')

    labels[dest.childNodes[0].data] = pc

    pc += 1

def jump():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    if (len(dest) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)
    pc = labels[dest.childNodes[0].data]

def jumpifeq():
    global pc
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')

    if (len(src1) != 1 or len(src2) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    if src1 == src2:
        pc = labels[dest.childNodes[0].data]

def jumpifgr():
    global pc
    dest = collec[pc].getElementsByTagName('dst')
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')

    if (len(dest) != 1 or len(src1) != 1 or len(src2) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    if src1 > src2:
        pc = labels[dest.childNodes[0].data]

def call():
    global pc
    dest = collec[pc].getElementsByTagName('dst')

    if (len(dest) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    callstack.append(pc)
    pc = labels[dest.childNodes[0].data]

def return_():
    global pc
    try:
        pc = callstack.pop()
    except IndexError:
        print("Run-time Error: Pop from the empty (data/call) stack is forbidden.", file=sys.stderr)
        exit(15)

def pop():
    global pc
    dest = collec[pc].getElementsByTagName('dst')

    if (len(dest) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    try:
        res = stack.pop()
    except IndexError:
        print("Run-time Error: Pop from the empty (data/call) stack is forbidden.", file=sys.stderr)
        exit(15)

    variables[dest.childNodes[0].data] = [res, type(res)]
    pc += 1

def push():
    global pc
    src1 = collec[pc].getElementsByTagName('src1')

    if (len(src1) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    stack.append(src1.childNodes[0].data)
    pc += 1

def readstr():
    global pc
    dest = collec[pc].getElementsByTagName('dst')

    if (len(dest) != 1):
        print("Semantic Error during the semantic checks: Bad syntax at instruction", pc + 1, file=sys.stderr)
        exit(5)

    res = input("Enter input = ")
    variables[dest.childNodes[0].data] = [res, type(res)]

    pc += 1

def concat():
    global pc
    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')
    dest = collec[pc].getElementsByTagName('dst')
    if src1.getAttribute['type'] == src2.getAttribute['type'] and src1.getAttribute['type'] == 'string' and dest.getAttribute['kind'] == 'variable':
        d1 = src1.childNodes[0].data
        d2 = src2.childNodes[0].data

        variables[dest.childNodes[0].data] = d1 + d2
    else:
        print('Run-time Error: Operands of incompatible type.', file=sys.stderr)
        exit(14)

def strint():
    global pc

    src1 = collec[pc].getElementsByTagName('src1')
    dest = collec[pc].getElementsByTagName('dst')

    if src1.getAttribute['type'] == 'string' and dest.getAttribute['type'] == 'integer' and \
            dest.getAttribute['kind'] == 'variable':
        try:
            variables[dest] = int(src1.childNodes[0].data)
        except ValueError:
            print("Run-time Error: Invalid literal for a integer", file=sys.stderr)
            exit(20)
    else:
        print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
        exit(14)

    pc += 1

def intstr():
    global pc
    src1 = collec[pc].getElementsByTagName('src1')
    dest = collec[pc].getElementsByTagName('dst')

    if src1.getAttribute['type'] == 'integer' and dest.getAttribute['type'] == 'string' and \
            dest.getAttribute['kind'] == 'variable':
        variables[dest] = str(src1.childNodes[0].data)
    else:
        print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
        exit(14)

    pc += 1

def getat():
    global pc

    src1 = collec[pc].getElementsByTagName('src1')
    src2 = collec[pc].getElementsByTagName('src2')
    dest = collec[pc].getElementsByTagName('dst')

    if src1.getAttribute['type'] == 'string' and src2.getAttribute['type'] == 'integer' and \
            dest.getAttribute['kind'] == 'variable':
        d1 = src1.childNodes[0].data
        d2 = src2.childNodes[0].data
        try:
            variables[dest] = d1[d2]
        except IndexError:
            print("Run-time Error: Index out of bounds.", file=sys.stderr)
            exit(20)
    else:
        print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
        exit(14)

def len():
    global pc

    src1 = collec[pc].getElementsByTagName('src1')
    dest = collec[pc].getElementsByTagName('dst')


    if src1.getAttribute['type'] == 'string' and dest.getAttribute['type'] == 'integer' and \
            dest.getAttribute['kind'] == 'variable':
        variables[dest] = len(src1.childNodes[0].data)
    else:
        print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
        exit(14)




































