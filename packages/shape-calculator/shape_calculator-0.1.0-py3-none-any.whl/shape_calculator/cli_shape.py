import click

from src.shape_calculator.shapes.rectangle import Rectangle
from src.shape_calculator.shapes.triangle import Triangle


@click.command()
@click.option("--count", default=1, prompt="Frequency", help="Number of frequency to calculate.")
@click.option(
    "--shape",
    default="y",
    type=click.Choice(["y", "n"]),
    prompt='Rectangle? Triangle if "n"',
    help="The shape to choose.",
)
@click.option(
    "--value1",
    default=3,
    prompt="width or base",
    help="If the shape is rectangle, the value should be width. If the shape is triangle, the value should be base.",
)
@click.option(
    "--value2",
    default=4,
    prompt="height or height",
    help="If the shape is rectangle, the value should be height. If the shape is triangle, the value should be height.",
)
@click.option(
    "--side1", default=1, prompt="side1", help="If the shape is triangle, the value should be side1."
)
@click.option(
    "--side2", default=2, prompt="side2", help="If the shape is triangle, the value should be side2."
)
@click.option(
    "--side3", default=3, prompt="side3", help="If the shape is triangle, the value should be side3."
)
def cli_shape(count, shape, value1, value2, side1, side2, side3):
    """Simple cli program that calculates from Shape class for a total of COUNT times."""
    for _ in range(count):
        if shape == "y":
            click.echo("Rectangle Calculated, width: {}, height: {}".format(value1, value2))
            rectangle = Rectangle(value1, value2)
            click.echo(rectangle.__repr__())
        else:
            click.echo(
                "Triangle Calculated, base: {}, height: {}, side1: {}, side2: {}, side3: {}".format(
                    value1, value2, side1, side2, side3
                )
            )
            triangle = Triangle(value1, value2, side1, side2, side3)
            click.echo(triangle.__repr__())
