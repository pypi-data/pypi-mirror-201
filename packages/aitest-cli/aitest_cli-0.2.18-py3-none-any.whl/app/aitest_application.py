from datetime import *
import click
import os
import requests
import json
from sys import *
import base64
from prettytable import PrettyTable
import time


# Command Group
@click.group(name='configure')
def configure():
    pass


def get_access_token(profile, client_id, client_secret_id):
    if profile == 'dev':
        access_token_api = "https://login-marxeed-dev.auth.us-east-1.amazoncognito.com/oauth2/token"
    else:
        access_token_api = "https://login.aaic.cc/oauth2/token"

    str_to_encode = client_id + ":" + client_secret_id
    encoded_str = base64.b64encode(str_to_encode.encode('utf-8'))
    encoded_value = encoded_str.decode('utf-8')
    data = {'grant_type': 'client_credentials', 'scope': 'aitestpublic/runtest'}
    access_token_api_headers = {"Authorization": f"Basic {encoded_value}",
                                "content-type": "application/x-www-form-urlencoded"}
    token = requests.post(access_token_api, headers=access_token_api_headers, data=data)
    if token.status_code == 400:
        click.echo('\n"error" : "Please add your valid Client ID and Client Secret ID ."\n')
        exit()
    else:
        token_data = token.json()

    access_token = token_data["access_token"]
    return access_token


# Creating command
@configure.command(name='configure')
@click.option('--env', '-e', required=False)
def configure(env):
    """If this command is run with no arguments, you will be prompted for configuration values such as your User ID, Client ID and Client Secret ID.If your configure file does not  exist
       (the default location is ~/.aitest/prod/configure), the aitest CLI will create it for you.To keep an existing value, hit enter when prompted for the value.
        Default Environment is PROD
       To save the configurations , you can run below command:\n
       aitest configure -e [aitest enviornment (dev/prod)]

    """
    user_id = input('Enter aiTest User Identifier :')
    client_id = input('Enter Client ID :')
    client_secret_id = input('Enter Client Secret ID :')

    if env and env == 'dev':
        profile = 'dev'
    else:
        profile = 'prod'

    folder_path = os.path.join(os.path.expanduser('~'), (".aitest/{}".format(profile)))
    folder_exist = os.path.exists(folder_path)
    if not folder_exist:
        os.mkdir(folder_path)
        fd = open(os.path.join(folder_path, "configure"), 'w')

        if user_id:
            fd.write("user_id = " + user_id + "\n")
        else:
            fd.write("user_id = " + " " + "\n")

        if client_id:
            fd.write("client_id = " + client_id + "\n")
        else:
            fd.write("client_id = " + " " + "\n")

        if client_secret_id:
            fd.write("client_secret_id = " + client_secret_id + "\n")
        else:
            fd.write("client_secret_id = " + " " + "\n")
        fd.close()
    else:
        file_path = os.path.join(os.path.expanduser('~'), (".aitest/{}".format(profile)), "configure")
        file = open(file_path, "r")
        content = file.read()
        data = content.split("\n")
        ex_user_id = data[0].split(" = ")[1]
        ex_client_id = data[1].split(" = ")[1]
        ex_client_secret_id = data[2].split(" = ")[1]

        fd = open(os.path.join(folder_path, "configure"), 'w')
        if user_id:
            fd.write("user_id = " + user_id + "\n")
        else:
            fd.write("user_id = " + ex_user_id + "\n")

        if client_id:
            fd.write("client_id = " + client_id + "\n")
        else:
            fd.write("client_id = " + ex_client_id + "\n")

        if client_secret_id:
            fd.write("client_secret_id = " + client_secret_id + "\n")
        else:
            fd.write("client_secret_id = " + ex_client_secret_id + "\n")
        fd.close()


# Command Group
@click.group(name='run')
def run():
    pass


