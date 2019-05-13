*** Settings ***
Library                      EmailProcessLibrary

*** Test Cases ***

Should Be Logged In To Outlook
    [Tags]                   Should Be Logged In To Outlook
    Should Be Logged In To Outlook  kelemenandras11@outlook.com

Should Be Logged In To Outlook 2
    [Tags]                   Should Be Logged In To Outlook
    Run Keyword And Expect Error  OutlookException*
        ...  Should Be Logged In To Outlook  nonexisting@outlook.c

Create New Email
    [Tags]                   Create New Email  Set Email Text
    Run Keyword And Expect Error  *Create New Email*
        ...  Set Email Text  test

Create New Email 2
    [Tags]                   Create New Email  Set Email Text
    Create New Email

Set Email Text
    [Tags]                   Set Email Text
    Set Email Text
    ...  line 1
    ...  line 2
    ...  line 3

Set Email Subject
    [Tags]                   Set Email Subject
    Set Email Subject
    ...  test_subject

Add Attachment
    [Tags]                   Add Attachment
    Add Attachment
    ...  test_files//picture.png

Send Email To
    [Tags]                   Send Email To
    Send Email To            kelemenandras11@outlook.com
    Sleep                    10s

Last Received Subject Should Be
    [Tags]                   Last Received Subject Should Be
    Wait Until Keyword Succeeds  50sec  1sec  Last Received Subject Should Be  test_subject

Read Last Received Email
    [Tags]                   Read Last Received Email  Last Received Subject Should Be
    ${text}=                 Read Last Received Email
    Last Received Subject Should Be  test_subject
    Should Contain           ${text}  line 2

Read Last Email From
    [Tags]                   Read Last Email From
    Read Last Email From     kelemenandras11@outlook.com

Last Sent Subject Should Be
    [Tags]                   Last Sent Subject Should Be
    Wait Until Keyword Succeeds  30sec  1sec  Last Sent Subject Should Be  test_subject

Get Email
    [Tags]                   Get Email
    ${mail}=                 Get Email  kelemenandras11@outlook.com  test_subject
    Should Not Be Equal      ${mail}  ${None}

Get Email 2
    [Tags]                   Get Email
    ${mail}=                 Get Email  nonexisting@outlook.com  test_subject
    Should Be Equal          ${mail}  ${None}

Save Attachments
    [Tags]                   Save Attachments  Get Email
    ${mail}=                 Get Email  kelemenandras11@outlook.com  test_subject
    Save Attachments         ${mail}  test_files

Get Email Text
    [Tags]                   Get Email Text  Get Email
    ${mail}=                 Get Email  kelemenandras11@outlook.com  test_subject
    ${text}=                 Get Email Text  ${mail}
    Should Contain           ${text}  line 3

Get Email Subject
    [Tags]                   Get Email Subject  Get Email
    ${mail}=                 Get Email  kelemenandras11@outlook.com  test_subject
    ${subject}=              Get Email Subject  ${mail}
    Should Be Equal          ${subject}  test_subject

Get Email Time
    [Tags]                   Get Email Time  Get Email
    ${mail}=                 Get Email  kelemenandras11@outlook.com  test_subject  2019.03.10  2019.03.10
    ${date}=                 Get Email Time  ${mail}
    ${python_version}=       Evaluate  sys.version_info[0]  modules=sys
    Run Keyword If  ${python_version}==2
        ...  Should Be Equal As Strings  ${date}  03/10/19 23:32:45
    Run Keyword If  ${python_version}==3
        ...  Should Be Equal As Strings  ${date}  2019-03-10 23:32:45+00:00

Get Email Sender
    [Tags]                   Get Email Sender  Get Email
    ${mail}=                 Get Email  kelemenandras11@outlook.com  test_subject
    ${sender}=               Get Email Sender  ${mail}
    Should Be Equal As Strings  ${sender}  kelemenandras11@outlook.com
