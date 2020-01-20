from app import db


users_has_diets = db.Table(
    "users_has_diets",
    db.Column(
        "user_id",
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
    db.Column(
        "diet_id",
        db.ForeignKey("diets.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
)
