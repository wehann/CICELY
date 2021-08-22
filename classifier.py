import gdb
import sys

class Classifier(gdb.Command):
    def __init__(self):
        super(self.__class__, self).__init__("classify", gdb.COMMAND_USER)

    def get_lib_address(self, libs_result):
        start_codes, end_codes, libs_name = [], [], []
        libs_address = {}
        for line in libs_result.split('\n'):
            if ' /' not in line or '0x' not in line:
                continue
            libs = line.split('0x')
            lib_start_code = '0x'
            for c in libs[1]:
                if c >= '0' and c <= 'f':
                    lib_start_code += c
                else:
                    break
            lib_end_code = '0x'
            for c in libs[2]:
                if c >= '0' and c <= 'f':
                    lib_end_code += c
                else:
                    break
            lib_file_path = '/' + line.split(' /')[1].split('\x1b')[0]
            if not lib_file_path.startswith('/home/'):
                continue
            if lib_file_path in libs_address.keys():
                libs_address[lib_file_path].append(lib_start_code + '-' + lib_end_code)
            else:
                libs_address[lib_file_path] = [lib_start_code + '-' + lib_end_code]
            start_codes.append(lib_start_code)
            end_codes.append(lib_end_code)
            libs_name.append(lib_file_path)
        return libs_address, start_codes, end_codes, libs_name

    def is_in_range(self, asm_address, start_codes, end_codes):
        for i in range(len(start_codes)):
            start = start_codes[i]
            end = end_codes[i]
            if (int(asm_address, 16) >= int(start, 16) and int(asm_address, 16) <= int(end, 16)):
                return i
        return -1

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 7:
            raise gdb.GdbError('输入参数数目不对')
        binary_file_path = argv[0]
        input_file_path = argv[1]
        parameters_1, parameters_2 = argv[2], argv[3]
        start_code, end_code = argv[4], argv[5]
        log_file_path = argv[6]

        gdb.execute('file ' + binary_file_path, to_string=True)
        gdb.execute('run ' + parameters_1.replace('_', ' ') + ' ' + input_file_path + ' ' + parameters_2.replace('_', ' '), to_string=True)
        libs_result = gdb.execute('libs', to_string=True)
        libs_address, start_codes, end_codes, libs_name = self.get_lib_address(libs_result)
        libs_address['self'] = [start_code + '-' + end_code]
        start_codes.append(start_code)
        end_codes.append(end_code)
        libs_name.append('self')
        asm_ins = gdb.execute('x/i $pc', to_string=True).replace('=> ', '')
        asm_address = asm_ins.split(' ')[0]
        while self.is_in_range(asm_address, start_codes, end_codes) == -1:
            gdb.execute('up 1', to_string=True)
            asm_ins = gdb.execute('x/i $pc', to_string=True).replace('=> ', '')
            asm_address = asm_ins.split(' ')[0]
            if ':' in asm_address:
                asm_address = asm_address[:asm_address.index(':')]
        lib_name = libs_name[self.is_in_range(asm_address, start_codes, end_codes)]
        with open(log_file_path, 'a') as f:
            f.write(binary_file_path + '\t' + input_file_path + '\t' + asm_ins.replace('\t', ' ').replace('\n', '') + '\t' +
                    lib_name + '\n')
        gdb.execute('quit')
        sys.exit()


if __name__ == '__main__':
    Classifier()

