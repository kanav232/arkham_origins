import sys
def binary(num, num_bits):
    num=int(num)
    if num >= 0:
        binary_representation = bin(num)[2:]
        binary_representation = binary_representation.zfill(num_bits)
    else:
        positive_binary = bin(-num)[2:].zfill(num_bits)
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in positive_binary)
        
        carry = 1
        twos_complement = ''
        for bit in reversed(inverted_binary):
            result_bit = str((int(bit) + carry) % 2)
            carry = (int(bit) + carry) // 2
            twos_complement = result_bit + twos_complement
        
        binary_representation = twos_complement

    return binary_representation


register={"zero":'00000',
          "ra":'00001',
          "sp":'00010',
          "gp":'00011',
          "tp":'00100',
          "t0":'00101',
          "t1":'00110',
          "t2":'00111',
          "s0":'01000',#fp
          "s1":'01001',
          "a0":'01010',
          "a1":'01011',
          "a2":'01100',
          "a3":'01101',
          "a4":'01110',
          "a5":'01111',
          "a6":'10000',
          "a7":'10001',
          "s2":'10010',
          "s3":'10011',
          "s4":'10100',
          "s5":'10101',
          "s6":'10110',
          "s7":'10111',
          "s8":'11000',
          "s9":'11001',
          "s10":'11010',
          "s11":'11011',
          "t3":'11100',
          "t4":'11101',
          "t5":'11110',
          "t6":'11111'}
r_type={"add": '0110011',"sub":'0110011',"sll":'0110011',"slt":'0110011',
        "sltu":'0110011',"xor":'0110011',"srl":'0110011',
        "or":'0110011',"and":'0110011'}

i_type={"lw":'0000011',"addi":'0010011',"sltiu":'0010011',"jalr":'1100111'}

b_type={"beq":'1100011',"bne":'1100011',"blt":'1100011',"bge":'1100011',
        "bltu":'1100011',"bgeu":'1100011'}

s_type={"sw":'0100011'}

u_type={"lui":'0110111',"auipc":'0010111'}

j_type={"jal":'1101111'}

bonus={}
r_func3={"add":'000',"sub":'000',"sll":'001',"slt":'010',"sltu":'011',"xor":'100',"srl":'101',"or":'110',"and":'111'}
i_funt3={"lw":"010","addi":"000","sltiu":"011","jalr":"000"}
s_funt3={"sw":"010"}
b_funt3={"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}

#last=int(input("enter total number of test cases "))
machine_code=""
for i in range(1,1+1):
        input_file= sys.argv[1]
        output_file= sys.argv[2]
        file=open(f"simpleBin/{input_file}")
        lines = file.readlines()
        if(lines[-1]!="beq zero,zero,0"):
               raise SyntaxError("Missing Virtual Halt instruction")
        for line in lines:
                temp=""
                if(line=="\n"):
                       continue

                word=line.split()
                stuff=word[1].split(",")
                word[1]=stuff[0]
                for i in range(1,len(stuff)):
                        word.append(stuff[i])
                if(word[0] in r_type):
                        if(word[0]=="sub"):
                                temp+="0100000"
                        else:
                                temp+="0000000"
                        try:
                                temp+=register[word[3]]
                        except KeyError:
                               print(f"ERROR: Register {word[3]} not found\n")
                               break
                        try:
                                temp+=register[word[2]]
                        except KeyError:
                               print(f"ERROR: Register {word[2]} not found\n")
                               break

                        temp+=r_func3[word[0]]
                        try:
                                temp+=register[word[1]]
                        except KeyError:
                               print(f"ERROR: Register {word[1]} not found\n")
                               break
                        temp+=r_type[word[0]]

                
                elif word[0] in b_type:
                        b=binary(word[3],12)
                        temp+=b[-12]
                        temp+=b[-10:-4]
                        temp+=register[word[2]]
                        temp+=register[word[1]]
                        temp+=b_funt3[word[0]]
                        temp+=b[-4:]
                        temp+=b[-11]
                        temp+=b_type[word[0]]

                elif word[0] in s_type:
                        imm_part = word[2].split('(')[0]
                        if(int(imm_part)<-(2)**12 or int(imm_part)>-1+2**12):
                               print("ERROR: immediate value out of bound")
                               break
                        imm = binary(imm_part, 12)
                        try:
                                rs2 = register[word[1]]  
                        except KeyError:
                               print(f"ERROR: Register {word[1]} not found\n")
                               break
                        try:
                                rs1 = register[word[2].split('(')[1][:2]]
                        except KeyError:
                               print(f"ERROR: Register {word[2].split('(')[1][:2]} not found\n")
                               break
                        opcode = s_type[word[0]]  
                        temp = imm[0:7] + rs2 + rs1 + '010' + imm[7:12] + opcode




                elif(word[0] in j_type):
                        # if(word[2]>2**20-1 or):
                        #        print("ERROR: immediate value out of bound")
                        #        break
                        b=binary(word[2],20)
                        temp+=b[-20]
                        temp+=b[-10:]
                        temp+=b[-11]
                        temp+=b[-19:-11]
                        try:
                                temp+=register[word[1]]
                        except KeyError:
                               print(f"ERROR: Register {word[1]} not found\n")
                               break
                        temp+=j_type[word[0]]
                elif(word[0] in u_type):
                        if(int(word[2])>1048576):
                               print("ERROR: immediate value out of bound\n")
                               break
                        temp+=binary(word[2],20)
                        try:
                                temp+=register[word[1]]

                        except KeyError:
                               print(f"ERROR: Register {word[1]} not found\n")
                               break
                        temp+=u_type[word[0]]
                elif(word[0] in i_type):
                        if(word[0]=='lw'):
                            imm_part=word[2].split('(')#['imm',rs1)]
                            imm=imm_part[0]
                            rs1=imm_part[1].split(')')[0]#rs1[0]
                            bin1=binary(imm,12)
                            temp=bin1+register[rs1]+i_funt3[word[0]]+register[word[1]]+i_type[word[0]]
                        
                        else:
                             bin1=binary(word[3],12)
                             temp=bin1+register[word[2]]
                             temp=temp+i_funt3[word[0]]
                             temp=temp+register[word[1]]
                             temp=temp+i_type[word[0]]
                        
                else:
                       print("ERROR: Unknown Instruction")
                       break
                if(line==lines[-1]):
                        machine_code+=temp
                else:
                        machine_code+=temp+"\n"

        file.close()
output=open(f"{output_file}","w")
output.write(machine_code)
output.close()