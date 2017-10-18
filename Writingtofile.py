def save_to_txt(text_data,file_name):
    file_name = ((file_name.replace(".pdf", ".txt")).replace(".docx",".txt")).replace(".doc",".txt") # Renaming the file to txt
    file_writer = open(str(file_name), "w")
    file_writer.writelines(text_data) # Writes to a file
    file_writer.close() # Closes the file writer.

# sample test of writign the file
data = '''
What is the wealthiest place on earth?
Its the heart.......'''
file_name = "datatowrite.pdf" # File name
save_to_txt(data, file_name)
