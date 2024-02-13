#! /usr/bin/env python3    

import os, stat
from sys import argv
from io import BufferedReader, FileIO

# Creates tar file similar to command tar c file1 file2... > combined.tar
def create(files,tar):

    fdWriter = os.open(tar, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU)  # Get tar file to write
    
    for file in files:
        if not os.path.exists(file):                         # Check if path does not exist
            os.write(2,("File %s does not exist\n" % file).encode())
            exit()

        fdReader = os.open(file, os.O_RDONLY)               # Get file reader
    
        fileByteSize = os.path.getsize(file)                # Get file byte size

        fileHeader = f"{file}\n{fileByteSize}\n".encode()   # Store header for file data

        contents = os.read(fdReader, fileByteSize)          # Get byte data

        os.write(fdWriter, fileHeader)                      # Store header file contents in tar file
        os.write(fdWriter, contents)                        # Store data contents in tar file

        os.close(fdReader)                                  # Close when done
    os.close(fdWriter)                                      # Close when done


# Extract from .tar  file into separate files
def extract(tar):

    if not os.path.exists(tar):                              # Check if path does not exist
        os.write(2,("Tar file %s does not exist\n" % tar).encode())
        exit()

    fdReader = os.open(tar, os.O_RDONLY)                     # Get file description of tar
    tar_file = BufferedReader(FileIO(fdReader, 'rb'))        # Use buffered reader and read in binary
    
    while True:                                              # Extract all contents
        # Read file name    
        fname = tar_file.readline().decode().rstrip()        # Get name of that file

        if not fname:                                        # Empty
            break                                            # End of tar file
        
        fname = fname.split(".")                             # Create new file for output
        fname[0] += "2"
        fname = ".".join(fname)

        fdWriter = os.open(fname, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU) # Create or open new file to write to
        
        fsize = int(tar_file.readline().decode().rstrip())   # Get a file size
        
        contents = tar_file.read(fsize)                      # Get file content from within file size (fsize)
        
        os.write(fdWriter,contents)                          # Write to new file

    tar_file.close()                                         # Close when done




tarCommand = argv[1:]                                       # Takes TAR command input 

# if(len(tarCommand) != 3):            # Check if input is not right length for create or extract.
#     os.write(2, ("Commands are not valid\n".encode()))
    

command = tarCommand[0].lower()                             # c or x

if(command == 'c'):                                         # Check if command valid "c"
    os.write(1,"Creating...\n".encode())
    # arFile = (file1.split(".".encode())[0] + file2.split(".".encode())[0] + ".tar".encode()) # Tar file
    os.write(1, b"tar c files... > foogoo.tar\n" )

    create(tarCommand[1:3], "foogoo.tar") # create and store in .tar

if(tarCommand[0].lower() == 'x'):                           # Check if command valid "x"
    os.write(1,"Extracting...\n".encode())                  
    tar = tarCommand[1]
    extract(tar)                                            # Extract files from .tar
