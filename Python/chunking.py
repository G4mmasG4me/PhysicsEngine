from math import ceil

def chunking(my_list, chunk_size):
  """
  Splits image into chunks, given by chunk size
  
  Parameters:
    my_list (list): 2d or higher list, to be split into square chunks
    chunk_size (list, tuple): list of 2 integers, specificying chunk size in width and height
  Returns:
    (list): list of chunks
  """
  row_size = len(my_list[0])
  for row in my_list:
    if len(row) != row_size:
      return None, 'Rows not same size throughout'
    
  num_chunks = [ceil(row_size / chunk_size[0]), ceil(len(my_list) / chunk_size[1])]

  chunks = []
  for y_chunk in range(num_chunks[1]):
    for x_chunk in range(num_chunks[0]):
      chunk = []
      for y in range(chunk_size[1]):
        y_pos = y_chunk * chunk_size[1] + y
        if y_pos >= len(my_list):
          break
        for x in range(chunk_size[0]):
          x_pos = x_chunk * chunk_size[0] + x
          
          if x_pos >= row_size:
            break
          chunk.append(my_list[y_pos][x_pos])
      
      chunks.append(chunk)
  return chunks