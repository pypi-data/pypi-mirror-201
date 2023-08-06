# Highspot Amazon Web Services Tools (HAWT)
A collection of utilities for working with Amazon Web Services (AWS) from the command line.
Often adds the missing "all in one" API call that AWS should have provided.

## Installation
pipx install hawt

## Usage
```
 Usage: hawt [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                              │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.       │
│ --help                        Show this message and exit.                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ hello                                                                                                                │
│ identitycenter                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Get help on a specific command:

```
hawt identitycenter list-group-memberships-enriched --help
                                                                                                                                                      
 Usage: hawt identitycenter list-group-memberships-enriched                                                                                           
            [OPTIONS] [SSO_ADMIN_ROLE_NAME] [SSO_ADMIN_ACCOUNT_ID]                                                                                    
            [SSO_ADMIN_REGION] [ID_STORE_ID]                                                                                                          
                                                                                                                                                      
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   sso_admin_role_name       [SSO_ADMIN_ROLE_NAME]   SSO Role with read access to Identity Center [default: ...] │
│   sso_admin_account_id      [SSO_ADMIN_ACCOUNT_ID]  AWS Account id, like 123456789012 [default: ...]            │
│   sso_admin_region          [SSO_ADMIN_REGION]      region, like us-east-1 [default: ...]                       │
│   id_store_id               [ID_STORE_ID]           Go to identity center Dashboard in the AWS web console,     │
│                                                     click on the id store, and copy the id                      │
│                                                     from the url                                                │
│                                                     [default: ...]                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --outputpath        PATH  [default: sso_group_memberships.csv]                                                  │
│ --help                    Show this message and exit.                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
