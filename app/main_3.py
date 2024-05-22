def StringReduction(strParam):
  letters = set(["a","b","c"])
  strParam = list(strParam)
  while len(set(strParam)) != 1:
  # code goes here
    for i in range(len(strParam) -1):
      if strParam[i] != strParam[i+1]:
        replace_letters = set([strParam[i] ,strParam[i+1]])
        new_letter = letters - replace_letters
        strParam[i+1] = list(new_letter)[0]
        strParam.pop(i)
        break
  return len(strParam)

# keep this function call here 
print (StringReduction("abcabc"))

