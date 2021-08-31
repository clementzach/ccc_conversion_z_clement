import os

files_in_folder = os.listdir('.')

for file in files_in_folder:
	if file[-3:] == 'pdf' and file[0] != '.':
		in_file = file

print("Found pdf file: " + in_file)
out_file = 'extracted_information_by_location.csv'



#f = open(out_file, "w")


from pdfminer.high_level import extract_pages

from pdfminer.layout import LTTextContainer, LAParams
import pandas as pd



first_billable_y = 476.131542975
between_billable_y = 81.7200165



address_x = 43.5600015
id_phone_x = 301.55999025

account_y = 473.85153622499996

sex_x = 325.55999025
sex_y = 626.251545975

date_x = 436.56001275
dob_y = 641.131542975


therapist_service_x = 151.5600015
therapist_y = 626.131542975
service_y = 581.131542975
fee_y = 566.131542975



first_session_y = 611.131542975

last_session_y = 596.131542975

age_y = 626.131542975

policy_x = 263.400009

client_name_y = 686.851548225

client_id_x = 301.55999

client_id_y = 473.851536

phone_offset = 29.28000675000004


client_name = []
client_address = []

first_name = []
last_name = []
street_address = []
city = []
state = []
zip_code = []
client_sex = []
first_session = []
last_session = []
client_dob = []

therapist = []
service = []
fee = []



billable_1 = []
billable_2 = []
billable_3 = []
billable_4 = []
billable_1_phone = []
billable_2_phone = []
billable_3_phone = []
billable_4_phone = []

account_num = []

insurance_policy_1 = []
insurance_id_1 = []
insurance_phone_1 = []
insurance_address_1 = []

insurance_policy_2 = []
insurance_id_2 = []
insurance_phone_2 = []
insurance_address_2 = []

notes = []

client_id_num = []

num_pages = 1


def is_close(my_element, x_coord, y_coord):
    if abs(my_element.x0 - x_coord) < 2 and abs(my_element.y1 - y_coord) < 2: # within 2 from the coordinate
        return True
    else:
        return False

def single_close(num_1, num_2):
    if abs(num_1- num_2) < 2: # within 2 from the coordinate
        return True
    else:
        return False
current_record_num = 0

