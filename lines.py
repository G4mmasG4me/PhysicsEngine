import os

allowed_extensions = ['py']

rootdir = 'C:/Users/domho/Desktop/Projects/PhysicsEngine/'
total_lines = 0
total_chars = 0
for subdir, dirs, files in os.walk(rootdir):
  for file in files:
    if file.split('.')[-1] in allowed_extensions:
      file_lines = 0
      file_chars = 0
      f = open(os.path.join(subdir, file), encoding='utf8')
      for line_num, line in enumerate(f):
        for char in list(line):
          file_chars += 1
        file_lines += 1
      print('%s | Lines: %i | Chars: %i' % (file, file_lines, file_chars))
      total_lines += file_lines
      total_chars += file_chars
      
print('total Lines:', total_lines)
print('Total Chars:', total_chars)