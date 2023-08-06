from pathlib import Path
from hawt.sso_auth import login_to_role
from mypy_boto3_identitystore import IdentityStoreClient
from mypy_boto3_identitystore.paginator import ListUsersPaginator, ListGroupMembershipsPaginator
from csv import DictWriter
import typer

app = typer.Typer()


@app.command()
def list_group_memberships_enriched(
        sso_admin_role_name: str = typer.Argument('...', help='SSO Role with read access to Identity Center'),
        sso_admin_account_id: str = typer.Argument('...', help='AWS Account id, like 123456789012'),
        sso_admin_region: str = typer.Argument('...', help='region, like us-east-1'),
        id_store_id: str = typer.Argument('...', help='Go to identity center Dashboard in the AWS web console, click '
                                                      'on the id store, and copy the id from the url'),
        outputPath: Path = Path("./sso_group_memberships.csv")):
    session = login_to_role(sso_admin_role_name, sso_admin_account_id, sso_admin_region)
    client: IdentityStoreClient = session.client("identitystore", region_name="us-east-1")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    users = dict()
    for page in list_users_paginator.paginate(IdentityStoreId=id_store_id):
        page_users = page["Users"]
        for user in page_users:
            users[user["UserId"]] = user
    groups_resp = client.list_groups(IdentityStoreId=id_store_id)
    groups = groups_resp["Groups"]
    with open(outputPath, "w", newline='') as groups_csv_file:
        field_names = ["GroupName", "GroupId", "UserName", "UserId", 'Emails', 'DisplayName', 'Addresses',
                       'IdentityStoreId', 'ExternalIds', 'Locale', 'Name', 'PhoneNumbers', 'Title']
        dict_writer = DictWriter(groups_csv_file, fieldnames=field_names)
        dict_writer.writeheader()
        for group in groups:
            display_name = group["DisplayName"]
            group_id = group["GroupId"]
            memberships_paginator: ListGroupMembershipsPaginator = client.get_paginator("list_group_memberships")
            for membership_page in memberships_paginator.paginate(IdentityStoreId=id_store_id, GroupId=group_id):
                memberships = membership_page["GroupMemberships"]
                for membership in memberships:
                    user_id = membership["MemberId"]["UserId"]
                    row = {"GroupName": display_name, "GroupId": group_id}
                    row.update(users[user_id])
                    dict_writer.writerow(row)
