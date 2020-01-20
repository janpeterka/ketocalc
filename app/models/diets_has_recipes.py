from app import db

diets_has_recipes = db.Table(
    "diets_has_recipes",
    db.Column(
        "diet_id",
        db.ForeignKey("diets.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
    db.Column(
        "recipes_id",
        db.ForeignKey("recipes.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
)