# Creating command
@run.command(name='run')
@click.option('--testrun_id', '-id', required=True)
@click.option('--wait_time', '-w', required=False)
@click.option('--git_pass', '-p', required=False)
@click.option('--branch', '-b', required=False)
@click.option('--testrun_name', '-n', required=False)
@click.option('--env', '-e', required=False)
def run(testrun_id, git_pass, wait_time, branch, testrun_name, env):
    """If this command is run with testrun id as an argument, aitest CLI will create new test for you with same configuration of provided testrun id.Enter git password with -p only if you used git url of the automation code for creating the test otherwise no need to enter git password.
       Enter the waiting time in minutes with -w as an argument, To wait for looking the testrun status in given time.\n
       Default Environment is PROD
       Enter branch name with -w as an [optional] argument to run aiTest CLI on specific branch
       Enter testrun name with -n as an [optional] argument to rename the testrun
       To re-run the test, you can run below command:\n
       aitest run -id [testrun id] -p [git password] -w [wait_time] -b [branch_name] -n [testrun_name] -e [aitest enviornment (dev/prod)]
    """
    if env and env == 'dev':
        profile = 'dev'
    else:
        profile = 'prod'
    try:
        if "USER_ID" in os.environ and "CLIENT_ID" in os.environ and "CLIENT_SECRET_ID" in os.environ:
            user_id = os.environ["USER_ID"]
            client_id = os.environ["CLIENT_ID"]
            client_secret_id = os.environ["CLIENT_SECRET_ID"]
        else:
            file_path = os.path.join(os.path.expanduser('~'), (".aitest/{}".format(profile)), "configure")
            file = open(file_path, "r")
            content = file.read()
            data = content.split("\n")
            user_id = data[0].split(" = ")[1]
            client_id = data[1].split(" = ")[1]
            client_secret_id = data[2].split(" = ")[1]
    except:
        click.echo('\n"error" : "Please add your valid USER_ID, CLIENT_ID and CLIENT_SECRET_ID in configure file."\n')
        exit()

    access_token = get_access_token(profile, client_id, client_secret_id)

    headers = {"Authorization": f"Bearer {access_token}", "aiTest-User-Identifier": user_id}

    if profile == 'dev':
        base_url = "https://api.aitest.dev.appliedaiconsulting.com/public/v1/testrun/load_test"
    else:
        base_url = "https://api.aitest.appliedaiconsulting.com/public/v1/testrun/load_test"

    dd = {"testrun_id": testrun_id, "git_password": git_pass, "git_branch": branch, "testrun_name": testrun_name}

    payload = json.dumps(dd)

    res2 = requests.post(base_url, data=payload, headers=headers)
    if res2.status_code == 401:
        click.echo('\n"error" : "Please add your valid User ID."\n')
        exit()
    if res2.status_code == 200:
        res_body = res2.json()
        try:
            test_data = json.loads(res_body['body'])
        except:
            click.echo(res_body)
            exit(-1)
        project_id = test_data['load_test_details']['project_id']
        test_type = test_data['load_test_details']['test_type']
        testrun_id_new = test_data['load_test_details']['testrun_id']
        if test_type == 'functional_test':
            sub_link = 'multi-browser-test'
        elif test_type == 'load_test':
            sub_link = 'performance-test'
        else:
            sub_link = 'url-test'
        if profile == 'dev':
            aitest_ui = "https://app.aitest.dev.appliedaiconsulting.com/"
        else:
            aitest_ui = "https://app.aitest.appliedaiconsulting.com/"
        testrun_link = aitest_ui + sub_link + "?testrun_id=" + testrun_id_new + "&project_id=" + project_id
        click.echo(
            f"\nTestrun created successfully\nTestrun Name : {test_data['load_test_details']['testrun_name']}\nTestrun ID : {test_data['load_test_details']['testrun_id']}\n")
        click.echo(f"\nTestrun Link: {testrun_link}\n")
        if wait_time:
            click.echo("Testrun is in progress, result will be displayed once it get completed.")
            new_time = datetime.now() + timedelta(minutes=int(wait_time))
            test_status = ""
            
            # while test_status != "completed":
            # sleep time before making status API call
            sleep_time_to_poll_status = 300
            wait_time = int((int(wait_time) * 60) / 10)
            if wait_time < 300:
                sleep_time_to_poll_status = wait_time
                
            while True:
                # get access token for every status call to avoid token expiration
                access_token = get_access_token(profile=profile, client_id=client_id, client_secret_id=client_secret_id)
                headers = {"Authorization": f"Bearer {access_token}", "aiTest-User-Identifier": user_id}

                if (datetime.now().strftime("%H:%M:%S")) >= (new_time.strftime("%H:%M:%S")):
                    click.echo(
                        f"The request is timed out. The testrun is still in progress. To see the status of the testrun, please run command : [ aitest status {test_data['load_test_details']['testrun_id']} ].")
                    exit()
                if profile == 'dev':
                    base_url = f"https://api.aitest.dev.appliedaiconsulting.com/public/v1/testrun_result/status/{test_data['load_test_details']['testrun_id']}"
                else:
                    base_url = f"https://api.aitest.appliedaiconsulting.com/public/v1/testrun_result/status/{test_data['load_test_details']['testrun_id']}"
                status_res = requests.get(base_url, headers=headers)
                status_test_data = status_res.json()
                if status_test_data.get("statusCode") and status_test_data['statusCode'] == 200:
                    body = json.loads(status_test_data['body'])
                    test_status = body['testrun_status']
                    click.echo(f"Test status is: {test_status}\n")
                else:
                    test_status = ""
                if test_status == "completed":
                    break
                # if test_status == "completed":
                #     testrun_status_details = body['testrun_status_details']
                #     table = PrettyTable(
                #         ["browser_name", "browser_version", "test run result id", "status", "time taken"])
                #     click.echo(f"\ntest status : {test_status}\n")
                #     fail_count = 0
                #     for i in testrun_status_details:
                #         if i['testrun_result_status'] == "fail":
                #             fail_count += 1
                #         table.add_row([i['browser_name'], i['browser_version'], i['testrun_result_id'],
                #                        i['testrun_result_status'], i['time_taken']])
                #     click.echo(table)
                #     if fail_count == 0:
                #         click.echo(
                #             "All test cases from this testrun have passed. Please refer above table for more details.")
                #         exit()
                #     else:
                #         click.echo(
                #             f"{fail_count} test cases from this testrun have failed. Please refer above table for more details.")
                #         exit(1)
                # adding a wait time so that we don't make continuous CALLS to status API.
                click.echo(f"Testrun in Progress waiting for {wait_time} seconds to perform next status call..")
                time.sleep(sleep_time_to_poll_status)
                # wait_time = int((int(wait_time) * 60) / 10)
                # if wait_time > 300:
                #     click.echo(f"Testrun in Progress waiting for {wait_time} seconds to perform next status call..")
                #     time.sleep(300)
                # time.sleep(wait_time)
                # click.echo(f"Testrun in Progress waiting for {wait_time} seconds to perform next status call..")

            if test_status == "completed":
                testrun_status_details = body.get('testrun_status_details', [])
                table = PrettyTable(
                    ["browser_name", "browser_version", "test run result id", "status", "time taken"])
                click.echo(f"\ntest status : {test_status}\n")
                fail_count = 0
                for i in testrun_status_details:
                    if i['testrun_result_status'] == "fail":
                        fail_count += 1
                    table.add_row([i['browser_name'], i['browser_version'], i['testrun_result_id'],
                                    i['testrun_result_status'], i['time_taken']])
                click.echo(table)
                if fail_count == 0:
                    click.echo(
                        "All test cases from this testrun have passed. Please refer above table for more details.")
                    exit()
                else:
                    click.echo(
                        f"{fail_count} test cases from this testrun have failed. Please refer above table for more details.")
                    exit(1)

    else:
        click.echo(res2.json())
        exit()


