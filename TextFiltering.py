import os  # operating system module for checking the operating system
from db_main import *
from nltk.tokenize import sent_tokenize, word_tokenize

class TextFilter:
    data_base = DB()  # This creates the object for the database
    dirpath = ""  # Global Object accessible directory name
    # The below will be the general paths which will be used.
    education_list = ["bachelor", "masters", "phd", "specialization"]  # Type in other keywords as well
    skills_list = ["python", "django", "hacker"]
    certification_list = ["specialization", "certification"]  # Type in other keywords as well
    qualification_list = ["bachelors", "masters", "phd", "specialization"]  # Type in other keywords as well
    workexperience_list = ["sql administrator", "data scientist", "integrator", "programmer", "data integeration"]
    db = None
    file_data_id = None

    def __init__(self, additional_list_input=False):
        self.dir_path = os.path.dirname(
            os.path.realpath(__file__))  # Adding in the respectable folder name in the file !
        self.db = DB()
        print("Text filter file has been created !")  # Debugging !!
        if not additional_list_input:
            print("-#--Default Attributes search on going--#-")
        else:
            print("-- Advance Filter input ---")
            education = input("Enter the Education list here with spaces e.g MSC PHD : ")
            if education == "":
                self.education_list = self.education_list
                print("No Education Modification : going Default")
            else:
                self.education_list = (str(education).lower()).strip().split(" ")  # Splits at spaces
            # The above returns a list
            skills = input("Enter the skills list here with spaces e.g Python Django: ")
            if skills == "":
                self.skills_list = self.skills_list  # Intializing the same list as again , since going with default one
                print("Default Skills sets ")  # Debugging
            else:
                self.skills_list = (str(skills).lower()).strip().split(
                    " ")  # Converts the list from the sentence input as splitted
            certificaiton = input("Enter the certifications list in here: ")
            if certificaiton == "":
                self.certification_list = self.certification_list
                print("Default certification list ")
            else:
                self.certification_list = (str(certificaiton).strip().lower()).split(" ")
                # splitting of the certification on the basis of spaces
            qualification = input("Enter the qualification list as mentioned with spaces: ")
            if qualification == "":
                self.qualification_list = self.qualification_list
                print("Default Qualification List !")
            else:
                self.qualification_list = (str(qualification).lower().strip()).split(
                    " ")  # Converting to lower and then spliting
                # Splitting the qualification from the spaced to a list
            workexperience = input("Enter the work experience list to work with : ")
            if workexperience == "":
                self.workexperience_list = self.workexperience_list  # Setting the same work experience list
                print("Default work experience list")
            else:
                self.workexperience_list = (str(workexperience).lower().strip()).split(" ")
                # Splitting the string to list
            # Adding in all the filters to the database for the further processing!
            for edu in self.education_list:
                self.db.insert_into_filter_education(edu)  # inserts into the education table
            for skill in self.skills_list:
                self.db.insert_into_filter_skill(skill)  # Inserts into the filter table for skills
            for certificate in self.certification_list:
                self.db.insert_into_filter_certification(certificate)  # inserts into the certificate table
            for qualification in self.qualification_list:
                self.db.insert_into_filter_qualification(qualification)  # inserts into the qualification table
            for workexperience in self.workexperience_list:
                self.db.insert_into_filter_work_experience(
                    workexperience)  # inserts into the filter for the work experience
                # The above function are the addition in the database

    # Read all the text files from the local directory, returns the .txt files list
    def read_file_list(self):
        # if os._exists(self.dirpath + "/ConvertedTexts"):
        text_file_list = []  # A list which will be used to hold the text files
        txt_folder = self.dir_path + "\\ConvertedTexts"
        doc_folder = self.dir_path + "\\Files"
        # For MACbOOK
        # txt_folder = self.dir_path + "/ConvertedTexts" # So that this may work on the mac as well
        if os.path.exists(txt_folder):  # Checking the directory
            # print("We are checking the path which exists")
            # print("Checking here")
            for filename in os.listdir(txt_folder):
                # Specifying the folder and looping through the folder
                if filename.endswith('.txt'):  # extension of the text files
                    # Inserting into the document location for the usage of the database
                    self.data_base.insert_into_doc(doc_folder + "\\" + filename[0:-4] + ".docx")  # Adds the doc file in
                    # self.data_base.insert_into_file_(filename, txt_folder + "\\" + filename,)
                    print("Found :", filename)  # prints out the file name for seeing the process of the listing
                    text_file_list.append(filename)  # Appends all the file that ends with the txt
                    # print(filename)  # Debugging
                    # print("This is the file name")
                    # pdfFiles.append(self.dir_path + "\\Files\\" + filename)  # Adding the pdf complete location in the list.
                    # pdfFiles.append(self.dir_path + "/Files/" + filename)  # Adding the pdf complete location in the list.
                else:
                    print("There was no filed with the .txt extension !")
                    print("Run the FilesToText.py first and then come back")
                    exit(0)  # Exit to be True closes the program
            return text_file_list  # this returns the text file list

    # reads each files data and convert the specified file in the format of the dictionary (hashmap in java)
    # where the file name is the key , and the value is the data in it
    def read_files_data(self, list_of_files):
        # MAC : txt_folder = self.dir_path + "/ConvertedTexts"
        txt_folder = self.dir_path + "\\ConvertedTexts"  # Taking in the folder which needs to be taken as input!
        file_datadictionary = {}  # Creating a dictionary for holding in the file values for the specified person
        for file_name in list_of_files:
            # For mac :
            # filepath = txt_folder + "/" + file_name # For having the file nae
            filepath = txt_folder + "\\" + file_name  # Creating the files name for the specified folder
            print(filepath)
            file_reader = open(filepath, "r")  # Reads each file's data
            file_data = file_reader.readlines()  # Reads all the line in the file
            print("Reading from file : ", file_name)
            file_data = str(file_data).replace("b'", "")  # Filterning
            file_datadictionary[file_name] = str(file_data).lower()
            # Adding in the key value pairs in the form of a dictionary as a file
        return file_datadictionary  # returning the data dictionary to the main file .

    def processfiledata(self, datavalues, file):
        list_of_keywords = ["work experience", "qualification", "education", "certification", "references",
                            "extracurricular",
                            "skill"]  # These are the list of keywords which will be used to find the valeus
        indexed_spliting = []  # Finding the index of the values
        total_check = 0  # Debugging
        CV_data_dict = {}  # This will hold the final dicitonary of (all keywords : value strings)
        for kw in list_of_keywords:
            # datavalues = str(datavalues)
            # lines = datavalues.split("\n")
            counter = 1
            # for line in lines:
            if str(datavalues).__contains__(kw):
                # print("Found kw in line :", kw)
                indexed_spliting.append([int(datavalues.index(kw)), kw])
                # Adds the index of the each keyword to get the desired and finds the index of those wit hthe keyword
                # print(datavalues.index(kw))
                total_check += 1


        if total_check == 0:
            print("None of the keyword found in filedata")
            return  # Returns to the main function as the file is not required to be parsed
            # print(indexed_spliting)
        indexed_spliting = sorted(indexed_spliting)  # Sorting on the basis of the provided the indexes
        counter = 0
        for i in indexed_spliting:  # Checking the indexes splitting 2D lists
            print("Processing ...")  # Debugging
            if counter == len(indexed_spliting) - 1:  # for the last element , we will go till the end
                print(i[0], i[1], len(datavalues) - 1)
                # if this is the last found index, you have to go till the last.
                CV_data_dict[i[1]] = datavalues[i[0] + len(i[1]):]
            else:
                print(i[0], i[1], indexed_spliting[counter + 1][0])
                CV_data_dict[i[1]] = datavalues[i[0] + len(i[1]):indexed_spliting[counter + 1][0]]  # Indexing the stuff
            counter += 1
        all_keys = CV_data_dict.keys()  # this gets all the keys from the dictionary
        if 'education' not in all_keys:
            CV_data_dict['education'] = "None"
        if 'qualification' not in all_keys:
            CV_data_dict['qualification'] = "None"
        if 'certification' not in all_keys:
            CV_data_dict['certification'] = "None"
        if 'work experience' not in all_keys:
            CV_data_dict['work experience'] = "None"
        if "skill" not in all_keys:
            CV_data_dict['skill'] = "None"

        print("*-----------------------------------------------------------*")
        file_id = self.db.select_id_from_file_(file)
        self.db.insert_into_file_data(file_id, CV_data_dict["qualification"], CV_data_dict["education"],
                                      CV_data_dict["skill"], CV_data_dict["certification"],
                                      CV_data_dict["work experience"])
        self.file_data_id = self.db.select_id_from_file_data(file_id)  # Getting the file_data_id from the file_id
        return CV_data_dict  # Returns the CV_data_dictionary to the called function

    # Will be used to display the data dictionary , just for debugging
    def display_text_keyvalue(self, data_dictionary):  # looping through the data dictionary
        for k, v in data_dictionary.items():
            print("Key :" + str(k), ":\n VALUE :" + str(v))  # printing the data for the file

    def parse_all_files(self):
        file_list = self.read_file_list()  # gets all the txt files from the specifed folder
        data_dictionary = self.read_files_data(file_list)  # reads the data and returns teh file
        Master_datadictionary = {}
        for file in file_list:
            Master_datadictionary[file] = self.processfiledata(data_dictionary[file], file)
            # This adds in all the data dictnionary in the file
        # print(Master_datadictionary) # This prints the master Data Dictionary at the end
        return Master_datadictionary

    def additional_filter(self, master_dictionary):
        # master dictionary -- > {Name : {Field : Value}  # In General
        for filename, filedata in master_dictionary.items():
            # Name : TextDictionary
            if filedata is not None:
                # If the file data is not applicable
                for field, text in filedata.items():  # iterating through the items
                    # Field : Value
                    print(field, text)  # Debugging !
                    if field == "education":
                        print("parsing educations")
                        print("*" * 50)
                        print(text)
                        edu_dict = self.parse_education(text)  # calls in the parse education function
                        if edu_dict is not None:
                            for filter_edu_name, Filter_data in edu_dict.items():
                                # This will return the Filter id from the filtered database !!!!!!
                                filter_edu_id = self.db.select_id_from_filter_education(filter_edu_name)
                                self.db.insert_into_brief_education(Filter_data,
                                                                    filter_edu_id)  # INSERTION OF THE FILTER ID
                                be_id = self.db.select_id_from_brief_education(Filter_data)  # This gets teh Brief ID !
                                self.db.insert_into_res_education(self.file_data_id,
                                                                  be_id)  # this inserts into the breof education !
                                # THE INSERTION OF THE DATABASE WAS DONE USING THE FOREIGN KEY AS WELL AS THE FILTER ONE's
                        master_dictionary[filename][field] = edu_dict
                    elif field == "skills":  # If field is skills
                        print("Parsing skills..")
                        print("*" * 50)
                        sk_dict = self.parse_skills(text)
                        if sk_dict is not None:
                            '''LOOPING THROUGH THE EACH DICTIONARY IN THE NAMES AND ADDING IN THE DATABASE'''
                            for filter_skill_name, filter_data in sk_dict.items():
                                filter_skill_id = self.db.select_id_from_filter_skill(filter_skill_name)
                                self.db.insert_into_brief_skill(filter_data, filter_skill_id)
                                bs_id = self.db.select_id_from_brief_skill(filter_data)  # This gets the filter
                                self.db.insert_into_res_skill(self.file_data_id,
                                                              bs_id)  # inserting the brief skill and others
                                # Inserting in to the table of the brief skills , wherer the values are inserted

                        master_dictionary[filename][field] = sk_dict
                        # Calls in the parse skills function
                    elif field == "certification":
                        print("Parsing certifications")
                        print("*" * 50)
                        pc_dict = self.parse_certifications(text)
                        if pc_dict is not None:
                            for filter_certificate_name, filter_certificate_data in pc_dict.items():
                                filter_certificate_id = self.db.select_id_from_filter_certification(
                                    filter_certificate_name)
                                # The above lines gets the certification id from the filter_certificate_id
                                self.db.insert_into_brief_certification(filter_certificate_data, filter_certificate_id)
                                bc_id = self.db.select_id_from_brief_certification(
                                    filter_certificate_data)  # This gets the Filter Certification Data id
                                self.db.insert_into_res_certification(self.file_data_id,
                                                                      bc_id)  # This inserts into the data ! !
                                '''THE ABOVE ADDS INTO THE BRIEF CERTIFICATION -- '''
                        master_dictionary[filename][field] = pc_dict  # Parsed Dictionary value is being replaced
                        # Calls the parse certification function
                    elif field == "work experience":
                        print("Parsing work experiences ")
                        print("*" * 50)
                        pwe_dict = self.parse_workexperience(text)
                        if pwe_dict is not None:
                            for filter_we_name, filter_we_data in pwe_dict.items():
                                filter_we_id = self.db.select_id_from_filter_work_experience(filter_we_name)
                                self.db.insert_into_brief_work_experience(filter_we_data,
                                                                          filter_we_id)  # Inserting in to the we data .
                                fwe_id = self.db.select_id_from_brief_work_experience(
                                    filter_we_data)  # This is the Getting of the ID from the Brief WOrk experience
                                self.db.insert_into_res_work_experience(self.file_data_id,
                                                                        fwe_id)  # This is the insertion to the table
                        master_dictionary[filename][field] = pwe_dict
                        # Parsed Work experience dictionary for the specified person
                        # Calls in the work Experience Function
                    elif field == "qualification":
                        print("Parsing qualification ! ")
                        print('*' * 50)
                        qual_dict = self.parse_qualification(text)
                        if qual_dict is not None:
                            for filter_qual_name, filter_qual_data in qual_dict.items():
                                filter_qual = self.db.select_id_from_filter_qualification(filter_qual_name)
                                self.db.insert_into_brief_qualification(filter_qual_data, filter_qual)
                                # Inserting into filter qualification
                                bq_id = self.db.select_id_from_brief_qualification(filter_qual_data)
                                self.db.insert_into_res_qua(self.file_data_id, bq_id)
                                # this is the insertion of the bd iq
                                # Inserting in to the filter Qualification

                    else:
                        print("You should have additional filters in the next increments here !!")
            else:
                print("The File", filename, " has no data :", filedata)  # If the file parsed has no data in it
                continue
        return master_dictionary  # Returns the master dictionary to the main function ! as well

    def advanced_parse_list(self, text, list_of_keywords):
        list_of_keywords = list_of_keywords  # Just a uniaray operation
        datavalues = text  # Just for coping the data from the education text parsed
        indexed_spliting = []  # This is a list which will be used to hold the indexes of the data .
        dictionary = {}  # This will be the education dictionary which will be added in the specified keyword
        total_check = 0  # Intializating the total check to be zero
        counter = 0  # intialization the counter to be queal 0
        for kw in list_of_keywords:  # looping through the list of keywords
            counter += 1  # Incrementing the counter just to check the occurence of words
            # for line in lines:
            if str(datavalues).__contains__(kw):
                # print("Found kw in line :", kw)
                indexed_spliting.append([int(datavalues.index(kw)), kw])
                # Adds the index of the each keyword to get the desired and finds the index of those wit hthe keyword
                # print(datavalues.index(kw))
                total_check += 1

        if total_check == 0:
            print("None of the keyword found in filedata")
            return  # Should return none # datavalues
            #  Returns to the main function as the file is not required to be parsed
        indexed_spliting = sorted(indexed_spliting)  # Sorting on the basis of the provided the indexes
        counter = 0  # Counter = 0 again
        for i in indexed_spliting:  # Checking the indexes splitting 2D lists
            print("Processing ...")  # Debugging
            if counter == len(indexed_spliting) - 1:  # for the last element , we will go till the end
                print(i[0], i[1], len(datavalues) - 1)
                # if this is the last found index, you have to go till the last.
                dictionary[i[1]] = datavalues[i[0] + len(i[1]):]
            else:
                print(i[0], i[1], indexed_spliting[counter + 1][0])
                dictionary[i[1]] = datavalues[i[0] + len(i[1]):indexed_spliting[counter + 1][0]]
            counter += 1
        return dictionary  # Returns the dictionary

    # The below function will be used to parse in the data in the education
    def parse_education(self, edu_dict):
        list_of_keywords = self.education_list
        print(self.education_list)
        text = edu_dict
        edu_dictionary = self.advanced_parse_list(text, list_of_keywords)
        print("Found education inner most data as : ", edu_dictionary)  # Debugging purposes
        return edu_dictionary

    def parse_skills(self, skills_dict):
        list_of_keywords = self.skills_list  # Skills set
        text = skills_dict  # Text replacement
        skills_dict = self.advanced_parse_list(text, list_of_keywords)
        # passes in the list of keywords and well as the text
        # Get dictionary in return
        # print(skills_dict)  # Debugging
        print("Found the skills inner most data matched with :", skills_dict)
        return skills_dict

    def parse_certifications(self, cert_dict):
        list_of_keywords = self.certification_list
        # print(cert_dict)  # Debugging
        text = cert_dict  # just replacing the naming convetion for the user ease
        cert_dict = self.advanced_parse_list(text, list_of_keywords)
        #print("Found the inner most certification data matched with: ",len(cert_dict))  # prints out the certification list
        return cert_dict

    def parse_qualification(self, qual_dict):
        list_of_keywords = self.qualification_list
        text = qual_dict  # Just replacement
        qual_dict = self.advanced_parse_list(text, list_of_keywords)  # Calls in the advanced parsing function
        # print("found the qualification inner most data", len(qual_dict))
        return qual_dict  # returning the converted dictionary

    def parse_workexperience(self, we_dict):
        list_of_keywords = self.workexperience_list  # This intializes with the works experience list
        # Type in other keywords as well
        text = we_dict
        we_dict = self.advanced_parse_list(text, list_of_keywords)
        print("Found the work experience inner most data", we_dict)
        return we_dict

    def master_print(self, masterdictionary):
        for filename, filedata in masterdictionary.items():  # File name : Filedata dictionary
            if filedata is not None and filedata != "":
                print("Processing the file name :", filename)
                print("Processing the file data : ", filedata)
                for field, innerdata in filedata.items():  # field : Innerdata dictionary:
                    if innerdata is not None and innerdata != "":
                        print("processing Field", field)
                        print("inner data is :", innerdata)
                        if type(innerdata) == dict:  # If there is ane
                            for innerfield, innermostdata in innerdata.items():
                                print("Inner Field is :", innerfield)  # prints the field name of the specified data !
                                print("Inner most data is :", innermostdata)  # prints the innner most data
                        else:  # If the inner most is not a dictionary than it would go in here.
                            # print("inner data is :",innerdata)
                            print("Inner most data is  : None")  # if the inner field is none
                    else:
                        print("The inner data is None or Empty", innerdata)
            else:
                print("no filedata", filename)


def test():
    print("Testing the function ")
    TF = TextFilter(additional_list_input=True)  # Creating the object of the text file !!
    # file_list = TF.read_file_list()  # gets all the txt files from the specifed folder
    # data_dictionary = TF.read_files_data(file_list)  # reads the data and returns teh file
    # print(file_list)
    ms_data = TF.parse_all_files()  # parsing all the files for the data
    # try:
    ms_complete = TF.additional_filter(ms_data)  # this returns the master most dictionary
    # except Exception as ex:
    #    print("Unable to parse in there is an error in the master dictionary parsing ", ex)
    # Just of the formating of the data.
    print("*" * 100)
    print("-" * 100)
    TF.master_print(ms_complete)
    # for file in file_list:
    # TF.processfiledata(data_dictionary[file_list])  # Parses the specified data file
    # TF.display_text_keyvalue(data_dictionary)
    # print(data_dictionary[file_list[4]])  # This is a test case , for all the dictin
    # for file in file_list:
    #   TF.processfiledata(data_dictionary[file])  # passed in the function and called


test()  # Debugging !
