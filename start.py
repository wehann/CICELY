import os
import subprocess
import shutil


def get_start_end_code(instruction):
    start_code, end_code = '', ''
    cmd = '~/Downloads/symbol-collect-user-64 -d page -D logs_out/page.log -- ' + instruction
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    ex.wait()
    if 'Invalid ELF image for this architecture' not in str(out):
        for line in open('logs_out/page.log', 'r'):
            if line.startswith('start_code'):
                start_code = line[len('start_code  '):-1]
            if line.startswith('end_code'):
                end_code = line[len('end_code  '):-1]
    if start_code == '' and end_code == '':
        cmd = '~/Downloads/symbol-collect-user-32 -d page -D logs_out/page.log -- ' + instruction
        ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = ex.communicate()
        ex.wait()
        for line in open('logs_out/page.log', 'r'):
            if 'start_code' in line:
                start_code = line[line.index('start_code') + len('start_code  '):-1]
            if 'end_code' in line:
                end_code = line[line.index('end_code') + len('end_code  '):-1]
    return start_code, end_code


def copy_file(input_directory, new_inputs_directory, input_filename):
    input_file_path = os.path.join(input_directory, input_filename)
    new_input_file_path = os.path.join(new_inputs_directory, input_filename.replace('(', '').replace(')', '').replace('%', ''))  # For some characters in filename are sensitive in terminal, we'll modify them.
    shutil.copyfile(input_file_path, new_input_file_path)
    return new_input_file_path


def start(configs, work_folder):
    results_directory = work_folder + os.path.sep + 'results' + os.path.sep
    if os.path.isdir(results_directory):
        shutil.rmtree(results_directory)
    os.makedirs(results_directory)
    for project_name, config in configs.items():
        print('Analyzing project [' + project_name + ']...')
        executable_file_path = config['executable_file_path']
        run_instruction = config['run_instruction']
        input_directories = config['input_directories']
        result_file = results_directory + 'result_' + project_name + '.txt'
        with open(result_file, 'w') as f:
            pass
        for i in range(len(input_directories)):
            input_directory = input_directories[i]
            log_directory = work_folder + os.path.sep + 'logs' + os.path.sep + project_name + os.path.sep
            if os.path.isdir(log_directory):
                shutil.rmtree(log_directory)
            os.makedirs(log_directory)
            new_inputs_directory = work_folder + os.path.sep + 'inputs' + os.path.sep + project_name + os.path.sep + str(i) + os.path.sep
            if os.path.isdir(new_inputs_directory):
                shutil.rmtree(new_inputs_directory)
            os.makedirs(new_inputs_directory)
            log_file = log_directory + 'log-' + str(i) + '.txt'
            with open(log_file, 'w') as f:
                pass
            input_files = os.listdir(input_directory)
            for input_filename in input_files:
                input_file_path = copy_file(input_directory, new_inputs_directory, input_filename)
                execute_instruction = run_instruction.replace('__PROGRAM__', '"' + executable_file_path + '"').replace('__SEEDFILE__', '"' + input_file_path + '"')
                start_code, end_code = '', ''
                start_code, end_code = get_start_end_code(execute_instruction)
                temp_instruction = run_instruction.replace(' ', '_').replace('__PROGRAM__', '').replace('__SEEDFILE__', ' ') + '_'
                cmd = 'echo "" | gdb -ex "source classifier.py" -ex "classify %s %s %s %s %s %s" ' % (executable_file_path, input_file_path, temp_instruction, start_code, end_code, log_file)
                # print('GDB cmd: ' + cmd)
                # os.system(cmd)
                ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                ex.communicate()
                ex.wait()
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
                f.write('Group ' + str(i) + ':\n')
                for key in dic.keys():
                    f.write(key.replace('\n', '') + '\t' + str(len(dic[key])) + '\t')
                    for input in dic[key]:
                        f.write(input + '\t')
                    f.write('\n')
                f.write('\n')
        print('Analyze project [' + project_name + '] complete.')

