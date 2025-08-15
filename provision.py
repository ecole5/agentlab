
from __future__ import print_function
import time
import argparse
import time
import cmlapi
from cmlapi.rest import ApiException
from pprint import pprint
import os

num_projects = int(os.environ["NUM_USERS"])

# Create an instance of the API client
api_instance = cmlapi.default_client()


projects = api_instance.list_projects().projects        
        
# Loop to create multiple projects
for i in range(1, num_projects + 1):
    try:
        project_name = f"AgentLab {i}"
        print(f"Creating project: {project_name}")
        
        target_project = next((p for p in projects if p.name.startswith(project_name)), None)
        
        if target_project != None:
          raise ValueError("The project already exists")
          

        # Create the project body with dynamic name
        project_body = cmlapi.CreateProjectRequest(
            name=project_name,
            description="Agent Studio Lab",
            visibility="private",
            template="blank",
            git_url="https://github.com/cloudera/CAI_STUDIO_AGENT"
        )

        # Define the AMP configuration
        amp_body = cmlapi.ConfigurePrototypeRequest(
            run_import_tasks=True,
            runtime_identifier='docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-pbj-workbench-python3.9-standard:2025.06.1-b5',
            execute_amp_steps=True
        )

        # Create AMP request
        body = cmlapi.CreateAmpRequest(project_body, amp_body)

        # Make the API call
        api_response = api_instance.create_amp(body)
        #pprint(api_response)
        print(f"✅ Successfully created: {project_name}\n")
        print(api_response)
        
        
    except (ApiException, ValueError) as e:
        print(f"❌ Exception creating project {project_name}: {e}\n")


time.sleep(30)
     

