input = [1,2,3,4,5,6,7,8,9]

inputmin = min(input)
print(inputmin)

            if section == 'temp':
                print(input1)
                mintemp = 36
                maxtemp = 64
                output_file = os.path.join('8Bits', f"{section}.json")
                with open(output_file, 'w') as f:
                    f.write('"tCod":[' + f"{section}," + f"{mintemp}," + f"{maxtemp}]\n")
                    f.write('"tDis":[incr,min temp,max temp],\n')
                    f.write('"tAdd":' + f"{hex_pos}\n")
                    f.write('"tUnit":' + '"C"\n')
                    f.write(f"\n\n{item}\n\n")
                    f.write(str(min(input1, input2))+',\n')
                    f.write(str(max(input1, input2))+'\n')