from app.models.models import GitHubEvent


def github_event_handler(event_type, payload):
  """
  In this function, it handles the business logic of github handler
  It filters out the event types and forms a pydantic response from it.

  Args:
      event_type (string): event types "push" | "pull"  | "merge" from github webhook
      payload (json): payload data from github webhook response body

  """
  if event_type == "push" and payload.get("head_commit"):
    return GitHubEvent(
      request_id=payload["head_commit"]["id"],
      author=payload["pusher"]["name"],
      action="PUSH",
      from_branch=None,
      to_branch=payload["ref"].split("/")[-1],
      timestamp=payload["head_commit"]["timestamp"]
    )
    
  if event_type == "pull_request":
    pr = payload["pull_request"]
    
    if payload["action"] == "opened":
      return GitHubEvent(
          request_id=str(pr["id"]),
          author=pr["user"]["login"],
          action="PULL_REQUEST",
          from_branch=pr["head"]["ref"],
          to_branch=pr["base"]["ref"],
          timestamp=pr["created_at"]
      )
      
    if payload["action"] == "closed" and pr["merged"]:
      return GitHubEvent(
        request_id=str(pr["id"]),
        author=pr["merged_by"]["login"],
        action="MERGE",
        from_branch=pr["head"]["ref"],
        to_branch=pr["base"]["ref"],
        timestamp=pr["merged_at"]
      )
      
  return None