import os
import subprocess


def get_start_end_code(exe_file, run_ins, input_file):
    start_code = ''
    end_code = ''
    cmd = '~/Downloads/symbol-collect-user-64 -d page -D logs_out/page.log -- "' + exe_file + '" ' + run_ins.replace(
        'run', '').replace('_', ' ') + ' "' + input_file + '"'
    # print(cmd)
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    if 'Invalid ELF image for this architecture' not in str(out):
        for line in open('logs_out/page.log', 'r'):
            if line.startswith('start_code'):
                start_code = line[len('start_code  '):-1]
            if line.startswith('end_code'):
                end_code = line[len('end_code  '):-1]
    if start_code == '' and end_code == '':
        cmd = '~/Downloads/symbol-collect-user-32 -d page -D logs_out/page.log -- "' + exe_file + '" ' + run_ins.replace(
            'run', '').replace('_', ' ') + ' "' + input_file + '"'
        # print(cmd)
        ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = ex.communicate()
        status = ex.wait()
        for line in open('logs_out/page.log', 'r'):
            if 'start_code' in line:
                start_code = line[line.index('start_code') + len('start_code  '):-1]
            if 'end_code' in line:
                end_code = line[line.index('end_code') + len('end_code  '):-1]
    return start_code, end_code


def get_so_libs(bin_file):
    cmd = 'ldd ' + bin_file
    # print(cmd)
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    rel_libs, act_libs, address = [], [], []
    for line in out.split('\n'):
        if 'linux-vdso.so.1' in line or 'ld-linux-x86-64.so.2' in line:
            continue
        line = line.replace('\t', '').replace(' ', '')
        if (line.find('=>') != -1):
            rel_libs.append(line.split('=>')[0])
            line = line.split('=>')[1]
        elif line.find('(') != -1:
            rel_libs.append('')
        else:
            continue
        if line.find('(') == -1:
            act_libs.append('')
            address.append('')
            continue
        act_libs.append(line.split('(')[0])
        address.append(line.split('(')[1][:-1])
    return rel_libs, act_libs

kinds = ['1', '2', '3', '4', '5']
project_names = ['bento4_aac2mp4', 'bento4_mp42aac', 'libav', 'libtiff', 'lrzip', 'mozjpeg', 'pax-util', 'pcre', 'potrace', 'ytnef', 'binutils']
for project_name in project_names:
    # if project_name == 'libming':
    #     exe_file = "/home/cobot/Desktop/tests/libming-CVE-2018-8962/libming-CVE-2018-8962/obj-aflgo/util/swftophp"
    #     input_dir = '/home/cobot/Desktop/tests/libming-CVE-2018-8962/libming-CVE-2018-8962/obj-aflgo/out/crashes'
    #     input_dir = '/home/cobot/honggfuzz_outputs'
    #     input_dir = '/home/cobot/bff_outputs'

    if project_name == 'sqlite':
        run_ins = "run_<_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/sqlite/ground-truth/sqlite/.libs/lt-sqlite3"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/sqlite/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/sqlite/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/sqlite/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/sqlite/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/sqlite/ground-truth/hf-cov/all/raw']

    if project_name == 'w3m':
        run_ins = "run_-dump_-T_text/html_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/w3m/ground-truth/w3m/w3m"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/w3m/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/w3m/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/w3m/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/w3m/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/w3m/ground-truth/hf-cov/all/raw']

# export LD_LIBRARY_PATH=/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/libmad-0.15.1b/.libs
    if project_name == 'libmad':
        run_ins = "run_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/libmad-0.15.1b/.libs/minimad"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/libmad/ground-truth/hf-cov/all/raw']

    if project_name == 'conntrackd':
        run_ins = "run_-C_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/conntrackd/ground-truth/conntrack-tools-1.4.3/src/conntrackd"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/conntrackd/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/conntrackd/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/conntrackd/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/conntrackd/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/conntrackd/ground-truth/hf-cov/all/raw']

    if project_name == 'php-5.5.37':
        run_ins = "run_/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/driver.php_--_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/php/source/5.5.37/sapi/cli/php"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-5.5.37/ground-truth/hf-cov/all/raw']

    if project_name == 'php-7.0.14':
        run_ins = "run_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-7.0.14/ground-truth/php/source/7.0.14/sapi/cli/php"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-7.0.14/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-7.0.14/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-7.0.14/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-7.0.14/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/php-7.0.14/ground-truth/hf-cov/all/raw']

