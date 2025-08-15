Steps for setting up this lab.

1. Provison a CAI workbench on AWS with one m5.4xlarge instace for each lab user. Make sure it is the minimum of the autoscale range so that you do not face scalling delay.

2. Within the new or existing workbench to be used import this amp. The specified number of projects will be deployed and permission granted ot the lab group and the default keycloak users if they are present. 

3. If you don't have keycloak users synced into the CAI environemnt you need to add your users to the lab group you specfied in the amp setup. 

4. Provision a CAI Inference service with GPU worker of type g6e.12xlarge for each replica of the LLM you will deploy. Make sure the volume size is at least 500gb per instance. ach replica can handle about 200 requests per second. You should have at least two for HA in case one crashes.

5. Import the Llama 3.3 70B param model optimized for 4xL40s from model hub into a model registry.

6. Deploy a model endpoint called AgentStudioHoL using the model from the registry using the correct gpu worker instance we added before.
 