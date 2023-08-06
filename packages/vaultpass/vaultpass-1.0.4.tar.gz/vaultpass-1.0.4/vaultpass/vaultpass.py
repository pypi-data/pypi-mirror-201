#!/usr/bin/env python3

try:
	import argparse
	import getpass
	import json
	import platform
	import requests
	import sys
except Exception as e:
	print()
	print('Could not import the required modules, exiting script ...')
	print()
	exit(1)

try:
	import passpy
	pass_available = True
except Exception as e:
	pass_available = False

def cyberark_choose_account(cyberark_accounts_list: list):
	print('>> Choose Account <<')
	print()

	cyberark_accounts_dict = {}
	
	for account in cyberark_accounts_list:	
		cyberark_accounts_id = account['id']
		
		try:
			cyberark_accounts_name = account['name']
		except:
			cyberark_accounts_name = 'No Name'
			
		try:
			cyberark_accounts_username = account['userName']
		except:
			cyberark_accounts_username = 'No Username'
			
		cyberark_accounts_dict[cyberark_accounts_username] = []
		cyberark_accounts_dict[cyberark_accounts_username] = [cyberark_accounts_id, cyberark_accounts_name]
			
	cyberark_accounts_id_list = []
	
	for username in sorted(cyberark_accounts_dict):	
		cyberark_accounts_id, cyberark_accounts_name = cyberark_accounts_dict[username]
		cyberark_accounts_id_list.append(cyberark_accounts_id)

	if len(cyberark_accounts_list) == 1:
		print('Good news! Account found ...')
		print()
		
		script_choose_account_choice = 0
	else:
		print('Displaying choices ...')
		print()
		
		print(f"{'Choice:' :<10}{'Account:' :<25}{'Name/Description:'}")
		
		cyberark_accounts_id_count = 0
		
		for username in sorted(cyberark_accounts_dict):
			cyberark_accounts_id_count += 1
			cyberark_accounts_id, cyberark_accounts_name = cyberark_accounts_dict[username]
			print(f"{cyberark_accounts_id_count :<10}{username[0:24] :<25}{cyberark_accounts_name[:44]}")
			
		print()
		
		print(f'Choice: 1-{cyberark_accounts_id_count}')
		print('r: Return to the main menu')
		print()
		
		script_choose_account_quit_flag = False
	
		while script_choose_account_quit_flag is False:
			script_choose_account_choice_input = input(f'Enter your choice: ')
			print()
		
			if script_choose_account_choice_input == 'r':
				break
			else:
				try:	
					script_choose_account_choice = int(script_choose_account_choice_input) - 1
					
					if (script_choose_account_choice > -1) and (script_choose_account_choice < len(cyberark_accounts_id_list)):
						return cyberark_accounts_id_list[script_choose_account_choice]
				except:
					script_choose_account_choice = -1

					print('Your choice was not a number in the specified range.')
					print()

def cyberark_output_password(cyberark_auth_header: dict, cyberark_chosen_password: str):
	print('>> Display or Save Password <<')
	print()
				
	cyberark_response_search_password_dict = do_webservice_request('POST', f'https://cyberark.its.umich.edu/PasswordVault/api/Accounts/{cyberark_chosen_password}/Password/Retrieve', cyberark_auth_header, {})
	
	script_output_password_quit_flag = False
	script_output_password_return = False
	
	while script_output_password_quit_flag is False:
		print('d: Display the password on the screen')
		if pass_available is True: print('s: Save the password in pass')
		print('r: Return to the main menu')
		print('!q: Exit the script')
		print()
		
		script_output_password_choice_input = input('Enter your choice: ')
		script_output_password_choice = script_output_password_choice_input.lower()
		print()
		
		if script_output_password_choice == 'd':	
			print(' Display Password '.center(50, "-"))
		
			if len(cyberark_response_search_password_dict) > 0:		
				print(' Success! '.center(50, '-'))
				print(f' {cyberark_response_search_password_dict} '.center(50, "-"))
				
			else:		
				print(' Error! '.center(50, "-"))
				
			print('-' * 50)
			print()
			
			script_output_password_quit_flag = True
		elif script_output_password_choice == 's':	
			cyberark_password_name_input = input('Enter the name of the password: ')
			print()
			
			try:
				password_store = passpy.Store()
				password_set = password_store.set_key(cyberark_password_name_input, cyberark_response_search_password_dict, force=True)
			
				print(' Save Password '.center(50, "-"))
			
				if password_set is None:		
					print(' Success! '.center(50, "-"))			
				else:		
					print(' Error! '.center(50, "-"))
				
				print('-' * 50)
				print()
			except:
				print('Error ...')
				print('Message: You do not have pass configured!')
				print()
			
			script_output_password_quit_flag = True
		elif script_output_password_choice == 'r':
			script_output_password_quit_flag = True
		elif script_output_password_choice == '!q':
			return True
		else:	
			print('You did not choose d, s, r, or !q.')
			print()

