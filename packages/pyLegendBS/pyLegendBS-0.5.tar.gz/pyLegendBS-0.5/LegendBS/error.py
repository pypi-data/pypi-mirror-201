def user_errors(error):
    if '[400 USERNAME_NOT_OCCUPIED]' in str(error):
       return "• You didn't provide username •"
    elif '[400 USERNAME_INVALID]' in str(error):
       return "• Username is invalid •"
    elif '[400 PEER_ID_INVALID]' in str(error):
       return "• Invalid User ID! •"
    else:
       return f"**Unknown Error:** \n\n {error}"
