from ScrapperClass import *
import re
import time

def FindSymbols(content):
    print('---------------Start printing symbols---------------')
    symbols_1 = re.findall('\$[A-Z][A-Z][A-Z][A-Z]',content)
    symbols_2 = re.findall('\$[A-Z][A-Z](?![A-Z])',content)
    symbols_3 = re.findall('\$[A-Z][A-Z][A-Z](?![A-Z])',content)
    print(symbols_1 + symbols_2 + symbols_3)
    print('------------------------End-------------------------')

scrapper = Scrapper()
scrapper.InitializeChrome()
while True:
    time.sleep(1)
    logged_in = scrapper.Login()
    if logged_in['status']:
        try:
            result = scrapper.NavigateToFirstPost()
            if result:

                content = scrapper.GetPostContent()
                FindSymbols(content)
            else:
                print ("---This is not the article you want to check.")    
        except Exception as error:
            print(error)        
            status = 'Error occured while searching stock symbols'
            print(status)
    elif logged_in['message'] == 'User not found':
        print('User not found')
    elif logged_in['message'] == 'Something went wrong':
        print('Something went wrong while logging in to website')
    elif logged_in['message'] == 'Incorrect password':
        print('Password is incorrect, Please check your password for login')

