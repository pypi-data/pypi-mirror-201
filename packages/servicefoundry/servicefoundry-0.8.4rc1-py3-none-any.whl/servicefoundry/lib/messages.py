SFY = "sfy"

# TODO: probably create another `rich_messages.py` and apply all formatting there
PROMPT_LOGIN_SUCCESSFUL = f"""[green bold]Login Successful![/]"""
PROMPT_LOGIN_INFO = (
    f"""[yellow]You are logged in as {{username!r}} with email {{email!r}}[/]"""
)
PROMPT_LOGOUT_SUCCESSFUL = f"""[green bold]Logged Out![/]"""
PROMPT_POST_LOGIN = ""
PROMPT_ALREADY_LOGGED_OUT = f"""[yellow]You are already logged out[/]"""
PROMPT_USING_CLUSTER_CONTEXT = f"""[yellow]Using cluster {{!r}}[/]"""
PROMPT_USING_WORKSPACE_CONTEXT = f"""[yellow]Using workspace {{!r}}[/]"""
PROMPT_USING_APPLICATION_CONTEXT = f"""[yellow]Using application {{!r}}[/]"""
PROMPT_CREATING_NEW_WORKSPACE = f"""[yellow]Creating a new workspace {{!r}}[/]"""
PROMPT_DELETING_WORKSPACE = f"""[yellow]Deleting workspace {{!r}}[/]"""
PROMPT_DELETED_WORKSPACE = f"""[green]Deleted workspace {{!r}}[/]"""
PROMPT_DELETING_SERVICE = f"""[yellow]Deleting service {{!r}}[/]"""
PROMPT_DELETED_SERVICE = f"""[green]Deleted service {{!r}}[/]"""
PROMPT_NO_WORKSPACES = f"""[yellow]No workspaces found. Either cluster name is wrong, or your cluster doesn't contain any workspaces. You can create one with [bold]{SFY} create workspace[/][/]"""
PROMPT_NO_APPLICATIONS = f"""[yellow]No applications found. You can create one with [bold]{SFY} deploy[/] from within your application folder"""
PROMPT_NO_VERSIONS = f"""[yellow]No application versions found."""
