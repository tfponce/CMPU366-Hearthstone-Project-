import sys

arg1 = str(sys.argv[1])
name = arg1.split("Cleaned.txt")[0]

with open(arg1, 'r') as f:
    content = f.read()
    content = content[2:len(f.read())-3]
    content = content.split('}, {')
    lines = [i +'\n' for i in content]
    
input_file = open(name + ".txt", "w")
input_file.writelines(lines)
input_file.close()