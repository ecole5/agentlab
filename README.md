Steps for setting up this lab.

1. Provison a CAI workbench on AWS with one m5.4xlarge instace for each lab user. Make sure it is the minimum of the autoscale range so that you do not face scalling delay.

2. Within the new or existing workbench to be used import the provision.py script into an empty project and create a session to run it. Change the num_projects variable before you run to the number of particapents. 

3. Provision a CAI Inference service with GPU worker of type g6e.12xlarge for each replica of the LLM you will deploy. Make sure the volume size is at least 500gb per instance. ach replica can handle about 200 requests per second. You should have at least two for HA in case one crashes.

4. Import the Llama 3.3 70B param model optimized for 4xL40s from model hub into a model registry.

5. Deploy a model endpoint called AgentStudioHoL using the model from the registry using the correct gpu worker instance we added before.
 
6. The provison.py will create an AgentLab CAI group and give that group admin rights over each project, ensure that all users of the lab are part of this groupor they will have permission issues.