# Command Group
@click.group(name='status')
def status():
    """ status command is use to display the status of particular test.  """
    pass


# Creating command
@status.command(name='status')
@click.option('--testrun_id', '-id', required=True)
@click.option('--env', '-e', required=False)
def status(testrun_id, env):
    """ If this command is run with testrun id as an argument, aitest CLI will display the test details .\n  
        Default Environment is PROD
        To see the status of test , you can run below command:\n
        aitest status -id [testrun_id] -e [aitest enviornment (dev/prod)]
    """
    if env and env == 'dev':
        profile = 'dev'
    else:
        profile = 'prod'
    try:
        if "USER_ID" in os.environ and "CLIENT_ID" in os.environ and "CLIENT_SECRET_ID" in os.environ:
            user_id = os.environ["USER_ID"]
            client_id = os.environ["CLIENT_ID"]
            client_secret_id = os.environ["CLIENT_SECRET_ID"]
        else:
            file_path = os.path.join(os.path.expanduser('~'), (".aitest/{}".format(profile)), "configure")
            file = open(file_path, "r")
            content = file.read()
            data = content.split("\n")
            user_id = data[0].split(" = ")[1]
            client_id = data[1].split(" = ")[1]
            client_secret_id = data[2].split(" = ")[1]
    except:
        click.echo('\n"error" : "Please add your valid USER_ID, CLIENT_ID and CLIENT_SECRET_ID in configure file."\n')
        exit()

    access_token = get_access_token(profile=profile, client_id=client_id, client_secret_id=client_secret_id)

    headers = {"Authorization": f"Bearer {access_token}", "aiTest-User-Identifier": user_id}
    if profile == 'dev':
        base_url = f"https://api.aitest.dev.appliedaiconsulting.com/public/v1/testrun_result/status/{testrun_id}"
    else:
        base_url = f"https://api.aitest.appliedaiconsulting.com/public/v1/testrun_result/status/{testrun_id}"

    status_res = requests.get(base_url, headers=headers)
    if status_res.status_code == 401:
        click.echo('\n"error" : "Please add your valid User ID."\n')
        exit()
    status_test_data = status_res.json()

    body = json.loads(status_test_data['body'])

    test_status = body['testrun_status']

    testrun_status_details = body['testrun_status_details']

    table = PrettyTable(["browser_name", "browser_version", "test run result id", "status", "time taken"])

    click.echo(f"\nTestrun Status : {test_status}\n")
    fail_count = 0
    for i in testrun_status_details:
        if i['testrun_result_status'] == "fail":
            fail_count += 1
        table.add_row([i['browser_name'], i['browser_version'], i['testrun_result_id'], i['testrun_result_status'],
                       i['time_taken']])
    click.echo(table)
    if fail_count == 0:
        click.echo("All test cases from this testrun have passed. Please refer above table for more details.")
        exit()
    else:
        click.echo(f"{fail_count} test cases from this testrun have failed. Please refer above table for more details.")
        exit(1)