for page_layout in extract_pages(in_file):

    if current_record_num > 10:
            break

    if current_record_num % 100 == 0:
            print('now reading record ' + str(current_record_num + 1))
    current_record_num += 1

    current_client_name = ''
    current_client_dob = ''
    current_full_address = ''
    current_sex = ''
    current_first_session = ''
    current_last_session = ''

    current_first_name = ''
    current_last_name = ''

    current_street_address = ''
    current_city = ''
    current_state = ''
    current_zip = ''

    current_therapist = ''
    current_service = ''
    current_fee = ''


    
    current_billable_1 = ''
    current_billable_2 = ''
    current_billable_3 = ''
    current_billable_4 = ''
    current_billable_1_phone = ''
    current_billable_2_phone = ''
    current_billable_3_phone = ''
    current_billable_4_phone = ''
    
    current_account_num = ''
    current_client_id_num = ''



    current_insurance_address_1 = ''
    current_insurance_policy_1 = ''
    current_insurance_id_1 = ''
    current_insurance_phone_1 = ''

    current_insurance_address_2 = ''
    current_insurance_policy_2 = ''
    current_insurance_id_2 = ''
    current_insurance_phone_2 = ''

    current_notes = ''
    
    
    
    insurance_coord_found = False
    insurance_coord_found_2 = False
    id_coord_y_1 = 0.0
    
    #if num_pages > 30: ## only do the first few while testing
    #    break
    #num_pages +=1

    for element in page_layout:
            if isinstance(element, LTTextContainer):
                if element.get_text() == "ID #:\n":
                    if id_coord_y_1 == 0.0:
                        insurance_coord_found = True
                        #print('found insurance coordinate ' + str(element.y1))
                        #insurance_coord_x = element.x0 + 22.7999955
                        id_coord_y_1 = element.y1
                    else:
                        insurance_coord_found_2 = True
                        id_coord_y_2 = element.y1
            if isinstance(element, LTTextContainer):
                if element.get_text() == "Account #:\n":
                    client_id_y = element.y1
                    

    
    first_loop = True
    
    while first_loop: ## this while loop does nothing but I didn't want to remove the indent on all of the ones below
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                if insurance_coord_found:

                    if is_close(element, client_id_x, client_id_y):
                        current_client_id_num = element.get_text()



                    if is_close(element, id_phone_x, id_coord_y_1):
                        current_insurance_id_1 = element.get_text()
                        
                    elif is_close(element, address_x, id_coord_y_1 + 2.160003):
                        current_insurance_address_1 = element.get_text()
                        #insurance_written = True
                        
                    elif is_close(element, policy_x, id_coord_y_1 - 13.5600135):
                        current_insurance_policy_1 = element.get_text()[10:]
                        
                    elif is_close(element, id_phone_x, id_coord_y_1 - 27.11998049999994):
                        current_insurance_phone_1 = element.get_text()
                        #print('found insurance phone ' + current_insurance_phone)
                        #print(element.get_text())
                    if insurance_coord_found_2:
                        if is_close(element, id_phone_x, id_coord_y_2):
                            current_insurance_id_2 = element.get_text()
                        
                        elif is_close(element, address_x, id_coord_y_2 + 2.160003):
                            current_insurance_address_2 = element.get_text()
                            #insurance_written = True
                        
                        elif is_close(element, policy_x, id_coord_y_2 - 13.5600135):
                            current_insurance_policy_2 = element.get_text()[10:]
                        
                        elif is_close(element, id_phone_x, id_coord_y_2 - 27.11998049999994):
                            current_insurance_phone_2 = element.get_text()
                            #print('found insurance phone ' + current_insurance_phone)
                            #print(element.get_text())
                        
                if single_close(element.x0, address_x):
                    if single_close(element.y1, first_billable_y):
                        current_billable_1 = element.get_text()
                        
                    elif single_close(element.y1, client_name_y):
                        current_full_address = element.get_text()
                        current_client_name = current_full_address.split('\n')[0]
                        current_first_name = current_client_name.split()[0]
                        current_last_name = current_client_name.split()[-1]

                        current_street_address = current_full_address.split('\n')[1]
                        try:
                            current_city = current_full_address.split('\n')[2].split(',')[0]
                            current_state = current_full_address.split('\n')[2].split(',')[1][1:3]
                            current_zip = current_full_address.split('\n')[2].split(',')[1].split()[1]
                        except:
                       	    junk_var = 1
                            #print('')
                        
                        
                    elif single_close(element.y1, first_billable_y - between_billable_y):
                        current_billable_2 = element.get_text()
                        
                    elif single_close(element.y1, first_billable_y - (2 * between_billable_y)):
                        current_billable_3 = element.get_text()
                        
                    elif single_close(element.y1, first_billable_y - (3 * between_billable_y)):
                        current_billable_4 = element.get_text()
                    elif element.y1 < 250:
                        current_notes = current_notes + element.get_text() + '\n'
                        
                elif single_close(element.x0, id_phone_x):
                    if single_close(element.y1, first_billable_y - phone_offset):
                        current_billable_1_phone = element.get_text()
                        
                    elif single_close(element.y1, account_y):
                        current_account_num = element.get_text()
                        
                    elif single_close(element.y1, first_billable_y - between_billable_y - phone_offset):
                        current_billable_2_phone = element.get_text()
                        
                    elif single_close(element.y1, first_billable_y - (2 * between_billable_y - phone_offset)):
                        current_billable_3_phone = element.get_text()
                        
                    elif single_close(element.y1, first_billable_y - (3 * between_billable_y - phone_offset)):
                        current_billable_4_phone = element.get_text()
                elif single_close(element.x0, therapist_service_x):
                    if single_close(element.y1, therapist_y):
                        current_therapist = element.get_text()
                    elif single_close(element.y1, fee_y):
                        current_fee = element.get_text()
                    elif single_close(element.y1, service_y):
                        current_service = element.get_text()
                        
                    
                        


                elif is_close(element, sex_x, sex_y):
                    current_sex = element.get_text()[5:]
                    
                elif single_close(element.x0, date_x):
                    if single_close(element.y1, dob_y):
                        current_client_dob = element.get_text()
                    elif single_close(element.y1, first_session_y):
                        current_first_session = element.get_text()
                    elif single_close(element.y1, last_session_y):
                        current_last_session = element.get_text()
                
                    
            first_loop = False
                        
                        
                        
                    
    if current_insurance_address_1 == current_billable_2: #Avoid counting an address as both a insurance and billable party
        current_billable_2 = ''
        current_billable_2_phone = ''
    elif current_insurance_address_1 == current_billable_3:
        current_billable_3 = ''
        current_billable_3_phone = ''
    elif current_insurance_address_1 == current_billable_4:
        current_billable_4 = ''
        current_billable_4_phone = ''

    if current_insurance_address_2 == current_billable_2: #Avoid counting an address as both a insurance and billable party
        current_billable_2 = ''
        current_billable_2_phone = ''
    elif current_insurance_address_2 == current_billable_3:
        current_billable_3 = ''
        current_billable_3_phone = ''
    elif current_insurance_address_2 == current_billable_4:
        current_billable_4 = ''
        current_billable_4_phone = ''
                    
                    
                        
                    
    client_name.append(current_client_name)
    client_address.append(current_full_address)
    client_sex.append(current_sex)
    client_dob.append(current_client_dob)
    first_session.append(current_first_session)
    last_session.append(current_last_session)

    therapist.append(current_therapist)
    fee.append(current_fee)
    service.append(current_service)

    client_id_num.append(current_client_id_num)

    
    billable_1.append(current_billable_1)
    billable_2.append(current_billable_2)
    billable_3.append(current_billable_3)
    billable_4.append(current_billable_4)
    
    billable_1_phone.append(current_billable_1_phone)
    billable_2_phone.append(current_billable_2_phone)
    billable_3_phone.append(current_billable_3_phone)
    billable_4_phone.append(current_billable_4_phone)
    
    account_num.append(current_account_num)
    
    insurance_address_1.append(current_insurance_address_1)
    insurance_id_1.append(current_insurance_id_1)
    insurance_policy_1.append(current_insurance_policy_1)
    insurance_phone_1.append(current_insurance_phone_1)

    insurance_address_2.append(current_insurance_address_2)
    insurance_id_2.append(current_insurance_id_2)
    insurance_policy_2.append(current_insurance_policy_2)
    insurance_phone_2.append(current_insurance_phone_2)

    first_name.append(current_first_name)
    last_name.append(current_last_name)

    street_address.append(current_street_address)
    city.append(current_city)
    state.append(current_state)
    zip_code.append(current_zip)

    notes.append(current_notes)

    
    
    
            
                
            
       


