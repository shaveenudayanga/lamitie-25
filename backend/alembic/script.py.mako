<%! set up_migration = "from alembic import op\nimport sqlalchemy as sa\n" %>
<%!
def upgrade():
    # Commands to upgrade the database schema
    pass
%>
<%!
def downgrade():
    # Commands to downgrade the database schema
    pass
%>

<% set up_migration %>