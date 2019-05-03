*** Settings ***
Library                       EmailProcessLibrary

*** Test Cases ***
Test 1
    ${mail}=         Get Email               kelemenandras11@outlook.com  csatolmany
    Save Attachments          ${mail}        save_folder


Test 2
    ${mail}=         Get Email               kelemenandras11@outlook.com  csatolmany
    Run Keyword And Expect Error     *directory doesn't exist*
        ...  Save Attachments          ${mail}        non_existing_folder


#Test 2
#    Create New Email
#    Set Email Subject  subject22
#    Set Email Text
#    ...  szia2
#    ...  sdfasfd
#    ...  aáeéiíoóöőuúüű
#    ...  AÁEÉIÍOÓÖŐUÚÜŰ
#    ...  Üdv, andrás
#    Add Attachment                  test_files//sam.xlsx  ${CURDIR}//test.robot
#    Send Email To
#    ...  kelemenandras11@gmail.com
#    ...  istvan787@gmail.com
#
#Test 3
#    Read Last Received Email
#    Last Sent Subject Should Be    ketcsatolmany
#
#    Run Keyword And Expect Error     *!=*
#        ...  Last Sended Subject Should Be    no_minta
