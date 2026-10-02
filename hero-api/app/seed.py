from sqlmodel import Session, SQLModel, select

from app.database import engine
from app.models import Hero, Mission, Team


def seed_database():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        existing_team = session.exec(select(Team)).first()

        if existing_team is not None:
            print("Database already seeded")
            return

        avengers = Team(
            name="Avengers",
            headquarters="New York",
        )
        x_men = Team(
            name="X-Men",
            headquarters="Westchester",
        )

        sokovia = Mission(title="Battle of Sokovia")
        save_new_york = Mission(title="Save New York")

        heroes = [
            Hero(
                name="Tony Stark",
                age=45,
                secret_name="Iron Man",
                team=avengers,
                missions=[sokovia, save_new_york],
            ),
            Hero(
                name="Natasha Romanoff",
                age=35,
                secret_name="Black Widow",
                team=avengers,
                missions=[sokovia],
            ),
            Hero(
                name="Peter Parker",
                age=16,
                secret_name="Spider-Man",
                team=avengers,
                missions=[save_new_york],
            ),
            Hero(
                name="Logan",
                age=150,
                secret_name="Wolverine",
                team=x_men,
                missions=[save_new_york],
            ),
            Hero(
                name="Ororo Munroe",
                age=32,
                secret_name="Storm",
                team=x_men,
                missions=[sokovia],
            ),
        ]

        session.add_all(heroes)
        session.commit()

        print("Database seeded successfully")


if __name__ == "__main__":
    seed_database()
