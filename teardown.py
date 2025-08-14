  

from __future__ import print_function
import time
import cmlapi
from cmlapi.rest import ApiException
from pprint import pprint
import time

# Set number of projects to launch
num_projects = 30  # change this to how many projects you want to create

# Create an instance of the API client
api_instance = cmlapi.default_client()

try:
    # List all projects
    projects = api_instance.list_projects().projects

    # Loop through the expected project names
    for i in range(1, num_projects + 1):
      target_name = f"AgentLab {i} - ecole"

        # Find the project with this name
      target_project = next((p for p in projects if p.name == target_name), None)
      
      
  
      if target_project:
        project_id = target_project.id
        print(f"Deleting project: {target_name} (ID: {project_id})")
        api_instance.delete_project(project_id)
        print(f"✅ Successfully deleted: {target_name}\n")
      else:
        print(f"⚠️ Project not found: {target_name}")
        

except ApiException as e:
    print(f"❌ Exception occurred: {e}")
        