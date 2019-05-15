
#CareAI Playground for the NHS

## User Manual

A demo of the web application can be found at https://nhs-playground.azurewebsites.net/

For the admin account to access the Django admin page with administrative permissions, the username is admin with password admin123.

Users will be prompted with a welcome page firstly, which consists of simple instructions about features of CareAI PlayGround and a navigation bar by which they access Challenges, Solutions, Discussion and Tutorial pages, and the Login and Register buttons will be shown if user has not logged in.

A developer and clinician account can be created via registration on the site although a clinician account has to be approved on the admin page. Hence, for convenience, a developer account can be accessed using username test_developer and password developer123 while the provided clinician account has username test_clinician and password clinician123.

To access the online coding environment of CareAI PlayGround, users should participate in the challenges and click the button on that page to open their JupyterHub page. Then, they can upload the data they need for solution and write down their solutions which can be saved automatically on their own Jupyter Notebook.

## Deployment Manual

First, clone the repo found at https://github.com/nhspg/COMP0016T12 on the local machine. Then, set up an Azure app service to host the Django app:

Create an Azure App Service running Linux on the Azure portal.
At the deployment center for the app, choose to deploy via a GitHub repo with the link provided above.

Then, to set up an Azure SQL database:

Create an Azure SQL database on the Azure portal.
On the database page on the Azure portal, navigate to "Connection Strings" then "ODBC" to get the relevant details to change under "settings.py" database code.
On the local machine's terminal, run the command "python manage.py migrate" to update the connected database.

Finally, to set up a JupyterHub server:

Activate the correct subscription on Azure.
Create a resource group. Azure uses the concept of resource groups to group related resources together. The command in terminal is: az group create \--name=RESOURCE-GROUP-NAME \--location=centralus \ --output table .
Create Cluster and name it using command: "mkdir CLUSTER-NAME" and then " cd CLUSTER-NAME".
Create an ssh key to secure your cluster: ssh-keygen -f ssh-key-CLUSTER-NAME.
Create an AKS cluster using "az aks create --name CLUSTER-NAME \--resource-group RESOURCE-GROUP-NAME \ --ssh-key-value ssh-key-CLUSTER-NAME.pub \--node-count 3 \ --node-vm-size Standard_D2s_v3 \--output table".
Get credentials from Azure for kubectl to work: az aks get-credentials \ --name CLUSTER-NAME \--resource-group RESOURCE-GROUP-NAME \ --output table
Check if your cluster is fully functional: kubectl get node
(The response should list three running nodes and their Kubernetes versions and each node should have the status of Ready)
Make Helm aware of the JupyterHub Helm chart repository using "helm repo add jupyterhub" and then "helm repo update"
Install the chart configured by the config.yaml by running this command from the directory that contains config.yaml: RELEASE=jhub NAMESPACE=jhub helm upgrade --install $RELEASE jupyterhub/jupyterhub \--namespace $NAMESPACE \--version=0.8.0 \ --values config.yaml.
To find the IP used to access the JupyterHub, run the following command: kubectl get service --namespace jhub.
To use JupyterHub, enter the external IP for the proxy-public service in to a browser.

## UCL COMP0016T12

This project was produced by the UCL IXN programme, *UCL COMP0016T12*

### Attributions
* Wei Tan
* Haixiang Sun
* Zixuan Wang

# Licence & Disclaimer

*CareAI Playground* is provided under a AGPLv3 licence and all terms of that licence apply ([AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)]). Use of *CareAI Playground* or the code is entirely at your own risk. Neither the Apperta Foundation nor UCL accept any responsibility for loss or damage to any person, property or reputation as a result of using the software or code. No warranty is provided by any party, implied or otherwise. This software and code is not guaranteed safe to use in a clinical or other environment and you should make your own assessment on the suitability for such use. Installation of any *CareAI Playground* software, indicates acceptance of this disclaimer.

Copyright &copy; Apperta Foundation 2019