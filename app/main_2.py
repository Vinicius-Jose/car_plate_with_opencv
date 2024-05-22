def PalindromeCreator(strParam):
  str_reversed = strParam[::-1]
  return_message = "not possible"
  if strParam == str_reversed:
    return strParam
  if len(strParam) < 3:
    return return_message
  for i in range(len(strParam)-1):
    new_str = strParam.replace(strParam[i],"")
    new_str_2 = strParam.replace(strParam[i],"")
    new_str_2 = new_str_2.replace(strParam[i+1],"")
    if new_str[::-1] == new_str and len(new_str) >= 3:
      return strParam[i]
    elif new_str_2[::-1] == new_str_2 and len(new_str_2) >= 3:
      return strParam[i] + strParam[i+1]
  # code goes here
  return return_message

# keep this function call here 
print (PalindromeCreator("danada"))