library(readxl)

library(dplyr)

library(lubridate)

library(tidyr)

library(comparator)

files_in_folder <- list.files() 

for (file in files_in_folder){
	file_length <- nchar(file)
	if (substr(file, start = file_length - 4, stop = file_length) == ".xlsx"){
		theranest_path = file
}
}
print(paste('found theranest file path at ', theranest_path, sep = ''))
from_theranest = readxl::read_excel(theranest_path )

print("reading in data from pdf")
from_pdf = read.csv('extracted_information_by_location.csv')


print("reformatting dataframes")
email_social <- from_theranest %>% mutate(
  only_first = sapply(`First Name`, function(x){strsplit(x, split = ' +')[[1]][1]}), 
only_last = sapply(`Last Name`, function(x){tail(strsplit(x, split = ' +')[[1]])}), 
dob = substr(`Date of Birth`, start = 1, stop = 10), 
combined_names = tolower(paste(only_first, only_last, dob))) %>% 
  rename(first_name_from_theranest = `First Name`, last_name_from_theranest = `Last Name`) %>% 
  select(c(combined_names, 
	   dob,
           Email, 
           Ssn, 
           first_name_from_theranest, 
           last_name_from_theranest, 
           'Primary Insurance: Insured Last Name',
           'Primary Insurance: Insured Middle Name',

           'Primary Insurance: Insured Phone',
           'Primary Insurance: Insured Birthdate',
           "Primary Insurance: Relationship To Insured")) %>%
           mutate(full_name = paste(first_name_from_theranest, last_name_from_theranest))

print('reformatting data from pdf')

print(colnames(from_pdf))
from_pdf_clean <- from_pdf %>% mutate(combined_names = 
                                        tolower(paste(first.name, 
                                              last.name, 
                                              substr(parse_date_time(client.date.of.birth, 
                                                                     orders = 'mdy' ), 
                                                     start = 1, 
                                                     stop = 10) , sep = " ")),
					dob_format = substr(parse_date_time(client.date.of.birth,
                                                                     orders = 'mdy' ),
                                                     start = 1,
                                                     stop = 10)) %>% 
  filter(sapply(full.name, nchar) > 5, 
         sapply(Billable.party.1, nchar) > 10, 
         sapply(client.date.of.birth, nchar) > 1)
         


print(paste('data cleaning reduced the number of records from ', toString(nrow(from_pdf)), 'to', toString(nrow(from_pdf_clean)), 
            "\n records were removed if they didn't have a client date of birth, they didn't have a name, or didn't have a billable party", 
            sep = " "))



joined_df <- left_join(from_pdf_clean, email_social, by = 'combined_names', na_matches = 'never') 

joined_df <- joined_df %>% mutate(id = rownames(joined_df))


duplicate_df <- as.data.frame(table(from_pdf_clean$combined_names))



print('Individuals with duplicate records')
print(duplicate_df[duplicate_df$Freq > 1,])

print('Fuzzy matching for emails not matched to a client: ')

min_similarity_score <- 0.85


for (email in from_theranest$Email[! from_theranest$Email %in% joined_df$Email]){
  i <- which(email_social$Email == email)
  
    temp_joined_df <- joined_df[joined_df$dob_format == email_social$dob[i], ]
    
	if ((nrow(temp_joined_df) >= 1 ) && (nchar(email_social$dob[i], keepNA = F) > 4)){
  
  max_similarity_temp <- which.max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
  max_similarity <- as.numeric(temp_joined_df$id[max_similarity_temp])
  similarity <- max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
  
  if (similarity > min_similarity_score){

  print(paste("Assuming", 
              email_social$first_name_from_theranest[i],
              email_social$last_name_from_theranest[i],
              from_theranest$`Date of Birth`[i],
              "is the same as", 
              joined_df$full.name[max_similarity], 
              substr(parse_date_time(joined_df$client.date.of.birth[max_similarity], 
                                     orders = 'mdy' ), start = 1, stop = 10), "with similarity", 
              toString(similarity)))
                                     

  joined_df[max_similarity, 'Email'] <- email
  
  joined_df[max_similarity, 'Ssn'] <- email_social$Ssn[i][1]
  joined_df[max_similarity, 'first_name_from_theranest'] <- email_social$first_name_from_theranest[i][1]
  joined_df[max_similarity, 'last_name_from_theranest'] <- email_social$last_name_from_theranest[i][1]

  }
  
  }
}






