from __future__ import print_function
import time
import cmlapi
from cmlapi.rest import ApiException
from pprint import pprint

# How many "AgentLab {i}" prefixes to target
num_projects = 4  # change as needed

# API client
api_instance = cmlapi.default_client()

def is_prefix_match(name: str, target_prefix: str) -> bool:
    """Case-insensitive 'starts with' match."""
    return name.lower().startswith(target_prefix.lower())

target_prefixes = [f"AgentLab {i}" for i in range(1, num_projects + 1)]

# Loop until no more deletions occur (safety-capped)
max_passes = 5
pass_num = 0

while pass_num < max_passes:
    pass_num += 1
    print(f"\n--- Deletion pass {pass_num} ---")
    deletions_this_pass = 0

    try:
        projects = api_instance.list_projects().projects
    except ApiException as e:
        print(f"❌ Failed to list projects: {e}")
        break

    # Build list of (id, name) to delete this pass
    to_delete = []
    for p in projects:
        if any(is_prefix_match(p.name, prefix) for prefix in target_prefixes):
            to_delete.append((p.id, p.name))

    if not to_delete:
        print("✅ No matching projects found. Done.")
        break

    # Delete each matched project
    for pid, pname in to_delete:
        try:
            print(f"Deleting project: {pname} (ID: {pid})")
            api_instance.delete_project(pid)
            deletions_this_pass += 1
            print(f"✅ Successfully deleted: {pname}")
            # Small delay to let the backend settle
            time.sleep(1)
        except ApiException as e:
            print(f"❌ ApiException deleting '{pname}' (ID: {pid}): {e}")
            # Continue with others
        except Exception as e:
            print(f"❌ Unexpected error deleting '{pname}' (ID: {pid}): {e}")
            # Continue with others

    # If nothing was deleted this pass, we can stop
    if deletions_this_pass == 0:
        print("ℹ️ No deletions occurred this pass. Stopping.")
        break

# If we hit the pass cap, let the user know
if pass_num >= max_passes:
    print("⚠️ Reached maximum passes. Some projects may remain.")