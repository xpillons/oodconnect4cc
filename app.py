from flask import Flask, render_template, request, url_for, flash, redirect
import subprocess, yaml, re, socket, json
MyApp = Flask(__name__)
MyApp.config['SECRET_KEY'] = '4b27e55d915941e3ef6b22ea588e3d27df0684d0797fffe9'

@MyApp.route("/",methods=('GET', 'POST'))


def index():
    """
    Handles the main logic for the index route of the web application.

    This function processes form data submitted via a POST request. It performs several checks 
    on the submitted data, including validation and network connectivity checks. If all checks 
    pass, it proceeds to configure the cluster and home directories using the provided data. 
    If any check fails, it redirects back to the index page.

    Returns:
        Response: A redirect to the index page or a rendered template of the index page.
    """
    if request.method == 'POST':
        check = False
        home_check = False
        login_check = False
        sshPort = 22
        nfsPort = 2049
        portCheckTimeout = 2
        status = 0
        
        clusterData = get_form_data() # Get data from HTML
        check = check_form_data(clusterData) # Check Data
        
        if check == False:
            return redirect(url_for('index'))
        else:
            #Check network connection
            home_check = port_check(clusterData['Home_mount_IP'], nfsPort, portCheckTimeout)
            login_check = port_check(clusterData['Login_ip'], sshPort, portCheckTimeout)
            
            if home_check and login_check:
                # Start configuring now that checks are good.
                # Write out vars file
                print("Input data valid progressing")
                # Dump out the variables to a an Ansbile Vars file
                with open('Ansible/vars.yml', 'w') as outfile:
                    yaml.dump(clusterData, outfile)
                status_home = Config_script("Home") # Configure home directories
                if status_home != 0:
                    return redirect(url_for('index'))
                
                status_cluster = Config_script("Cluster") # Configure cluster
                if status_cluster != 0:
                    return redirect(url_for('index'))
                
                flash("Cluster added with settings {}".format(json.dumps(clusterData)),'message')
                flash("Please restart the webserver from the Help menu in Open OnDemand",'message')
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
            
        
    return render_template('index.html',)

def Config_script (mode):
    """
    Uses subprocess to call a bash script that runs Ansible playbooks for configuring OOD.
    The exit code of the script and playbook is captured and checked.

    Args:
        mode (str): String to be passed to the bash script that controls which playbook to run.

    Returns:
        int: The exit code from the subprocess call.

    Side Effects:
        Displays a flash message if the connection fails.
    """
    exit_code = subprocess.call(["./OOD_configure.sh", mode]) # Checks exit code of the ansible
    if exit_code == 0:
        return exit_code
    else:
        flash("Error running Ansible for {} setup. Check log at /var/log/ondemand-nginx/USER/error.log".format(mode),"alert")
        return exit_code

def get_form_data():
    """
    Retrieves form data from an HTML request and creates a dictionary of values.

    This function extracts specific fields from the form data submitted via an HTML request
    and stores them in a dictionary. Additionally, it formats the 'cluster_name' field to 
    ensure it is in a consistent format by replacing any non-alphanumeric characters with 
    hyphens and converting it to lowercase.

    Returns:
        dict: A dictionary containing the following keys:
            - 'cluster_name': The name of the cluster as provided in the form.
            - 'Login_ip': The login IP address as provided in the form.
            - 'Home_mount_IP': The home mount IP address as provided in the form.
            - 'Home_mount_export': The home mount export path as provided in the form.
            - 'escaped_cluster_name': The formatted cluster name with non-alphanumeric
              characters replaced by hyphens and converted to lowercase.
    """
    # Retrieves the form from HTML and creates a dictionary of values the returns this dict.
    clusterData={"cluster_name": request.form['cluster_name'],
                    "Login_ip" : request.form['Login_ip'] ,
                    "Home_mount_IP" : request.form['Home_mount_IP'] ,
                    "Home_mount_export" : request.form['Home_mount_export'],
                    }
    # taken from CycleCloud Slurm, used so names are in the same format as CC
    clusterData['escaped_cluster_name']=re.sub('[^a-zA-Z0-9-]', '-', clusterData['cluster_name']).lower()
    
    return clusterData

def check_form_data(clusterData):
    """
    Validates the form data contained in the clusterData dictionary.

    This function iterates through the key-value pairs in the provided dictionary and checks 
    if any of the values are empty using the check_empty function. If an empty value is found, 
    the function returns False immediately. If all values are non-empty, the function returns True.

    Args:
        clusterData (dict): A dictionary containing form data to be validated.

    Returns:
        bool: False if any value in the dictionary is empty, True otherwise.
    """
    data_state = False
    for k,v in clusterData.items():
        empty = check_empty(k,v)
        if empty:
            return data_state
    else:
        data_state =True
        return data_state


def check_empty(Name, value):
    """
    Checks if a value is blank. If so, it flashes the value on the next refresh and returns False.

    Args:
        Name (str): The name of the field being checked.
        value (str): The value of the field being checked.

    Returns:
        bool: True if the value is blank, False otherwise.
    """
    if value == '':
        flash('{} is required'.format(Name),"alert")
        return True
    return False

def port_check(ip, port, timeout):
    """
    Check if a network port on a given IP address is open within a specified timeout.

    Args:
        ip (str): The IP address to check.
        port (int): The port number to check.
        timeout (float): The timeout duration in seconds for the connection attempt.

    Returns:
        bool: True if the port is open and a connection is established, False otherwise.

    Raises:
        None

    Side Effects:
        Displays a flash message if the connection fails.

    Example:
        >>> port_check('192.168.1.1', 80, 5)
        True
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        flash('Network issue with {} on port {}. Cannot connect'.format(ip, port),"alert")
        return False
    finally:
        s.close()

if __name__ == "__main__":
	MyApp.run()