for (Ssn in from_theranest$Ssn[! from_theranest$Ssn %in% joined_df$Ssn]){
  i <- which(email_social$Ssn == Ssn)
  
  temp_joined_df <- joined_df[joined_df$dob_format == email_social$dob[i], ]
  
  if ((nrow(temp_joined_df) >= 1 ) && (nchar(email_social$dob[i], keepNA = F) > 4)){
    
    max_similarity_temp <- which.max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
    max_similarity <- as.numeric(temp_joined_df$id[max_similarity_temp])
    similarity <- max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
    
    if (similarity > min_similarity_score){
      
      print(paste("Assuming", 
                  email_social$first_name_from_theranest[i],
                  email_social$last_name_from_theranest[i],
                  from_theranest$`Date of Birth`[i],
                  "is the same as", 
                  joined_df$full.name[max_similarity], 
                  substr(parse_date_time(joined_df$client.date.of.birth[max_similarity], 
                                         orders = 'mdy' ), start = 1, stop = 10), "with similarity", 
                  toString(similarity)))
      
      
      joined_df[max_similarity, 'Email'] <- email
      
      joined_df[max_similarity, 'Ssn'] <- email_social$Ssn[i][1]
      joined_df[max_similarity, 'first_name_from_theranest'] <- email_social$first_name_from_theranest[i][1]
      joined_df[max_similarity, 'last_name_from_theranest'] <- email_social$last_name_from_theranest[i][1]
      
    }
    
  }
}



for (l_name in from_theranest$`Last Name`[! from_theranest$`Last Name` %in% joined_df$last_name_from_theranest]){
	i <- which(email_social$last_name_from_theranest == l_name)
	
	temp_joined_df <- joined_df[joined_df$dob_format == email_social$dob[i], ]
	
	if ((nrow(temp_joined_df) >= 1 ) && (nchar(email_social$dob[i], keepNA = F) > 4)){
	  
	  max_similarity_temp <- which.max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
	  max_similarity <- as.numeric(temp_joined_df$id[max_similarity_temp])
	  similarity <- max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
	  
	  if (similarity > min_similarity_score){
	    
	    print(paste("Assuming", 
	                email_social$first_name_from_theranest[i],
	                email_social$last_name_from_theranest[i],
	                from_theranest$`Date of Birth`[i],
	                "is the same as", 
	                joined_df$full.name[max_similarity], 
	                substr(parse_date_time(joined_df$client.date.of.birth[max_similarity], 
	                                       orders = 'mdy' ), start = 1, stop = 10), "with similarity", 
	                toString(similarity)))
	    
	    
	    joined_df[max_similarity, 'Email'] <- email
	    
	    joined_df[max_similarity, 'Ssn'] <- email_social$Ssn[i][1]
	    joined_df[max_similarity, 'first_name_from_theranest'] <- email_social$first_name_from_theranest[i][1]
	    joined_df[max_similarity, 'last_name_from_theranest'] <- email_social$last_name_from_theranest[i][1]
	    
	  }
	  
	}
}


for (f_name in from_theranest$`First Name`[! from_theranest$`First Name` %in% joined_df$first_name_from_theranest]){
	i <- which(email_social$first_name_from_theranest == f_name)


	temp_joined_df <- joined_df[joined_df$dob_format == email_social$dob[i], ]
	
	if ((nrow(temp_joined_df) >= 1 ) && (nchar(email_social$dob[i], keepNA = F) > 4)){
	  
	  max_similarity_temp <- which.max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
	  max_similarity <- as.numeric(temp_joined_df$id[max_similarity_temp])
	  similarity <- max(JaroWinkler()(email_social$full_name[i], temp_joined_df$full.name))
	  
	  if (similarity > min_similarity_score){
	    
	    print(paste("Assuming", 
	                email_social$first_name_from_theranest[i],
	                email_social$last_name_from_theranest[i],
	                from_theranest$`Date of Birth`[i],
	                "is the same as", 
	                joined_df$full.name[max_similarity], 
	                substr(parse_date_time(joined_df$client.date.of.birth[max_similarity], 
	                                       orders = 'mdy' ), start = 1, stop = 10), "with similarity", 
	                toString(similarity)))
	    
	    
	    joined_df[max_similarity, 'Email'] <- email
	    
	    joined_df[max_similarity, 'Ssn'] <- email_social$Ssn[i][1]
	    joined_df[max_similarity, 'first_name_from_theranest'] <- email_social$first_name_from_theranest[i][1]
	    joined_df[max_similarity, 'last_name_from_theranest'] <- email_social$last_name_from_theranest[i][1]
	    
	  }
	  
	}
}

joined_df <- joined_df %>% select(!c(combined_names, dob_format, id))

write.csv(joined_df, 
          
          paste('final_joined_spreadsheet_',
          substr(now(), start = 1, stop = 10),
          '.csv', sep = ''), 
          na = '', row.names = F)

print('File write complete. The final merged file is in:')
print(paste('final_joined_spreadsheet_',
          substr(now(), start = 1, stop = 10),
          '.csv', sep = ''))
print('Don\'t forget to run the uninstall R program in the applications folder if you want to save storage space on this computer')