df = pd.DataFrame(data = {'full name': client_name,
                          'first name' : first_name,
                          'last name' : last_name,
                          
                          'full address': client_address,
                          'street address' : street_address,
                          'city' : city,
                          'state' : state,
                          'zip code' : zip_code,
                          
                          'client sex' : client_sex,
                          'client date of birth' : client_dob,
                          'first session' : first_session,
                          'last session' : last_session,

                          'ID number' : client_id_num,

                          
                          'Therapist' : therapist,
                          'Fee' : fee,
                          'Service' : service,
                          
                          'Billable party 1': billable_1,
                          'Billable party 1 phone': billable_1_phone,
                          'Billable party 2': billable_2,
                          'Billable party 2 phone': billable_2_phone,
                          'Billable party 3': billable_3,
                          'Billable party 3 phone': billable_3_phone,
                          'Billable party 4': billable_4,
                          'Billable party 4 phone': billable_4_phone,
                          
                          'Account #' : account_num,
                          
                          'Insurance Address 1': insurance_address_1,
                          'Insurance ID 1' : insurance_id_1,
                          'Insurance Policy 1' : insurance_policy_1,
                          'Insurance Phone 1' : insurance_phone_1,
                          
                          'Insurance Address 2': insurance_address_2,
                          'Insurance ID 2' : insurance_id_2,
                          'Insurance Policy 2' : insurance_policy_2,
                          'Insurance Phone 2' : insurance_phone_2,

                          'Notes' : notes})

df.to_csv(path_or_buf = out_file, index = False)