# export LD_LIBRARY_PATH=/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/R-3.3.2/lib
# export R_HOME=/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/R-3.3.2
    if project_name == 'R':
        run_ins = "run_--no-restore_--slave_--file=/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/driver.r_--args_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/R-3.3.2/bin/exec/R"
        input_dirs = ['/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/afl-tmin/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/bff-1/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/bff-5/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/hf/all/raw',
        '/home/cobot/SCB/SemanticCrashBucketing/src/complete/R/ground-truth/hf-cov/all/raw']

    if project_name == 'mozjpeg':
        run_ins = "run_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/mozjpeg-2.1/.libs/cjpeg"
        input_dirs = ['/home/cobot/test_projects/cjpeg/afl_crash_1/out/queue',
        '/home/cobot/test_projects/cjpeg/afl_crash_2/out/queue',
        '/home/cobot/test_projects/cjpeg/afl_crash_3/out/queue',
        '/home/cobot/test_projects/cjpeg/afl_crash_4/out/queue',
        '/home/cobot/test_projects/cjpeg/total']

    if project_name == 'libav':
        run_ins = "run_-i"
        run_ins_2 = "_-f_/dev/null_"
        exe_file = "/home/cobot/project-i386/libav-11.8/avconv"
        input_dirs = ['/home/cobot/test_projects/libav/afl_crash_1/out/queue',
        '/home/cobot/test_projects/libav/afl_crash_2/out/queue',
        '/home/cobot/test_projects/libav/afl_crash_3/out/queue',
        '/home/cobot/test_projects/libav/afl_crash_4/out/queue',
        '/home/cobot/test_projects/libav/total']

    if project_name == 'libtiff':
        run_ins = "run_-i"
        run_ins_2 = "_/dev/null"
        exe_file = "/home/cobot/project-i386/libtiff-Release-v4-0-7/tools/.libs/tiffcp"
        input_dirs = ['/home/cobot/test_projects/libtiff/afl_crash_1/out/queue',
        '/home/cobot/test_projects/libtiff/afl_crash_2/out/queue',
        '/home/cobot/test_projects/libtiff/afl_crash_3/out/queue',
        '/home/cobot/test_projects/libtiff/afl_crash_4/out/queue',
        '/home/cobot/test_projects/libtiff/total']

    if project_name == 'bento4_mp42aac':
        run_ins = "run_"
        run_ins_2 = "_/dev/null"
        exe_file = "/home/cobot/project-i386/Bento4-1.5.0-617/build/mp42aac"
        input_dirs = ['/home/cobot/test_projects/bento4_mp42aac/afl_crash_1/out/queue',
        '/home/cobot/test_projects/bento4_mp42aac/afl_crash_2/out/queue',
        '/home/cobot/test_projects/bento4_mp42aac/afl_crash_3/out/queue',
        '/home/cobot/test_projects/bento4_mp42aac/afl_crash_4/out/queue',
        '/home/cobot/test_projects/bento4_mp42aac/total']

    if project_name == 'lrzip':
        run_ins = "run_-t"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/lrzip-0.631/lrzip"
        input_dirs = ['/home/cobot/test_projects/lrzip/afl_crash_1/out/queue',
        '/home/cobot/test_projects/lrzip/afl_crash_2/out/queue',
        '/home/cobot/test_projects/lrzip/afl_crash_3/out/queue',
        '/home/cobot/test_projects/lrzip/afl_crash_4/out/queue',
        '/home/cobot/test_projects/lrzip/total']

    if project_name == 'bento4_aac2mp4':
        run_ins = "run_"
        run_ins_2 = "_/dev/null"
        exe_file = "/home/cobot/project-i386/Bento4-1.5.0-617/build/aac2mp4"
        input_dirs = ['/home/cobot/test_projects/bento4_aac2mp4/afl_crash_1/out/queue',
        '/home/cobot/test_projects/bento4_aac2mp4/afl_crash_2/out/queue',
        '/home/cobot/test_projects/bento4_aac2mp4/afl_crash_3/out/queue',
        '/home/cobot/test_projects/bento4_aac2mp4/afl_crash_4/out/queue',
        '/home/cobot/test_projects/bento4_aac2mp4/total']

    if project_name == 'binutils':
        run_ins = "run_-A_-a_-l_-S_-s_--special-syms_--synthetic_--with-symbol-versions_-D"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/binutils-2.29.1/binutils/nm-new"
        input_dirs = ['/home/cobot/test_projects/binutils/afl_crash_1/out/queue',
        '/home/cobot/test_projects/binutils/afl_crash_2/out/queue',
        '/home/cobot/test_projects/binutils/afl_crash_3/out/queue',
        '/home/cobot/test_projects/binutils/total',
        '/home/cobot/test_projects/binutils/total']

    if project_name == 'pcre':
        run_ins = "run_-d"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/pcre-8.40/.libs/pcretest"
        input_dirs = ['/home/cobot/test_projects/pcre-2/afl_crash_1/out/queue',
        '/home/cobot/test_projects/pcre-2/afl_crash_2/out/queue',
        '/home/cobot/test_projects/pcre-2/afl_crash_3/out/queue',
        '/home/cobot/test_projects/pcre-2/afl_crash_4/out/queue',
        '/home/cobot/test_projects/pcre-2/total']

    if project_name == 'pax-util':
        run_ins = "run_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/pax-utils-1.2/dumpelf"
        input_dirs = ['/home/cobot/test_projects/pax-util/afl_crash_1/out/queue',
        '/home/cobot/test_projects/pax-util/afl_crash_2/out/queue',
        '/home/cobot/test_projects/pax-util/afl_crash_3/out/queue',
        '/home/cobot/test_projects/pax-util/afl_crash_4/out/queue',
        '/home/cobot/test_projects/pax-util/total']

    if project_name == 'potrace':
        run_ins = "run_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/potrace-1.3/src/potrace"
        input_dirs = ['/home/cobot/test_projects/potrace/afl_crash_1/out/queue',
        '/home/cobot/test_projects/potrace/afl_crash_2/out/queue',
        '/home/cobot/test_projects/potrace/afl_crash_3/out/queue',
        '/home/cobot/test_projects/potrace/afl_crash_4/out/queue',
        '/home/cobot/test_projects/potrace/total']

    if project_name == 'ytnef':
        run_ins = "run_"
        run_ins_2 = "_"
        exe_file = "/home/cobot/project-i386/ytnef-1.9.2/ytnefprint/.libs/ytnefprint"
        input_dirs = ['/home/cobot/test_projects/ytnef/afl_crash_1/out/queue',
        '/home/cobot/test_projects/ytnef/afl_crash_2/out/queue',
        '/home/cobot/test_projects/ytnef/afl_crash_3/out/queue',
        '/home/cobot/test_projects/ytnef/afl_crash_4/out/queue',
        '/home/cobot/test_projects/ytnef/total']

    result_file = './results/result_' + project_name + '.txt'
    with open(result_file, 'w') as f:
        pass
    for i in range(5):
        kind = kinds[i]
        log_file = 'log-exp-' + kind + '.txt'
        with open(log_file, 'w') as f:
            pass
        input_dir = input_dirs[i]
        inputs = os.listdir(input_dir)
        for input in inputs:
            if input.startswith(''):
                if input_dir.endswith(os.path.sep):
                    input_file = input_dir + input
                else:
                    input_file = input_dir + os.path.sep + input
                new_file_name = input_file.replace('(', '').replace(')', '').replace('%', '')
                os.rename(input_file, new_file_name)
                input_file = new_file_name

                start_code, end_code = get_start_end_code(exe_file, run_ins, input_file)
                # rel_libs, act_libs = get_so_libs(exe_file)
                # act_libs_str = ''
                # for act_lib in act_libs:
                #     act_libs_str += act_lib + '_-_-_'
                cmd = 'echo y |gdb -ex "source move.py" -ex "mv ' + exe_file + ' ' + input_file + ' ' + log_file + ' ' + \
                      run_ins + ' ' + run_ins_2 + ' ' + start_code + ' ' + end_code + '"'
                print(cmd)
                ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = ex.communicate()
                status = ex.wait()
        prefix = ''
        dic = {}
        with open(log_file, 'r') as f:
            for line in f:
                exe = line.split('\t')[0]
                input = line.split('\t')[1]
                asm = line.split('\t')[2]
                src = line.split('\t')[3]
                key = asm + '\t' + src
                # key = asm
                if key in dic.keys():
                    dic[key].append(input)
                else:
                    dic[key] = [input]
        with open(result_file, 'a') as f:
            f.write(kind + ':\n')
            for key in dic.keys():
                f.write(key.replace('\n', '') + '\t' + str(len(dic[key])) + '\t')
                for input in dic[key]:
                    f.write(input.replace(prefix, '') + '\t')
                f.write('\n')
            f.write('\n')

