## SHAN API Server Configuration
1)  Open **powershell** in the same command window by typing the following command in command prompt:-
    ```bash
    > powershell
    ```


2)  Install Chocolatey by typing the following command in powershell (wait till the command finishes):-
    ```bash
    > Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```

    Now, exit and reopen powershell (otherwise choco will fail):-
    ```bash
    > exit
    > powershell
    ```

    Now, in powershell set alias for choco by typing the following command:-
    ```bash
    > Set-Alias -Name choco -Value 'C:\ProgramData\chocolatey\choco.exe'
    ```


3)  Install **python** (version 3.8.7) and **git** by typing the following commands in powershell:-
    ```bash
    > choco install python --version=3.8.7 -y
    > choco install git -y
    ```


4)  Move to **C:\Program Files** directory, download NSSM and untar zip file by typing the following commands in powershell:-
    ```bash
    > cd 'C:\Program Files'
    > wget https://nssm.cc/release/nssm-2.24.zip -OutFile nssm-2.24.zip
    > tar -xvf nssm-2.24.zip
    ```


5)  Connect to github account by creating a personal access token using following steps:-

    a) Login to your github account.

    b) Verify your email address (if it hasn't been verified yet) using following steps :

       I) In the upper-right corner of any page, click your profile photo, then click **Settings**.

       ![GitHub1](/Docs/images/git-1.png)

       II) In the left sidebar, click **Emails**.

       ![GitHub2](/Docs/images/git-2.png)

       III) Under your email address, click **Resend verification email**.

       ![GitHub3](/Docs/images/git-3.png)

       IV) GitHub will send you an email with a link in it. After you click that link, you'll be taken to your GitHub dashboard and see a confirmation banner.

       ![GitHub4](/Docs/images/git-4.png)

    c) In the upper-right corner of any page, click your profile photo, then click **Settings**.

    ![GitHub5](/Docs/images/git-5.png)

    d) In the left sidebar, click **Developer settings**.

    ![GitHub6](/Docs/images/git-6.png)

    e) In the left sidebar, click **Personal access tokens**.

    ![GitHub7](/Docs/images/git-7.png)

    f) Click **Generate new token**.

    ![GitHub8](/Docs/images/git-8.png)

    g) Give your token a descriptive name.

    ![GitHub9](/Docs/images/git-9.png)

    h) Select the scopes, or permissions, you'd like to grant this token. To use your token to access repositories from the command line, select **repo**.

    ![GitHub10](/Docs/images/git-10.png)

    i) Click **Generate token**.

    ![GitHub11](/Docs/images/git-11.png)

    j) Click paste icon to copy the token to your clipboard. For security reasons, after you navigate off the page, you will not be able to see the token again.

    ![GitHub12](/Docs/images/git-12.png)


6)  Go to powershell and clone the **shan-api-server** repository to **C:\Program Files** folder using the following commands (create alias for git first):-
    ```bash
    > Set-Alias -Name git -Value 'C:\Program Files\Git\bin\git.exe'
    > cd 'C:\Program Files'
    > git clone https://github.com/shantanu73/shan-api-server.git
    Username: <your_username>
    Password: <your_token>
    ```

    **Delete** your **personal access token** after cloning the repository.


7)  Now, go to directory **shan-api-server** and install python requirements using the following commands
    (create alias for python first):-
    ```bash
    > Set-Alias -Name python -Value 'C:\Python38\python.exe'
    > cd 'C:\Program Files\shan-api-server'
    > python -m pip install -r requirements.txt
    ```


8)  Now, configure the app:-

    a) Open **eligibility_groups_mapping.cfg** file using command :
       ```bash
       > notepad eligibility_groups_mapping.cfg
       ```

       And, add the following lines in **eligibility_groups_mapping.cfg** as mentioned below :
       ```bash
       <eligibility group 1>:<admin group 1>
       <eligibility group 2>:<admin group 2>
       <eligibility group 3>:<admin group 3>
       ```

       Now save the file and close notepad.

    b) Open **app_config.py** file using command :
       ```bash
       > notepad app_config.py
       ```

       And, edit the following variables in **app_config.py** as mentioned below :
       ```bash
       SHAN_SERVER_SECRET_KEY = "<your SHAN server secret key, should have same value as configured in SHAN WEB server>"
       ```

       Now save the file and close notepad.

    c) Run the following commands to initialize log and certificates folders and exit powershell :
       ```bash
       > python app.py
       > exit
       ```


9)  Now, to give service account, the permissions of folders **shan-api-server**, folder of python executable, **nssm-2.24**,
    and to install & run service **SHAN_API_SERVER** and to open port **443**:-

    Go to **Scripts** folder and open **permissions.bat**:
    ```bash
    > cd "C:\Program Files\shan-api-server\Scripts"
    > notepad permissions.bat
    ```

    Modify **SHAN_SERVICE_ACCOUNT** variable in **permissions.bat**:
    ```bash
    set SHAN_SERVICE_ACCOUNT="<domain>\<service account>$"
    ```

    Now, run **permissions.bat** file using the following command:-
    ```bash
    > "C:\Program Files\shan-api-server\Scripts\permissions.bat"
    ```



## Certificate creation and renewal using Win-ACME
1)  To install **Win-ACME** in a new directory **win-acme**, run the following command:-
    ```bash
    > "C:\Program Files\shan-api-server\Scripts\winacme_config.bat"
    ```


2)  For creating certificates and configuring it's auto renewal:-

    Go to **Scripts** folder and open **install_cert.bat**:
    ```bash
    > cd "C:\Program Files\shan-api-server\Scripts"
    > notepad install_cert.bat
    ```

    Modify **CERT_DOMAIN**, **CERT_EMAIL** & **CERT_TOKEN** variables in **install_cert.bat**:
    ```bash
    set CERT_DOMAIN="<your domain>"
    set CERT_EMAIL="<your email address>"
    set CERT_TOKEN="<your api token>"
    ```

    Now, run the following command in the command line:-
    ```bash
    > "C:\Program Files\shan-api-server\Scripts\install_cert.bat"
    ```


3)  Now your API server is up and running.
    Refer to **C:\Program Files\shan-api-server\logs** folder to access log files.
