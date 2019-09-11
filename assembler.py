import sys

command_types = {'ADD':'R', 'SUB':'R', 'AND':'R', 'OR':'R', 'XOR':'R',
                 'ADDI':'I', 'ANDI':'I', 'ORI':'I', 'XORI':'I',
                 'SLL':'R', 'SRL':'R','SRA':'R',
                 'SLLI':'IS', 'SRLI':'IS', 'SRAI':'IS',
                 'SLT':'R', 'SLTU':'R', 'SLTI':'I',
                 'SLTIU':'I', 'LUI':'U', 'AUIPC':'U',
                 'JAL':'J', 'JALR':'I', 'BEQ':'B', 'BNE':'B',
                 'BLT':'B', 'BGE':'B','BLTU':'B','BGEU':'B',
                 'LB':'I', 'LH':'I', 'LW':'I', 'LBU':'I','LHU':'I',
                 'SB':'S', 'SH':'S', 'SW':'S',
                 'NOP':'C', 'CONST':'C', 'NONE':'C'}

command_bits = {'ADD':[51,0,0], 'SUB':[51,0,32],
                'AND':[51,7,0], 'OR':[51,6,0], 'XOR':[51,4,0],
                'ADDI':[19,0], 'ANDI':[19,7], 'ORI':[19,6], 'XORI':[19,4],
                'SLL':[51,1,0], 'SRL':[51,5,0], 'SRA':[51,5,32],
                'SLLI':[19,1,0], 'SRLI':[19,5,0], 'SRAI':[19,5,32],
                'SLT':[51,2,0], 'SLTU':[51,3,0], 'SLTI':[19,2,0], 'SLTIU':[19,3,0],
                'LUI':[55], 'AUIPC':[23],
                'JAL':[111], 'JALR':[103,0], 'BEQ':[99,0], 'BNE':[99,1],
                'BLT':[99,4], 'BGE':[99,5], 'BLTU':[99,6], 'BGEU':[99,7],
                'LB':[3,0], 'LH':[3,1], 'LW':[3,2], 'LBU':[3,4], 'LHU':[3,5],
                'SB':[35,0], 'SH':[35,1], 'SW':[35,2],
                'NOP':[19], 'CONST':[], 'NONE':[]}

command_format = {'R':[('r',5), ('f',3), ('r',5), ('r',5), ('f',7)],
                  'I':[('r',5), ('f',3), ('r',5), ('i',12)],
                  'IS':[('r',5), ('f',3), ('r',5), ('i',5), ('f',7)],
                  'S':[('i',5), ('f',3), ('r',5), ('r',5), ('i',7)],
                  'B':[('i',5), ('f',3), ('r',5), ('r',5), ('i',7)],
                  'U':[('r',5), ('i',20)],
                  'J':[('r',5), ('i',20)],
                  'C':['i',32]}

immediate_order = {'I':list(range(12)),
                   'IS':list(range(5)),
                   'S':list(range(12)),
                   'B':[10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11],
                   'U':list(range(20)),
                   'J':[11, 12, 13, 14, 15, 16, 17, 18, 10, 0,
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 19],
                   'C':list(range(32))}

def main():
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().split('\n')
    try:
        lines.reverse()
        lines.remove('')
    except ValueError:
        pass
    finally:
        lines.reverse()
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if l and not l[0] == '#']
    lines = [l.split(' ') for l in lines if l]
    lines = [[w for w in l if w] for l in lines]

    code = []
    human_readable = []
    print('DEC\t HEX\tINSTR\t  CODE')

    for l in lines:
        print(l)
        if l[0] == 'CONST':
            newline = hex(int(l[1]))[2:]
            code.append(newline)
            human_readable.append([l[0], newline])
            continue
        elif l[0] == 'NOP':
            for i in range(int(l[1])):
                newline = hex(command_bits['NOP'][0])[2:]
                code.append(newline)
                human_readable.append([l[0], newline])
            continue
        elif l[0] == 'NONE':
            for i in range(int(l[1])):
                newline = '0'
                code.append(newline)
                human_readable.append([l[0], newline])
            continue
        try:
            form_name = command_types[l[0]]
        except KeyError:
            print('Command "' + l[0] + '" not found!')
            raise

        bits = command_bits[l[0]]

        form = command_format[form_name]

        order = []
        if not form_name == 'R':
            order = immediate_order[form_name]
            i_len = 0
            for element in form:
                if element[0] == 'i':
                    i_len += element[1]
            imm_bin = bin(int(l[-1]) & (2**i_len - 1))[2:]
            imm_bin = imm_bin.zfill(i_len)[::-1]
            imm_bin = ''.join(
                [imm_bin[order[i]] for i in reversed(range(len(imm_bin)))])
        command = [bin(bits[0])[2:].zfill(7)]

        i_l = 1
        i_bits = 1
        for element in form:
            print(element)

            if element[0] == 'r':
                length = element[1]
                str_bits = bin(int(l[i_l])%32)[2:]
                str_bits = str_bits.zfill(length)
                command.append(str_bits)
                print('r:')
                print('i_l:l[i_l]: ' + str(i_l) + ':' + str(l[i_l]))
                i_l += 1
            elif element[0] == 'f':
                length = element[1]
                str_bits = bin(bits[i_bits])[2:]
                str_bits = str_bits.zfill(length)
                command.append(str_bits)
                print('i_bits:bits[i_bits]: ' + str(i_bits) + ':' + str(bits[i_bits]))
                i_bits += 1
            elif element[0] == 'i':
                length = element[1]
                imm = imm_bin[len(imm_bin) - length:]
                imm_bin = imm_bin[:-length]
                print(imm)
                command.append(imm)
        print(command)

        command = '0b' + ''.join(reversed(command))

        command = hex(int(command,2))[2:]

        code.append(command)
        human_readable.append([l[0], command])
    for i,h in enumerate(human_readable):
        print(str(i).zfill(3) + '\t0x' + hex(i).upper()[2:].zfill(3) + '\t'
              + h[0].upper().rjust(5) + '\t' + h[1].upper().zfill(8))

    filename = 'a.hex'
    if len(sys.argv) >= 3:
        filename = sys.argv[2]
    with open(filename,'w') as f:
        f.write('v2.0 raw\n')
        for l in code:
            f.write(l)
            f.write('\n')
            f.write('0\n')
    l = len(code)
    print(str(l) + ' = ' + str(hex(l)) + ' program lines written!')

if __name__ == '__main__':
    main()
