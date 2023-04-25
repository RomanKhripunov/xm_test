### Before start
Make sure you have installed Python version **>=3.10**
(seems that all will work fine and with older versions, but still I used 3.10.6).  
Also, I've run tests on **Mac OS**. Hope all will work fine on the other OS.

### Get code
In terminal go to directory you want to download code and run next command:
> git clone https://github.com/RomanKhripunov/xm_test.git

### Prepare venv
Then go to created directory.
Run make init command to create venv and install some dependencies:
> make init

After that activate created venv in your terminal
> source venv/bin/activate

### Install browsers
I recommend you to install all required browsers to the custom folder.
To reach this goal you can simply define environment variable:
> export PLAYWRIGHT_BROWSERS_PATH="$(pwd)/pw-browsers" 

_*_ `pw-browsers` directory is added to `.gitignore`.  
_*_ remember, that the added variable lives only in current terminal session.

After that in the same terminal session run next command:
> playwright install

This command will install basic browsers using by playwright into the `PLAYWRIGHT_BROWSERS_PATH` path.
But keep in mind that Playwright uses open source Chromium builds. 
It means that you have to install Google Chrome explicitly. Also, it uses different folder for such browsers.
I offer to use only basic open-source browsers here.

### Run tests
To run tests use next command:
> pytest --alluredir=allure_results --browser chromium --headed ./tests

_*_ You are able to specify a few browser, just add one more argument `--browser firefox`  
_*_ Argument `--headed` tells playwright to run UI browser. 
There is some problem with user-agent in headless mode which I haven't resoled.  

### Get report
Pytest only prepare data for report, but to finally get it you have to use allure command line tool.  
You can install it via, e.g. brew (Mac OS):
> brew install allure

And then run command to generate report from previously produced data:
> make report

It will generate and open browser with report preview.