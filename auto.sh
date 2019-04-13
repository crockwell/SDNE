executable_name=parser
echo $executable_name
g++ -std=c++11 -o $executable_name parser.cpp
./$executable_name cit-Patents.txt apat63_99.txt 1993 1999 false

