from __future__ import print_function
import re
import cmlapi
from cmlapi.rest import ApiException
import os 

num_projects = int(os.environ["NUM_USERS"])
TEAM = os.environ["TEAM_NAME"]

api = cmlapi.default_client()

def ensure_team_exists(team_name: str) -> None:
    """
    Create the team if it doesn't exist. Swallow common 'already exists'
    variants across CML deployments so the script never crashes on duplicates.
    """
    try:
        print(f"Ensuring team exists: {team_name}")
        api.create_team(cmlapi.CreateTeamRequest(username=team_name))
        print(f"Created team: {team_name}")
    except ApiException as e:
        status = getattr(e, "status", None)
        # Some environments return a message in e.body, others only in str(e)
        text = (getattr(e, "body", None) or str(e) or "").lower()

        # Treat 400/409 or any message that looks like "already exists" as success
        if status in (400, 409) or "exist" in text or "already" in text or "duplicate" in text:
            print(f"Team '{team_name}' already exists (HTTP {status}). Proceeding.")
        else:
            # Log and continue rather than crashing the whole run
            print(f"⚠️ Could not create team '{team_name}' (HTTP {status}): {e}")
            # If you prefer to fail hard on unexpected statuses, replace with: raise

def find_project_by_prefix_bounded(prefix: str):
    """
    Match 'AgentLab N' followed by a word boundary, e.g. 'AgentLab 1' matches
    'AgentLab 1 - ecole' but NOT 'AgentLab 10 ...'.
    """
    pattern = re.compile(rf"^{re.escape(prefix)}\b")
    try:
        projects = api.list_projects().projects
        return next((p for p in projects if pattern.match(p.name)), None)
    except ApiException as e:
        print(f"❌ Failed to list projects: {e}")
        return None

def add_admin(project_id: str, principal: str):
    """Add collaborator with admin permission; swallow 'already has access' errors."""
    try:
        api.add_project_collaborator(
            cmlapi.AddProjectCollaboratorRequest(permission="admin"),
            project_id,
            principal,
        )
        print(f"  → Added admin: {principal}")
    except ApiException as e:
        status = getattr(e, "status", None)
        msg = (getattr(e, "body", None) or str(e) or "")
        if status in (400, 409):
            print(f"  (already has admin; HTTP {status})")
        elif status == 404:
            print(f"  ⚠️ Principal not found (404): {principal}")
        else:
            print(f"  ❌ Error adding '{principal}' (HTTP {status}): {msg}")

# --- main flow ---
ensure_team_exists(TEAM)

for i in range(1, NUM_PROJECTS + 1):
    project_name = f"AgentLab {i}"
    print(f"\nAssigning permissions to: {project_name}")

    target_project = find_project_by_prefix_bounded(project_name)
    if target_project is None:
        print(f"⚠️ Project not found with prefix '{project_name}'. Skipping.")
        continue

    target_user = f"user{i:03d}"  # user001, user010, ...

    add_admin(target_project.id, target_user)
    add_admin(target_project.id, TEAM)
