# move.py
# 1. 导入gdb模块来访问gdb提供的python接口
import gdb
import sys


# 2. 用户自定义命令需要继承自gdb.Command类
class Dis(gdb.Command):
    # 3. docstring里面的文本是不是很眼熟？gdb会提取该类的__doc__属性作为对应命令的文档
    """Move breakpoint
    Usage: mv old_breakpoint_num new_breakpoint
    Example:
        (gdb) mv 1 binary_search -- move breakpoint 1 to `b binary_search`
    """

    def __init__(self):
        # 4. 在构造函数中注册该命令的名字
        super(self.__class__, self).__init__("mv", gdb.COMMAND_USER)


    def get_lib_address(self, libs_result):
        start_codes, end_codes, libs_name = [], [], []
        libs_address = {}
        # with open('libs.txt', 'a') as f:
        #     f.write(libs_result + '\n----------------------\n')
        for line in libs_result.split('\n'):
            if ' /' not in line:
                continue
            # with open('libs.txt', 'a') as f:
            #     f.write(line + '\n1')
            # with open('libs.txt', 'a') as f:
            #     f.write(str(line.split('/')) + '\n2')
            # with open('libs.txt', 'a') as f:
            #     f.write(str(line.split(' /')) + '\n3')
            # with open('libs.txt', 'a') as f:
            #     f.write(str(line.split('\t/')) + '\n----------------------\n')
            if '0x' not in line:
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
            if lib_file_path.startswith('/lib/'):
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


    # 5. 在invoke方法中实现该自定义命令具体的功能
    # args表示该命令后面所衔接的参数，这里通过string_to_argv转换成数组
    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 6:
            raise gdb.GdbError('输入参数数目不对，help mv以获得用法')
        # 6. 使用gdb.execute来执行具体的命令
        start_code = argv[4]
        end_code = argv[5]

        file_assign = gdb.execute('file ' + argv[0], to_string=True)
        run_result = gdb.execute(argv[3].replace('_', ' ') + ' ' + argv[1], to_string=True)
        libs_result = gdb.execute('libs', to_string=True)
        # with open('log.txt', 'a') as f:
        #     f.write(libs_result)
        libs_address, start_codes, end_codes, libs_name = self.get_lib_address(libs_result)
        libs_address['self'] = [start_code + '-' + end_code]
        start_codes.append(start_code)
        end_codes.append(end_code)
        libs_name.append('self')
        asm_ins = gdb.execute('x/i $pc', to_string=True).replace('=> ', '')
        asm_address = asm_ins.split(' ')[0]
        with open('log.txt', 'a') as f:
            f.write('--------------------------------------------------------------\n')
            f.write('test case:\n' + argv[0] + '\n\n')
            f.write('libs:\n' + str(libs_address) + '\n\n')
            f.write('asm_address:\n' + asm_address + '\n\n')
            f.write('asm_ins:\n' + asm_ins + '\n\n')
            f.write('start_code:\n' + start_code + '\n\n')
            f.write('end_code:\n' + end_code + '\n\n')

        while self.is_in_range(asm_address, start_codes, end_codes) == -1:
            run_result = gdb.execute('up 1', to_string=True)
            asm_ins = gdb.execute('x/i $pc', to_string=True).replace('=> ', '')
            asm_address = asm_ins.split(' ')[0]
            if ':' in asm_address:
                asm_address = asm_address[:asm_address.index(':')]
            # with open('log.txt', 'a') as f:
            #     f.write(run_result + '\n')
            #     f.write(asm_address + '\n')
            #     f.write(asm_ins + '\n')
        lib_name = libs_name[self.is_in_range(asm_address, start_codes, end_codes)]
        with open(argv[2], 'a') as f:
            # f.write(file_assign + '\n')
            # f.write(run_result + '\n')
            # f.write(argv[0] + '\t' + argv[1] + '\t' + asm_ins.replace('\t', ' ').replace('\n', '') + '\t' +
            #         run_result.split('\n')[-2].replace('\t', ' ') + '\n')
            f.write(argv[0] + '\t' + argv[1] + '\t' + asm_ins.replace('\t', ' ').replace('\n', '') + '\t' +
                    lib_name + '\n')
        gdb.execute('quit')
        sys.exit()


# 7. 向gdb会话注册该自定义命令
if __name__ == '__main__':
    Dis()
