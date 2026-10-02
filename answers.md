## Question 1

1. Duplicate Avengers:
   Blocked by the UNIQUE constraint because Team.name must be unique.

2. Hero with team_id = 99:
   Blocked by the FOREIGN KEY constraint because team 99 does not exist.

3. Hero with only age:
   Blocked by the NOT NULL constraint because Hero.name is required.

4. Delete team id = 1:
   Blocked by the FOREIGN KEY constraint because existing heroes still reference this team.

## Question 2

Team 1 -------- N Hero
FK: hero.team_id

The foreign key is stored in Hero because each Hero belongs to at most one Team, while one Team can have many Heroes. Therefore each Hero row stores the id of its Team.

## Question 3

Hero N -------- N Mission

## hero

id PK
name
...

## mission

id PK
title

## hero_mission

hero_id PK, FK -> hero.id
mission_id PK, FK -> mission.id

## Question 13

For `GET /heroes?min_age=18&team_id=1`, SQLAlchemy printed:

```sql
SELECT hero.name, hero.age, hero.power, hero.team_id, hero.id, hero.secret_name
FROM hero
WHERE hero.age >= ? AND hero.team_id = ? ORDER BY hero.id
LIMIT ? OFFSET ?
```

The bound parameter values were `(18, 1, 10, 0)`. The values do not appear directly inside the SQL string; the database driver sends them separately as parameters. Therefore they are treated as data rather than executable SQL, which protects the query from SQL injection.

## Question 14

Filtering in the database transfers only the required rows, uses less application memory, and lets the database use indexes and its optimized query engine. Loading every hero and filtering in Python becomes slow and wasteful as the table grows, and it also makes pagination inaccurate or unnecessarily expensive.

## Question 15

`create_all()` creates tables that are present in `SQLModel.metadata` but missing from the database. It created `mission` and `heromissionlink` because they were new, but did nothing to the existing `hero` table. It does not alter an existing table to match later model changes.

## Question 16

The observed INSERT order was:

1. `team`
2. `mission`
3. `hero`
4. `heromissionlink`

The relationships told SQLAlchemy about the dependencies. It inserted the teams and missions first, obtained their generated primary keys, then automatically used those values for `hero.team_id` and for both foreign keys in `heromissionlink`.

## Question 17

After adding `power` to the model and only restarting the server, the existing `hero` table had no `power` column. `GET /heroes` then tried to select `hero.power` and failed with an `OperationalError` (`no such column: hero.power`). This happens because `create_all()` creates missing tables but does not migrate existing ones. Dropping all tables is not acceptable in production because it destroys existing data and causes avoidable downtime.

## Question 18

The generated migration contains:

```python
def upgrade() -> None:
    op.add_column(
        "hero",
        sa.Column(
            "power",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("hero", "power")
```

`upgrade()` adds the nullable `power` column. `downgrade()` reverses the revision by removing that column.

## Question 19

Alembic stores the current revision in the database table `alembic_version`. The `migrations/` folder should be committed to Git so every environment and teammate applies the same ordered, reviewable schema changes and can reproduce or roll them back consistently.

## Question 20

Autogenerate treated the rename as two unrelated changes:

```python
op.add_column(
    "hero",
    sa.Column(
        "alias",
        sqlmodel.sql.sqltypes.AutoString(),
        nullable=False,
    ),
)
op.drop_column("hero", "secret_name")
```

Applying that migration could delete every existing `secret_name` value, and adding a non-null column can also fail while rows already exist. The migration should be reviewed and changed to a real rename, for example:

```python
op.alter_column("hero", "secret_name", new_column_name="alias")
```

The downgrade should rename `alias` back to `secret_name`. As required by the exercise, the experimental revision was deleted and the model rename was undone.
