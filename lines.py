import os

allowed_extensions = ['py', 'cpp']
extension_lines = {value: 0 for value in allowed_extensions}

total_lines = 0
total_chars = 0
for subdir, dirs, files in os.walk(os.getcwd()):
  for file in files:
    file_extension = file.split('.')[-1]
    if file_extension in allowed_extensions:
      file_lines = 0
      file_chars = 0
      f = open(os.path.join(subdir, file), encoding='utf8')
      for line_num, line in enumerate(f):
        for char in list(line):
          file_chars += 1
        file_lines += 1
      # print('%s | Lines: %i | Chars: %i' % (file, file_lines, file_chars))
      extension_lines[file_extension] += file_lines
      total_lines += file_lines
      total_chars += file_chars
      
print('Total Lines:', total_lines)
print('Total Chars:', total_chars)

for extension, lines in extension_lines.items():
  print(f'{extension}: {lines} Lines')