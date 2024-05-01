import re

keys = {
  'k': 1000,
  'M': 1000000,
  'G': 1000000000,
}


def extract_loop(lines):
  res_lines = []
  continues = 0

  for i in range(len(lines)):
    flag = 0
    line = lines[i]

    if '{' in line:
      continues += 1
    elif '}' in line:
      if continues > 0:
        continues -= 1
      else:
        flag = 1
    
    res_lines.append(line)
    
    if flag:
      break
  
  return res_lines


def extract_parallel_regions(file_content):
  lines = file_content.split('\n')
  res_lines = []

  for i in range(len(lines)):
    line = lines[i]

    if not '#pragma dvm parallel' in line:
      continue

    while not 'for' in line:
      i += 1
      line = lines[i]
    
    res_lines.append(line)

    if '{' in line:
      i += 1
      loop_lines = extract_loop(lines[i:])
      res_lines += loop_lines
      i += len(loop_lines)
    elif '{' in lines[i+1]:
      i += 1
      line = lines[i]
      res_lines.append(line)

      i += 1
      loop_lines = extract_loop(lines[i:])
      res_lines += loop_lines
      i += len(loop_lines)
    else:
      tabs_count = len(lines[i].split('|')[2].split('for')[0])
      i += 1

      line = lines[i]

      new_tabs_count = 0
      spl = line.split('|')[2][0]
      while line.split('|')[2][new_tabs_count] == ' ' and new_tabs_count < len(line.split('|')[2]):
        new_tabs_count += 1

      res_lines.append(line)
      i += 1
      line = lines[i]

      while tabs_count < new_tabs_count:
        i += 1
        line = lines[i]
        res_lines.append(line)
        if not line.split('|')[2]:
          continue
        new_tabs_count = 0

        while line.split('|')[2][new_tabs_count] == ' ' and new_tabs_count < len(line.split('|')[2]):
          new_tabs_count += 1
  return res_lines


def get_coverage_metric(file_path):
  with open(file_path, 'r') as f:
    file_content = f.read()

  parallel_str_list = extract_parallel_regions(file_content)

  # with open('./output.txt', 'w') as f:
  #   f.write(parallel_str)

  average = 0
  count = len(parallel_str_list)

  for line in parallel_str_list:
    if not line.strip():
      continue
    if len(line.split('|')) > 1 and line.split('|')[1].strip():
      pre_number = line.split('|')[1].strip()
    else:
      continue

    if 'k' in pre_number:
      number = float(pre_number[:-1]) * keys['k']
    elif 'M' in pre_number:
      number = float(pre_number[:-1]) * keys['M']
    elif 'G' in pre_number:
      number = float(pre_number[:-1]) * keys['G']
    else:
      number = float(pre_number)
    average += number

  average /= count

  return average