def cyberark_search_accounts(cyberark_auth_header: dict):
	print('>> Search for Account <<')
	print()

	print('Search accounts: Enter a search term')
	print('r: Return to the main menu')
	print()
	
	script_search_accounts_input = input('Enter your choice: ')
	print()
	
	if script_search_accounts_input == '':	
		print('You did not enter a search term.')
		print()
	elif script_search_accounts_input == 'r':
		pass
	else:
		cyberark_response_search_accounts_dict = do_webservice_request('GET', f'https://cyberark.its.umich.edu/PasswordVault/api/Accounts?search={script_search_accounts_input}', cyberark_auth_header, {})
		
		try:	
			cyberark_search_accounts_return = cyberark_response_search_accounts_dict['value']
		except:
			cyberark_search_accounts_return = []
			
		return cyberark_search_accounts_return

def do_webservice_request(requests_method: str, requests_url: str, requests_headers: dict, requests_json: dict or None):
	try:	
		webservice_response = requests.request(
				method=requests_method,
				url=requests_url,					
				headers=requests_headers,
				json=requests_json
			)
		
		webservice_response.raise_for_status()

		return json.loads(webservice_response.text)	
	except (ConnectionError, requests.exceptions.HTTPError, Timeout, Exception) as e:	
		print('Error ...')
		print(f'Message: {str(e)}')
		print()
		
		exit(1)
	
def get_auth_userinfo_from_commandline():
	print()
	print('>>> VaultPass: A CyberArk Search Script <<<')
	print()
	
	print('>> Provide Credentials <<')
	print()	
	
	parser = argparse.ArgumentParser(description='VaultPass: Search CyberArk for elevated accounts and retrieve their passwords. You can only retrieve accounts that you are able to view.')
	
	parser.add_argument('--uniqname', '-u', type=str, required=True, help='Your uniqname')
	parser.add_argument('--password', '-p', type=str, required=True, help='Your UMICH Level 1 password')
	
	args = parser.parse_args()
	
	username = args.uniqname
	password = args.password
	
	return username, password
	
def get_auth_userinfo_from_directinput():
	print()
	print('>>> VaultPass: A CyberArk Search Script <<<')
	print()
	
	print('>> Provide Credentials <<')
	print()	
	
	print('>> Enter your uniqname and UMICH Level 1 Password <<')
	print()
	
	username = input('uniqname: ')
	print()
	
	password = getpass.getpass(prompt='Password: ')
	print()
	
	if username == '' or password == '':	
		print('Error ...')
		print('Message: You did not enter a uniqname or a UMICH Level 1 password!')
		print()
		
		exit(1)
		
	return username, password
	
def get_cyberark_auth_header(username: str, password: str):
	print('>> Authenticating ... <<')
	print()
	
	cyberark_generic_header = {'content-type': 'application/json', 'accept': 'application/json'}
	cyberark_auth_userinfo_dict = {'username': username, 'password': password}
	
	try:	
		cyberark_auth_token_string = do_webservice_request('POST', 'https://cyberark.its.umich.edu/PasswordVault/api/auth/RADIUS/Logon', cyberark_generic_header, cyberark_auth_userinfo_dict)
		
		cyberark_auth_header = cyberark_generic_header
		cyberark_auth_header['Authorization'] = cyberark_auth_token_string
		
		print('Success!')
		print()
		
		return cyberark_auth_header		
	except:	
		print('Error ...')
		print('Message: There was an error retrieving the authentication token.')
		print()
		
		exit(1)

def main():	
	if len(sys.argv) > 1:
		username, password = get_auth_userinfo_from_commandline()		
	else:	
		username, password = get_auth_userinfo_from_directinput()

	cyberark_auth_header = get_cyberark_auth_header(username, password)
	
	script_quit_choice = 's'
	script_quit_flag = False
	
	while script_quit_flag is False:
		if script_quit_choice == 's':			
			cyberark_accounts_list = cyberark_search_accounts(cyberark_auth_header)
			
			if cyberark_accounts_list is None:
				pass
			else:
				if len(cyberark_accounts_list) == 0:
					print('Your search produced no results.')
					print()
				else:				
					cyberark_chosen_account = cyberark_choose_account(cyberark_accounts_list)
					
					if not(cyberark_chosen_account is None):
						script_output_password_quit_flag = cyberark_output_password(cyberark_auth_header, cyberark_chosen_account)
						
						if script_output_password_quit_flag is True:
							script_quit_flag = True
	
		elif script_quit_choice == '!q':
			script_quit_flag = True
		else:
			print('You did not choose s or !q.')
			print()
			
		if script_quit_flag is False:
			print('Do you want to search again for another account or exit the script?')
			print()			
			print('s: Search again')
			print('!q: Exit the script')
			print()
			
			script_quit_choice_input = input('Enter your choice: ')
			script_quit_choice = script_quit_choice_input.lower()
			
			print()
				
	print('>> Exiting VaultPass ... <<')
	print()
			
	print('Buh-Bye Now! Y\'all have a GREAT DAY!')
	print()

if __name__ == "__main__":

	main()

